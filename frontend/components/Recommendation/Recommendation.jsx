import React from 'react'
import style from './recommend.module.css'

const Recommendation = () => {
  return (
    <div className={style.recommend}>
        <div className='heading text-xl'>Recommended Outings</div>
        <div className={style.outing}>
            <div className="title text-xl">Lorem ipsum dolor sit amet.</div>
            <div className="time px-2">24.06.2024 - 28.06.2024</div>
            <div className="desc px-2">Lorem ipsum dolor sit, amet consectetur adipisicing elit.</div>
        </div>
    </div>
  )
}

export default Recommendation