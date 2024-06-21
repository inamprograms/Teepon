"use client";

import ChatLayout from "@/components/ChatLayout";
import ProtectedRoute from "@/components/ProtectedRoute";
import React, { useState } from "react";
import style from "./new.module.css";

const page = () => {
  const [page, setPage] = useState(1);
  const [name, setName] = useState('');
  const [friends, setFriends] = useState([]);

  return (
    // <ProtectedRoute>
      <ChatLayout>
        <div className="flex items-center justify-center bg-slate-200 h-screen">
          <div className={style.page}>
            <h1 className="text-xl mx-6 my-3">Create a new Outing</h1>

            {page === 1 ? (
              <input
                className={style.input}
                type="text"
                placeholder="Enter the name of the outing"
                value={name}
                onChange={(e)=>{setName(e.target.value)}}
              />
            ) : page === 2 ? (
              <select
                className={style.input}
                onChange={(e)=>{setName(e.target.value)}}
              >
                <option value="" selected hidden disabled>Enter IDs of your friends</option>
                <option>Hello</option>
                <option>Hello2</option>
              </select>
            ) : page === 3 ? (
              ""
            ) : 'Congrats'}

            <button className="m-auto me-6 mb-3 flex items-center justify-center px-4 py-2 bg-black text-white rounded-lg" onClick={()=>{setPage(page+1)}} >
              Next
            </button>
          </div>
        </div>
      </ChatLayout>
    // </ProtectedRoute>
  );
};

export default page;
