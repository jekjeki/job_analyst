import BoldTextParser from "@/component/BoldParser";
import axios from "axios";
import { useParams } from "next/navigation";
import React, { useEffect, useState } from "react";
import { InboxOutlined } from '@ant-design/icons';
import { UploadProps, Button, message } from 'antd';
import {Upload} from 'antd'
import { Session } from "inspector/promises";

const { Dragger } = Upload;

function DetailQuestion() {
  const params = useParams();
  const [task, setTask] = useState('')
  const [fileList, setFileList] = useState<any[]>([]);

  console.log(params);

  // make function to connect with api model 
  const ModelApi = () => {

    const id = Array.isArray(params.id) ? params.id.join('') : params.id

    const stored = sessionStorage.getItem(id) || null 
    // check session storage 
    if(stored){
      setTask(stored as string)
    }
    else{
        axios.post("http://127.0.0.1:5000/chat-completion", {
          messages: [
            {"role": "user", "content": `give me simple project question that can I develop about ${params.id} !`}
          ]
        })
        .then((res)=>{
          console.log(res.data)
          sessionStorage.setItem(id, res.data)
          setTask(res.data as string)
        })
      }
    }

    // submit data and analyze the data based on question that given 
    const handleUploadAnswer = async () => {

      // set obj to form data 
      const formData = new FormData()
      formData.append("description", sessionStorage.getItem(Array.isArray(params.id) ? params.id.join('') : params.id) || '')
      formData.append("file", fileList[0].originFileObj)

      

      try {
        const response = await axios.post(`http://127.0.0.1:5000/analyze-zip`,formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })

        console.log(response.data)

      } catch (error) {
        console.log(error)
      }

    }

    // props data 
    const uploadProps: UploadProps = {
      onRemove: (file: any) => {
        setFileList([]);
      },
      beforeUpload: (file: any) => {
        if (!file.name.endsWith(".zip")) {
          message.error("Only .zip files are supported.");
          return Upload.LIST_IGNORE;
        }
        setFileList([file]);
        return false; // Prevent automatic upload
      },
      fileList,
      accept: ".zip",
    }

  useEffect(()=>{
    ModelApi()
  }, [])

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
          <div className="flex flex-wrap">
              <pre className="whitespace-pre-wrap break-words">{task || "Loading..."}</pre>
          </div>
        </div>
      </div>
      <div className="mx-[20px] mt-5 rounded bg-white">
        <Dragger {...uploadProps}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">Click or drag file to this area to upload</p>
          <p className="ant-upload-hint">
            Only zip files allowed 
          </p>
        </Dragger>
        <Button type="primary" onClick={handleUploadAnswer}>
          Submit
        </Button>
      </div>
    </div>
  );
}

export default DetailQuestion;
