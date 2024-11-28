import fitz
import spacy
import pandas as pd
import numpy as np 
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, StratifiedKFold
from verify_data import ground_truth
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder

file_path = '/Users/yosolukito/Documents/web_aic_lomba_compfest_2024/CV_Zaky_Yusuf_Pahlevi.pdf'
nlp = spacy.load('en_core_web_sm')

# membaca file pdf 
def read_pdf_cv(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

projects_name = [
    "Binus Bekasi Room Management", 
    "TraveloHI", 
    "NewEgg Website Clone", 
    "Caddo Catering Online", 
    "Waste Bank Desktop Application"
]

# list prog skill
list_prog_skill = [
    "Python",
    "JavaScript",
    "Java",
    "C",
    "C++",
    "C#",
    "Ruby",
    "PHP",
    "Swift",
    "Kotlin",
    "Go",
    "Rust",
    "Perl",
    "R",
    "Scala",
    "TypeScript",
    "Objective-C",
    "Lua",
    "Haskell",
    "Elixir",
    "Clojure",
    "Dart",
    "MATLAB",
    "F#",
    "Erlang",
    "VB.NET",
    "Assembly",
    "SQL",
    "SAS",
    "Shell",
    "Prolog",
    "Julia",
    "Groovy",
    "Scheme",
    "COBOL",
    "Fortran",
    "Ada",
    "Pascal",
    "Lisp",
    "Smalltalk",
    "Tcl",
    "Hack",
    "Delphi/Object Pascal",
    "Crystal",
    "Nim",
    "Elm",
    "VHDL",
    "Verilog",
    "ABAP",
    "RPG",
    "PL/SQL",
    "Apex",
    "Solidity",
    "Forth",
    "ML",
    "OCaml",
    "Awk",
    "PostScript",
    "Racket",
    "Logo",
    "Scratch",
    "Bash",
    "PowerShell",
    "D",
    "Chapel",
    "Zig",
    "Pony",
    "Io",
    "Rebol",
    "Red",
    "Eiffel",
    "J",
    "K",
    "Q",
    "Squirrel",
    "Neko",
    "BASIC",
    "PureScript",
    "CoffeeScript",
    "LiveScript",
    "Ada",
    "Modula-2",
    "ALGOL",
    "Simula",
    "BCPL",
    "B",
    "ZPL",
    "Vala",
    "Cobra",
    "Factor",
    "Fantom",
    "Io",
    "X10",
    "XQuery",
    "XSLT",
    "SML",
    "Nimrod",
    "ATS",
    "ChucK",
    "E",
    "Fantom",
    "Fortress",
    "JScript",
    "NATURAL",
    "Nemerle",
    "NXC",
    "OpenCL",
    "Oz",
    "RPG",
    "Turing",
    "VHDL",
    "Wolfram",
    "XC"
]

# membaca data file pdf
data_has_reader_pdf = read_pdf_cv(file_path)
data_real_currwork = ''

# ekstrak informasi dari CV 
def extract_information(text):
    
    doc = nlp(text)

    skills = []
    achievements = []
    
    projects = []
    languages = []
    latest_skills = []

    programming_language_skills = []
    framework_skills = []
    database_management_skills = []
    tools_skills = []

    # ekstrak mendapatkan data yang dikerjakan sekarang
    if "EXPERIENCES" in text: 
        experiences = text.split("EXPERIENCES")[1].split("RELEVANT PROJECTS")[0]
        # print(experiences)
        # remove list point
        experiences = [item.strip() for item in experiences.split("●")]
        # menghapus \n
        experiences = [item.replace('\n', ' ') for item in experiences]
        # mendapatkan pekerjaan sekarang 
        curr_work = experiences[0]
        curr_work = curr_work.replace(' – ','-')
        # preprocessing the curr_work untuk remove '-'
        curr_work = [s.strip() for s in curr_work.split('-')]
        data_real_currwork = curr_work[0]

        # get latest work skills that use
        # print(experiences)

    # ekstrak skill data 
    if "SKILLS" in text or "LANGUAGE" in text or "Frameworks" in text or "EXPERIENCES":
        skills_section = text.split("SKILLS")[1].split("LANGUAGE")[0]
        # for splitting dot list
        skills = [line.strip() for line in skills_section.split("●") if line.strip()]
        # for taking data that programming lang with splitting :
        programming_language_skills = [item.split(": ")[1] for item in skills if "Programming Languages:" in item]
        
        # change programming skills string to array with split ','
        programming_language_skills = programming_language_skills[0].split(', ')

        # for framework and libraries 
        framework_skills = [item.split(": ")[1] for item in skills if "Frameworks/Libraries:" in item]
        framework_skills = framework_skills[0].split(', ')
        
        # for database managemewnt preprocessing 
        database_management_skills = [item.split(': ')[1] for item in skills if "Database Management:" in item]
        database_management_skills = database_management_skills[0].split(', ')
        
        # for tools preprocessing 
        tools_skills = [item.split(": ")[1] for item in skills if "Tools" in item]
        tools_skills = [item.replace("\n", " ") for item in tools_skills]
        tools_skills = tools_skills[0].split(', ')
        # print(tools_skills)
    
    # ambil data relevant project 
    if "RELEVANT PROJECTS" in text:
        text_project = text.split("RELEVANT PROJECTS")[1].split("ACHIEVEMENTS")[0].strip()
        
        # masukkan ke dalam doc spacy 
        doc_text_project = nlp(text_project)
        in_project_section = False 
        text_projects_real = []

        for sent in doc_text_project.sents: 
            in_project_section = True 
            if in_project_section and sent.text.strip() == "":
                in_project_section = False

            if in_project_section:
                text_projects_real.append(sent.text.strip())

        text_projects_real = [line.replace('●', '') for line in text_projects_real]
        text_projects_real = [line.replace('\n', ' ').strip() for line in text_projects_real]
        
        # validasi text projects real dengan lainnya
        for txt in text_projects_real:
            for proj in projects_name:
                if proj in txt: 
                    projects.append(proj)

    # achievements data 
    if "ACHIEVEMENTS" in text: 
        # jika ada achievement pada teks kategorisasikan
        text_achievement = text.split("ACHIEVEMENTS")[1].split("SKILLS")[0].strip()
        # jika terdapat \n pada teks split terlebih dahulu
        text_achievement = text_achievement.split('\n')
        # gabung menjadi string array yang digabung
        test_txt = " ".join(text_achievement)
        # implementasi nlp ke text achievement
        ach_doc = nlp(test_txt)
        # tokenisasi
        ach_data = [token.text for token in ach_doc]
        ach_after_token = " ".join(ach_data)
        # data setelah token diimplementasi dengan nlp 
        doc_ach_after_token = nlp(ach_after_token)

        achievement_real = []
        # ambil data achievement dengan model spacy 
        for ent in doc_ach_after_token.ents:
            if ent.label_ == 'WORK_OF_ART' or ent.label_ == "EVENT":
                achievement_real.append(ent.text)

    return data_real_currwork, programming_language_skills, framework_skills, database_management_skills, tools_skills, achievement_real, projects


# menampilkan hasil data result dari proses ekstrak cv 
data_real_currwork, programming_language_skills, framework_skills, database_management_skills, tools_skills, achievement_real, projects=extract_information(data_has_reader_pdf)

# membuat variable data yang berhasil di extract 
data_extract = {
    "current_work": data_real_currwork, 
    "programming_language": programming_language_skills, 
    "framework_skills": framework_skills, 
    "database_management_skills": database_management_skills, 
    "tools_skills": tools_skills, 
    "achievements": achievement_real, 
    "projects": projects
}

print(data_extract)

# menghitung akurasi dengan menggunakan precision, recall, f1
# Fungsi untuk menghitung precision, recall, f1 untuk setiap kategori
def calculate_scores(ground_truth, extracted_data):
    categories = ground_truth.keys()
    precision_scores = {}
    recall_scores = {}
    f1_scores = {}
    
    for category in categories:
        true_values = set(ground_truth[category])
        extracted_values = set(extracted_data[category])
        
        true_positives = len(true_values.intersection(extracted_values))
        false_positives = len(extracted_values - true_values)
        false_negatives = len(true_values - extracted_values)
        
        precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

        
        precision_scores[category] = precision
        # recall_scores[category] = recall
        # f1_scores[category] = f1
    
    return precision_scores

# menghitung skor akurasi 
precision_scores = calculate_scores(ground_truth, extracted_data=data_extract)

# Mencetak hasil
print("Precision Scores per Category:")
for category, score in precision_scores.items():
    print(f"{category}: {score:.2f}")

# melakukan predict future job work (section)

# read csv skill project
df_skillsproject = pd.read_csv('SkillProject.csv')
# Menggabungkan list menjadi string untuk setiap kolom yang berisi list
df_skillsproject['ProgrammingSkills'] = df_skillsproject['ProgrammingSkills'].apply(lambda x: ' '.join(eval(x)) if isinstance(x, str) else str(x))
df_skillsproject['Framework'] = df_skillsproject['Framework'].apply(lambda x: ' '.join(eval(x)) if isinstance(x, str) else str(x))
df_skillsproject['DatabaseSkills'] = df_skillsproject['DatabaseSkills'].apply(lambda x: ' '.join(eval(x)) if isinstance(x, str) else str(x))
df_skillsproject['ToolsSkills'] = df_skillsproject['ToolsSkills'].apply(lambda x: ' '.join(eval(x)) if isinstance(x, str) else str(x))

# mengambil data x (data yang digunakan untuk mendapatkan target)
combine = df_skillsproject['TotalProject'].astype(str) +' '+ \
        df_skillsproject['ProgrammingSkills']+ ' '+ \
        df_skillsproject['Framework'] + ' ' + \
        df_skillsproject['DatabaseSkills'] + ' ' + \
        df_skillsproject['ToolsSkills'] + ' ' + \
        df_skillsproject['Description']

x = combine
print(x)
# mengambil data y (target label)
y = df_skillsproject['Job'].values

print(df_skillsproject['Job'].value_counts())

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

# membuat pipeline 
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()), 
    ('clf', RandomForestClassifier(random_state=42))
])

