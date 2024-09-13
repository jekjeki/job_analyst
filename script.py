import fitz
import spacy
import pandas as pd
import numpy as np 
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, StratifiedKFold

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

        # implementasi spacy 
        # join_pg_skill = " ".join(programming_language_skills)
        
        # for pg in programming_language_skills:
        #     pg_doc = nlp(pg)
        #     pg_data = [token.text for token in pg_doc if token.text in list_prog_skill]
        #     print(pg_data)
        #     programming_language_skills.extend(pg_data)
        # print(programming_language_skills)


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

        # for text in text_achievement: 
        #     if text.strip() and text.startswith("Best") or text.startswith("Finalist"):
        #         achievements.append(text.strip())
    return data_real_currwork, programming_language_skills, framework_skills, database_management_skills, tools_skills, achievement_real, projects


# menampilkan hasil data result dari proses ekstrak cv 
data_real_currwork, programming_language_skills, framework_skills, database_management_skills, tools_skills, achievement_real, projects=extract_information(data_has_reader_pdf)

print(f"curr work: {data_real_currwork}")
print(f"programming language: {programming_language_skills}")
print(f"framework: {framework_skills}")
print(f"database management: {database_management_skills}")
print(f"tools skills: {tools_skills}")
print(f"achievement: {achievement_real}")
print(f"projects: {projects}")

# melakukan predict future job work (section)

# read csv skill project
df_skillsproject = pd.read_csv('SkillProject.csv')
df_skillsproject['ProgrammingSkills'] = df_skillsproject['ProgrammingSkills'].apply(lambda x: ''.join(x))
df_skillsproject['Framework'] = df_skillsproject['Framework'].apply(lambda x: ''.join(x))
df_skillsproject['DatabaseSkills'] = df_skillsproject['DatabaseSkills'].apply(lambda x: ''.join(x))
df_skillsproject['ToolsSkills'] = df_skillsproject['ToolsSkills'].apply(lambda x: ''.join(x))

combine = df_skillsproject['TotalProject'].astype(str) +' '+ \
        df_skillsproject['ProgrammingSkills']+ ' '+ \
        df_skillsproject['Framework'] + ' ' + \
        df_skillsproject['DatabaseSkills'] + ' ' + \
        df_skillsproject['ToolsSkills']

x = combine
y = df_skillsproject.iloc[:, 0].values 

print(x)

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

# membuat pipeline 
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()), 
    ('clf', RandomForestClassifier(random_state=42))
])

# melakukan fit
pipeline.fit(x_train, y_train)

y_pred = pipeline.predict(x_test)

new_data = "4 [Python JavaScript Go] [NextJs Springboot Gin Gorilla] [MySQL SQL Server Management Studio] [Docker Kubernetes Google Collab]"
print(pipeline.predict([new_data]))

# check accuracy score (proses testing dalam pengembangan)
# sk = StratifiedKFold(n_splits=2)
# score = cross_val_score(pipeline,x,y, cv=sk)

# print(score)

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
list_courses = {}

# membuat vector fitur untuk setiap dokumen
# format data input 
# "4 [Python JavaScript] [NextJs Springboot] [MySQL] [Docker]"
def prediction(data_input):
    get_predicted_future_job = pipeline.predict([data_input]) 
    for tl in range(len(training_list_1)):  
        distance = model.wv.wmdistance(training_list_1[tl], get_predicted_future_job[0], norm=False)
        list_courses[distance] = training_list_1[tl]

    # get top 5 of courses that available with they skills
    top_5_courses = []
    flag = 0 
    for i in sorted(list_courses.keys()):
        if flag <= 4:
            top_5_courses.append(list_courses[i])
        else: 
            break
        flag = flag + 1

    return pipeline.predict([data_input]), top_5_courses



