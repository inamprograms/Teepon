import React from 'react'
import style from './sidebar.module.css'
import { IoMdClose } from "react-icons/io";
import { FiSearch, FiPlus } from "react-icons/fi";

const Sidebar = ({hamburg, setHamburg}) => {

  const outings = [
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    },
    {
      'name' : 'Weekend Outings',
      'desc' : 'Weekend party near the hills'
    }
    
  ]

  return (
    <div className={`${style.sidebar} ${!hamburg ? style.hide : ''}`}>
      <div className={style.close} onClick={()=>{setHamburg(false)}}><IoMdClose /></div>
      <div className={style.upper_dock}>
        <h1 className={style.outings}>Outings</h1>
        <div className={style.searchbar}>
          <FiSearch className={style.search_icon}/>
          <input type="text" name="search" id="search" className={style.input} placeholder='Search' />
        </div>
      </div>

      <div className={style.middle_dock}>
        <ul className={style.outings}>
          {outings.map((item)=>{
            return <li className={style.outing}>
              <div className={style.title}>{item.name}</div>
              <div className={style.desc}>{item.desc}</div>
            </li>
          })}
        </ul>
      </div>


      <div className={style.lower_dock}>
        <div className={style.profile}></div>
        <button className={style.new}>
          <FiPlus className={style.svg}/> New
        </button>
      </div>
    </div>
  )
}

export default Sidebar