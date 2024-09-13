from flask import Flask, request, url_for, redirect, render_template, jsonify
import os
from script import read_pdf_cv, extract_information, prediction
from flask_cors import CORS
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = '/Users/yosolukito/Documents/web_aic_lomba_compfest_2024/upload'

# config for google cloud platform 
project_id = "850946675474"
endpoint_id = "4656582376724365312"
region = "us-central1"

# define ai platform for google cloud
aiplatform.init(project=project_id, location=region)

# connect vertex ai 
vertexai.init(project="850946675474", location="us-central1")

# melakukan config project dengan LLAama
endpoint = aiplatform.Endpoint(endpoint_id)

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
        print(type(predicted_job.tolist()))

    #    ai that description the project 
        model = GenerativeModel("gemini-1.5-flash-001")
        responses = model.generate_content(
            f"summarize the job of {predicted_job}", stream=True
        )

        # loop the response
        rlist = [] 
        for r in responses:
            rlist.append(r.text.replace("*",''))

        return jsonify({  
            "current_work": data_real_currwork, 
            "programming_language": programming_language_skills,
            "frameworks_skills": framework_skills, 
            "database_skills":database_management_skills, 
            "tools_skills": tools_skills, 
            "achievements": achievement_real, 
            "number_of_projects": projects, 
            "predicted_job": predicted_job.tolist(), 
            "top_5_courses": top_5_courses, 
            "explanation_backend": "".join(rlist)
            }), 200
    
@app.route('/task/<courseid>', methods=['GET'])
def give_course(courseid):

# TODO(developer): Set the following variables and un-comment the lines below
# PROJECT_ID = "your-project-id"
# MODEL_ID = "gemini-1.5-flash-001"
    if courseid:
        model = GenerativeModel("gemini-1.5-flash-001")
        responses = model.generate_content(
            f"give me simple learning path about {courseid}", stream=True
        )

    rlist = []
    for response in responses:
        print(response.text)
        rlist.append(response.text.replace('*',''))
    
    return jsonify({
        "status": 400, 
        "learning_path": "".join(rlist)
    })

# function for getting question about that send 
@app.route("/question/<courseid>", methods=['GET'])
def get_question(courseid):
    if courseid: 
        total = []
        model = GenerativeModel('gemini-1.5-flash-001')

        # make three question 
        for i in range(3):
            rlist = []
            responses = model.generate_content(
                f"give me one multiple choice question and answer about {courseid}", stream=True
            )

            # question obj
            qst = {}

            for r in responses:
                print(r.text)
                rlist.append(r.text)
            

    return jsonify({
        "status": "success", 
        "data": "".join(rlist)
    }), 200
    
if __name__ == '__main__':
    app.run(debug=True)
    
