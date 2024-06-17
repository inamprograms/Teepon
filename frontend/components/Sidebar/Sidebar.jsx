import React from 'react'
import style from './sidebar.module.css'
import { IoMdClose } from "react-icons/io";

const Sidebar = ({hamburg, setHamburg}) => {
  return (
    <div className={`${style.sidebar} ${!hamburg ? style.hide : ''}`}>
      <div className={style.close} onClick={()=>{setHamburg(false)}}><IoMdClose /></div>
    </div>
  )
}

export default Sidebar