# melakukan fit & menghitung score akurasi 1 
pipeline.fit(x_train, y_train).score(x_test, y_test)

y_pred = pipeline.predict(x_test)

# data user cv yang dimasukkan 
new_data = "4 [Python JavaScript Go] [NextJs Springboot Gin Gorilla] [MySQL SQL Server Management Studio] [Docker Kubernetes Google Collab]"
# print(pipeline.predict([new_data]))

# function predict job recommendation 
def recommend_job_function(new_data):
    # probabilitas untuk setiap pekerjaan yang direkomendasikan  
    probs = pipeline.predict_proba([new_data])

    # mendapatkan label pekerjaan 
    job_labels = pipeline.classes_

    # melakukan urutan probabilitas 
    top_data = 3
    sorted_indices = probs[0].argsort()[::-1][:top_data]
    recommend_jobs = job_labels[sorted_indices]
    recommend_props = probs[0][sorted_indices]

    # menampilkan data serta prob 
    list_recommend_jobs = []
    for job, prob in zip(recommend_jobs, recommend_props):
        # ambil description job 
        description = df_skillsproject[df_skillsproject['Job'] == job]['Description'].values[0]
        print(f"{job}: {prob*100:.2f}%")
        list_recommend_jobs.append({'job': job, 'prob': prob, 'description': description})

    return list_recommend_jobs

