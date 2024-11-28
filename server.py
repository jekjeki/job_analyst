from flask import Flask, request, url_for, redirect, render_template, jsonify, Response
import os
from script import read_pdf_cv, extract_information, prediction
from flask_cors import CORS
from transformers import pipeline
from huggingface_hub import InferenceClient
import zipfile

repo_id = "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = '/Users/yosolukito/Documents/web_aic_lomba_compfest_2024/upload'




client = InferenceClient(api_key="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")

@app.route('/analyze-zip', methods=['POST', 'GET'])
def analyze_zip():
    uploaded_file_user = request.files.get("file")
    project_desc = request.form.get("description")

    # validasi user data 
    if not uploaded_file_user or not project_desc: 
        return jsonify({"error": "missing project file or project question"}), 400 
    
    # validasi file ended .zip
    if not uploaded_file_user.filename.endswith(".zip"):
        return jsonify({"error": "only zip files that supported"}), 400
    
    # Save the uploaded ZIP file
    zip_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file_user.filename)
    uploaded_file_user.save(zip_path)

    # Extract ZIP file contents
    extracted_contents = []
    extracted_path = os.path.join(app.config["UPLOAD_FOLDER"], 'extracted')
    os.makedirs(extracted_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_path)

    # Read files in the extracted folder
    for root, _, files in os.walk(extracted_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                extracted_contents.append(content)

    # Combine extracted file contents for analysis
    combined_content = " ".join(extracted_contents)

    question = f"""
        Question: {project_desc}
        Answer: {combined_content}
        Please evaluate the answer what is must be fixed from this answer for get best result based on Question?
    """

    messages = [{"role": "user", "content": question}]

    def generate():
        try: 
            stream = client.chat.completions.create(
                model="microsoft/Phi-3.5-mini-instruct",
                messages=messages,
                max_tokens=800,
                stream=True
            )

            for chunk in stream: 
                content = chunk.choices[0].delta.get("content", "")
                yield content
        except Exception as e:
            yield f'Error: {str(e)}'
    
    return Response(generate(), content_type='text/plain')

# chat api 
@app.route('/chat-completion', methods=['POST', 'GET'])
def chat_completion():
    data = request.json
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    def generate():
        try:
            stream = client.chat.completions.create(
                model="microsoft/Phi-3.5-mini-instruct",
                messages=messages,
                max_tokens=800,
                stream=True
            )
         
            for chunk in stream:
                
                content = chunk.choices[0].delta.get("content", "")
                yield content
        except Exception as e:
            yield f"Error: {str(e)}"

    # Return a streamed response
    return Response(generate(), content_type="text/plain")


@app.route("/")
def index():
    return render_template('main.html')

@app.route("/upload", methods=['POST'])
def upload_file():
    
    file = request.files['file']

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # membaca isi file pdf 
        pdf_text = read_pdf_cv(file_path)

        # melakukan proses NLP dari hasil teks yang didapatkan 
        data_real_currwork, programming_language_skills, framework_skills, database_management_skills, tools_skills, achievement_real, projects = extract_information(pdf_text)
        
        # melakukan proses predict berdasarkan total project, bahasa, framework, database, tools
        data_input_prediction = str(len(projects))+' '+str(programming_language_skills)+' '+str(framework_skills)+' '+str(database_management_skills)+' '+str(tools_skills)

        predicted_job, top_5_courses = prediction(data_input=data_input_prediction)
        print(type(predicted_job))

        return jsonify({  
            "current_work": data_real_currwork, 
            "programming_language": programming_language_skills,
            "frameworks_skills": framework_skills, 
            "database_skills":database_management_skills, 
            "tools_skills": tools_skills, 
            "achievements": achievement_real, 
            "number_of_projects": projects, 
            "predicted_job": predicted_job, 
            "top_5_courses": top_5_courses, 
            }), 200
    



    
if __name__ == '__main__':
    app.run(debug=True)
    
