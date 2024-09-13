import BoldTextParser from "@/component/BoldParser";
import axios from "axios";
import { useParams } from "next/navigation";
import React, { useEffect, useState } from "react";

function DetailQuestion() {
  const params = useParams();
  console.log(params);
  let savedAns = []

  // make api for generate learning path based on course
  const generateLearningPath = () => {
    axios.get(`http://127.0.0.1:5000/task/${params.id}`).then((res) => {
      console.log(res);
      const lines = res.data.learning_path.split("\n");
      const formattedText = lines.join("<br>");
      let lp = document.getElementById("learn-path");

      if (lp) {
        lp.innerHTML = formattedText;
      }
    });
  };

  // Approach 2: Using String Methods
function extractAnswerString(text) {
  const start = text.indexOf("## Answer:") + "## Answer:".length;
  const end = text.indexOf("**Explanation:**");
  if (start !== -1 && end !== -1 && start < end) {
    return text.substring(start, end).trim();
  }
  return null;
}

  // generate question about the course 
  const generateQuestion = () => {
    axios.get(`http://127.0.0.1:5000/question/${params.id}`)
    .then((resp)=>{
      console.log(resp.data.data) 

      const qs_from_cloud = resp.data.data.split("\n")

      // save the answer 
      savedAns = extractAnswerString(resp.data.data)
      console.log(savedAns)

      let txtFormatted = qs_from_cloud.join("<br>")
      // insert the text to inner html 
      let qs = document.getElementById("questions")
      if(qs){
        qs.innerHTML = txtFormatted
      }
    })
  }

  useEffect(() => {
    generateLearningPath();
    generateQuestion()

  }, []);

  return (
    <div className="bg-indigo-700 min-h-screen p-4">
      <div className="mx-[20px] py-2 min-h-5 bg-white rounded-lg">
        <div className="text-center text-xl font-bold">
          <p>{params.id}</p>
        </div>
        <div className="px-4" id="learn-path"></div>
      </div>
      <div className="mx-[20px] mt-5 rounded-xl bg-white">
        <div className="mx-[20px] p-4">
          <p>{`Example test about ${params.id}`}</p>
        </div>
        <div className="mx-[20px] p-4" id="questions">
          
        </div>
      </div>
    </div>
  );
}

export default DetailQuestion;