print(recommend_job_function(new_data=new_data))

# check accuracy score (proses testing dalam pengembangan)
sk = StratifiedKFold(n_splits=5)
score = cross_val_score(pipeline,x,y, cv=sk, scoring='accuracy')

print(f"Result cross val score: {score}")

# melakukan rekomendasi training yang bisa dia dapatkan degan similarity cosine 
# dengan word2vec word moverse distance 
from gensim.models import Word2Vec

# contoh list training data yang bisa digunakan 
training_list_1 = ["learn excel fundamental", 
                   "learn business fundamental", 
                   "mastering excel in one month",
                   "mastering data analysis", 
                   "guide for beginning of programming", 
                   "mastering Python for beginner", 
                   "mastering Python for intermediate", 
                   "mastering Python for expert", 
                   "mastering R for beginner", 
                   "mastering R for intermediate", 
                   "mastering R for expert", 
                   "mastering Data Structures for Beginner", 
                   "mastering Data Structure for Intermediate", 
                   "introduction to Computer Network", 
                   "mastering CCNA for Beginner"]

# membuat model word2vec
model = Word2Vec(training_list_1, min_count=1, vector_size=100, workers=4)

# menyiapkan dictionary untuk membantu proses mendapatkan data 
course_reccomendations = {}
# membuat vector fitur untuk setiap dokumen
# format data input 
# "4 [Python JavaScript] [NextJs Springboot] [MySQL] [Docker]"
def prediction(data_input):
    get_predicted_future_job = recommend_job_function(data_input)

    # loop setiap get predicted future job 
    for pred_job in get_predicted_future_job:
        predicted_job_text = pred_job['job']
        distance_course_pairs = []
        # belum selese mau pulang

        for tl in range(len(training_list_1)): 
            # mengukur jarak antara predicted job dengan course 
            distance = model.wv.wmdistance(training_list_1[tl], predicted_job_text, norm=False)

            # menambahkan data course ke dalam list 
            distance_course_pairs.append((distance, training_list_1[tl]))

        # melakukan sort berdasarkan data terkecil 
        distance_course_pairs.sort(key=lambda x: x[0])

        # ambil top 5 courses 
        top_5_courses = [course for _,course in distance_course_pairs[:5]]

        # simpan ke dalam course recommendation 
        course_reccomendations[pred_job['job']] = top_5_courses

    # print akhir untuk check 
    print(course_reccomendations)

    return get_predicted_future_job, course_reccomendations

prediction("4 [Python JavaScript] [NextJs Springboot] [MySQL] [Docker]")


