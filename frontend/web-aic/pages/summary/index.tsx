import { useRouter } from 'next/router'
import React from 'react'

function index() {
    const router = useRouter()
    console.log(router.query.explanation_backend)
  return (
    <div className='bg-indigo-700 min-h-screen'>
        <div className='flex justify-center'>
            <div className='w-3/4 rounded min-h-44 bg-white mt-[30px]'>
                <h3 className='font-bold text-xl text-center'>Summarize of your CV data</h3>
                <div className='flex text-xl mt-5'>
                    <p className='ml-[10px]'>Current work: </p>
                    <p className='mx-1 font-bold'>{router.query.curr_work}</p>
                </div>
                <div className='flex text-xl mt-5'>
                    <div className='ml-[10px]'>
                        <p>Database Skills:</p>
                    </div>
                    <div className='mx-2 font-bold'>
                        <ul className='flex flex-wrap'>
                            {
                                (router.query.database_skills?.map((ds, idx)=>(
                                    <li className='mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {ds}
                                    </li>
                                )))
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
                                router.query.framework_skills?.map((fs, idx)=>(
                                    <li className='mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {fs}
                                    </li>
                                ))
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
                                router.query.number_of_projects?.map((nop, idx)=>(
                                    <li className='mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {nop}
                                    </li>
                                ))
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
                                router.query.programming_language?.map((pl, idx)=>(
                                    <li className='mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {pl}
                                    </li>
                                ))
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
                                router.query.tools_skills?.map((ts, idx)=>(
                                    <li className='my-1 mr-5 rounded-md px-2 bg-green-400' key={idx}>
                                        {ts}
                                    </li>
                                ))
                            }
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div className='flex justify-center'>
            {/* predicted job and list of courses */}
            <div className='w-3/4 rounded min-h-44 bg-white mt-[30px]'>
                <div className='text-center font-bold text-xl'>
                    <p>Results</p>
                </div>
                {/* predicted job */}
                <div className='flex text-xl'>
                    <div className='ml-[10px]'>
                        <p>Predicted Job:</p>
                    </div>
                    <div className='mx-2 font-bold'>
                        <p className='rounded-md px-2 bg-green-400'>{router.query.predicted_job}</p>
                    </div>
                </div>
                {/* description */}
                <div className='flex flex-wrap ml-[10px] mt-[20px] text-xl'>
                    <div>
                        <p>Description:</p>
                    </div>
                    <div className='font-bold'>
                        <p>{router.query.explanation_backend}</p>
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
                            router.query.top_5_courses?.map((tc, idx)=>(
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