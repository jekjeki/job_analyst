import { useRouter } from 'next/router'
import React, { useEffect, useRef, useState } from 'react'
import {gsap} from 'gsap'

function index() {
    const router = useRouter()
    const [datas, setDatas] = useState<any>({})
    const [predClick, setPredClick] = useState<any>({})
    const [topCourses, setTopCourses] = useState<any>([])
    const circleRefs = useRef<(HTMLDivElement|null)[]>([])

    useEffect(()=>{

        if(typeof window !== 'undefined' && datas['predicted_job']){
            circleRefs.current.forEach((circle, idx)=>{
                if(circle){
                    gsap.to(circle, {duration:5, x:100, rotation:360, ease: 'power3.out'})
                }
            })
        }
        
        // mengambil data dari local storage 
        let dataObj = localStorage.getItem("objData")
        
        // melakukan valiasi obj data 
        if(dataObj){
            let dataObjNew = JSON.parse(dataObj)
            console.log(dataObjNew)
            console.log(dataObjNew['predicted_job'][0])
            setPredClick(dataObjNew['predicted_job'][0])
            setDatas(dataObjNew)

            console.log(Object.keys(dataObjNew['top_5_courses']))
        }
    }, [])

  return (
    <div className='bg-indigo-700 min-h-screen'>
        <div className='flex justify-center'>
            <div className='w-3/4 rounded min-h-44 bg-white mt-[30px]'>
                <h3 className='font-bold text-xl text-center'>Summarize of your CV data</h3>
                <div className='flex text-xl mt-5'>
                    <p className='ml-[10px]'>Current work: </p>
                    <p className='mx-1 font-bold'>{datas['curr_work']}</p>
                </div>
                <div className='flex text-xl mt-5'>
                    <div className='ml-[10px]'>
                        <p>Database Skills:</p>
                    </div>
                    <div className='mx-2 font-bold'>
                        <ul className='flex flex-wrap'>
                            {
                                (datas['database_skills'] ? datas['database_skills'].map((ds:string, idx:number)=>(
                                    <li className='mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {ds}
                                    </li> 
                                )) : <p>Null</p> )
                            }
                        </ul>
                    </div>
                </div>
                {/* framework skills */}
                <div className='flex text-xl mt-5'>
                    <div className='ml-[10px]'>
                        <p>Framework Skills: </p>
                    </div>
                    <div className='mx-2 font-bold'>
                        <ul className='flex flex-wrap'>
                            {
                                datas['framework_skills'] ? datas['framework_skills']?.map((fs:string, idx:number)=>(
                                    <li className='mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {fs}
                                    </li>
                                )) : <p>Null</p>
                            }
                        </ul>
                    </div>
                </div>
                {/* number of projects */}
                <div className='flex text-xl mt-5'>
                    <div className='ml-[10px]'>
                            <p>Projects: </p>
                    </div>
                    <div className='mx-2 font-bold'>
                        <ul className='flex flex-wrap'>
                            {
                                datas['number_of_projects'] ? datas['number_of_projects']?.map((nop:string, idx:number)=>(
                                    <li className='mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {nop}
                                    </li>
                                )) : <>Null</>
                            }
                        </ul>
                    </div>
                </div>
                {/* programming language */}
                <div className='flex text-xl mt-5'>
                    <div className='ml-[10px]'>
                            <p>Programming Language: </p>
                    </div>
                    <div className='mx-2 font-bold'>
                        <ul className='flex flex-wrap'>
                            {
                                datas['programming_language'] ? datas['programming_language']?.map((pl:string, idx:number)=>(
                                    <li className='mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {pl}
                                    </li>
                                )) : <>Null</>
                            }
                        </ul>
                    </div>
                </div>
                {/* Tools skills */}
                <div className='flex text-xl mt-5'>
                    <div className='ml-[10px]'>
                        <p>Tools Skills: </p>
                    </div>
                    <div className='mx-2'>
                        <ul className='font-bold flex flex-wrap'>
                            {
                                datas['tools_skills'] ? datas['tools_skills']?.map((ts:string, idx:number)=>(
                                    <li className='my-1 mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {ts}
                                    </li>
                                )) : <>Null</>
                            }
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div className='flex justify-center'>
            <div className='w-3/4'>
                {/* predicted job and list of courses */}
                <div className='rounded bg-white my-[30px]'>
                    <div className='text-center font-bold text-xl'>
                        <p>Results</p>
                    </div>
                </div>
                    {/* predicted job */}
                    <div className='text-xl'>
                        <div className='text-center my-2 text-white font-bold'>
                            <p>Predicted Job:</p>
                        </div>
                        <div className='flex justify-center'>
                            {
                                datas['predicted_job'] ? datas['predicted_job']?.map((pj:any, idx:number)=>(
                                    <div onClick={()=>{
                                        setTopCourses(datas['top_5_courses'][datas['predicted_job'][idx].job])
                                        setPredClick(datas['predicted_job'][idx])
                                        }} className='mx-2 font-bold bg-white w-1/3 h-[200px] rounded' key={idx}>
                                        <p className='rounded-md px-2 text-center my-2'>{pj['job']}</p>
                                        <div className='flex items-center h-3/4'>
                                            <div 
                                            ref={(el) => {
                                                circleRefs.current[idx] = el
                                            }} 
                                            className='w-[120px] h-[120px] bg-gradient-to-r from-green-300 to-green-600 rounded-full flex justify-center items-center'>
                                                <p>{Math.round(pj['prob']*100)+'%'}</p>
                                            </div>
                                        </div>
                                    </div>
                                )) : <>Null</>
                            }
                        </div>
                    </div>
                    {/* description */}
                    <div className='flex flex-wrap ml-[10px] mt-[20px] text-xl'>
                        <div>
                            <p>Description:</p>
                        </div>
                        <div className='font-bold'>
                            <p>{predClick['description']}</p>
                        </div>
                    </div>
                    {/* top 5 courses */}
                    <div className='text-xl mt-[20px]'>
                        <div className='mx-[10px]'>
                            <p>Recommended Courses: </p>
                        </div>
                        {/* list of courses */}
                        <div className='px-3'>
                            {
                               
                                topCourses?.map((tc:any, idx:number)=>( 
                                    <div className='hover:[border-black border-2 border-solid] min-h-[100px] rounded mt-2 shadow-md mx-3' key={idx}>
                                        <div 
                                        className='m-5 font-bold'>
                                            <p className=''>{tc}</p>
                                        </div>
                                        <button
                                            onClick={()=>router.push({
                                                pathname: `question/${tc}`
                                            })}
                                        className='m-5 bg-sky-700 p-3 text-white font-bold rounded'>Detail</button>
                                    </div>
                                ))
                            }
                        </div>
                    </div>
            </div>
        </div>
    </div>
  )
}

export default index