"use client";

import React, { useState } from 'react'
import Sidebar from '@/components/Sidebar/Sidebar'
import { RxHamburgerMenu } from "react-icons/rx";
import style from './chat.module.css'

const index = () => {

  const [hamburg, setHamburg] = useState(false)

  return (
    <>
    <Sidebar hamburg={hamburg} setHamburg={setHamburg} />
    <div className={style.hamburg}>{!hamburg?<RxHamburgerMenu onClick={() => setHamburg(!hamburg)} />:''}</div>
    
    </>
  )
}

export default index