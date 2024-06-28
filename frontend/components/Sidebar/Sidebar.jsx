import React, { useState } from "react";
import { IoMdClose } from "react-icons/io";
import { FiSearch, FiPlus } from "react-icons/fi";
import { useRouter } from "next/navigation";
import { useDispatch, useSelector } from "react-redux";
import {
  setCurrentRoom,
  setCurrentMessages,
  server_url,
} from "@/store/ChatSlice";
const Sidebar = ({ hamburg, setHamburg }) => {
  const [searchInput, setSearchInput] = useState("");
  const router = useRouter();
  const messages = useSelector((state) => state.chat.messages);
  const dispatch = useDispatch();
  const server_url = useSelector((state) => state.chat.server_url);
  const userdata = useSelector((state) => state.chat.userdata);
  const outings = [
    { name: "Outing-1", desc: "Weekend party near the hills" },
    { name: "Outing-2", desc: "Weekend party near the hills" },
    { name: "Outing-3", desc: "Weekend party near the hills" },
    { name: "Outing-4", desc: "Weekend party near the hills" },
    { name: "Outing-5", desc: "Weekend party near the hills" },
    { name: "Outing-6", desc: "Weekend party near the hills" },
    { name: "Outing-7", desc: "Weekend party near the hills" },
    { name: "Outing-8", desc: "Weekend party near the hills" },
    { name: "Outing-9", desc: "Weekend party near the hills" },
    { name: "Outing-10", desc: "Weekend party near the hills" },
  ];

  const handleRoomClick = async (roomName) => {
    // const data = [
    //   { message: 'Hello', sender: 'user' },
    //   { message: 'Hi', sender: 'friend' },
    // ];

    console.log(messages);
    // post message

    const data = await fetch(`${server_url}/chats`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        oid: roomName,
      }),
    })
      .then((res) => res.json())
      .then((e) => {dispatch(setCurrentMessages(e)); console.log(e);});

    setHamburg(false);
    dispatch(setCurrentRoom(roomName));

    router.push(`/chat/${roomName}`);
  };

  const handleSearchChange = (e) => {
    setSearchInput(e.target.value);
  };

  const filteredOutings = outings.filter((outing) =>
    outing.name.toLowerCase().includes(searchInput.toLowerCase())
  );
  const photoURL = userdata?.photoURL || 'default-image-url.jpg';
  return (
    <div
      className={`fixed md:static top-0 left-0 h-full z-10 md:w-80 w-screen max-w-md bg-white border-r border-gray-400 transition-transform transform ${
        hamburg ? "translate-x-0" : "-translate-x-full"
      } md:translate-x-0`}
    >
      <div
        className="absolute top-4 right-4 text-3xl cursor-pointer md:hidden"
        onClick={() => setHamburg(false)}
      >
        <IoMdClose />
      </div>
      <div className="flex flex-col h-full">
        <div className="p-6 border-b border-gray-400">
          <h1 className="text-xl mb-4">Outings</h1>
          <div className="flex items-center border border-gray-400 rounded-lg overflow-hidden">
            <FiSearch className="w-6 h-6 mx-2 text-gray-500" />
            <input
              type="text"
              className="flex-1 p-2 focus:outline-none"
              placeholder="Search"
              value={searchInput}
              onChange={handleSearchChange}
            />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-6">
          <ul className="space-y-4">
            {filteredOutings.map((item, index) => (
              <li
                key={index}
                className="p-4 bg-gray-100 rounded-lg shadow cursor-pointer"
                onClick={() => handleRoomClick(item.name)}
              >
                <div className="text-lg">{item.name}</div>
                <div className="text-gray-600">{item.desc}</div>
              </li>
            ))}
          </ul>
        </div>
        <div className="p-6 border-t border-gray-400 flex items-center justify-between bg-white">
        <div
            className="w-12 h-12 bg-gray-300 rounded-full bg-cover bg-center"
            style={{ backgroundImage: `url(${photoURL})` }}
            onClick={() => {
              router.push("/profile");
            }}
          ></div>
          <button
            className="flex items-center justify-center px-4 py-2 bg-black text-white rounded-lg"
            onClick={() => {
              router.push("/chat/new");
            }}
          >
            <FiPlus className="mr-2" /> New
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
