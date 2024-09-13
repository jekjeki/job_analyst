import Image from "next/image";
import { Inter } from "next/font/google";
import axios from 'axios'
import { FormEvent, useState } from "react";
import { useRouter } from "next/router";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const router = useRouter()

  const handleFileChange = (e : React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null 
    setSelectedFile(file)
  }

  // upload file cv API 
  const uploadFile = async (event: FormEvent) => {
    event.preventDefault()

    const formData = new FormData();
    formData.append('file', selectedFile); 
    await axios.post("http://127.0.0.1:5000/upload", formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/json',
      },
    })
    .then((response)=>{
      console.log(response.data)
      router.push({
        pathname: '/summary', 
        query: {
          explanation_backend: response.data.explanation_backend,
          curr_work: response.data.current_work, 
          programming_language: response.data.programming_language, 
          framework_skills: response.data.frameworks_skills, 
          database_skills: response.data.database_skills, 
          tools_skills: response.data.tools_skills, 
          achievements: response.data.achievements, 
          number_of_projects: response.data.number_of_projects, 
          predicted_job: response.data.predicted_job, 
          top_5_courses: response.data.top_5_courses
        }
      })
    })
  }

  return (
    <main
      style={{
        background: `rgb(9,9,121)`, 
      }}
      className={`flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}
    >
      <div>
        <div
        className="text-7xl bg-gradient-to-r from-violet-500 to-fuchsia-500 bg-clip-text text-transparent min-h-20">
          <p>Welcome to AI Job Recommend and Learning System</p>
        </div>
        <div className="text-[30px] text-center bg-gradient-to-r from-violet-500 to-fuchsia-500 bg-clip-text text-transparent min-h-20">
          <p>Upload your CV file !</p>
        </div>
        <div className="mt-[80px] flex justify-center items-center text-white">
          <div className="min-h-20 flex flex-col">
              <input onChange={handleFileChange} type="file" name="file" />
              <input onClick={uploadFile} className="mt-2 bg-teal-500 rounded p-3" type="submit" name="upload" />
          </div>
        </div>
      </div>
    </main>
  );
}
