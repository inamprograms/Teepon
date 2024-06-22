"use client";
import ProtectedRoute from "@/components/ProtectedRoute";
import React from "react";
import style from "./profile.module.css";
import { MdKeyboardArrowLeft } from "react-icons/md";
import { useRouter } from "next/navigation";

const page = () => {
  const router = useRouter();

  return (
    <ProtectedRoute>
      <div className="flex bg-slate-200 w-screen h-screen">
        <div className={`bg-white m-auto flex ${style.window}`}>
          <div className={`${style.topbar} flex items-center`}>
            <MdKeyboardArrowLeft
              className="my-5 text-3xl ms-3 cursor-pointer"
              onClick={() => {
                router.back();
              }}
            />
            <span className="heading text-xl my-5 mx-auto pe-6">Profile</span>
          </div>

          <div className={`content m-auto flex flex-col ${style.form}`}>
            <span className={style.img}>P</span>
            <div>
              <label htmlFor="">Name</label>
              <input type="text" />
            </div>
            <div>
              <label htmlFor="">User ID</label>
              <input type="text" disabled value="ghostfreak123" />
            </div>
            <div>
              <label htmlFor="">Email</label>
              <input type="email" name="email" id="email" />
            </div>
            {/* More info */}
          </div>

          <button
            className="m-auto me-6 mb-6 flex items-center justify-center px-4 py-2 bg-black text-white rounded-lg"
            onClick={() => {
              setPage(page + 1);
            }}
          >
            Edit
          </button>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default page;
