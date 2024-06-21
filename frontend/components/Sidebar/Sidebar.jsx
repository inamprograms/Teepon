import React, { useState } from 'react';
import { IoMdClose } from "react-icons/io";
import { FiSearch, FiPlus } from "react-icons/fi";

const Sidebar = ({ hamburg, setHamburg, onRoomSelect }) => {
  const [searchInput, setSearchInput] = useState(''); // State to track search input
  const outings = [
    { name: 'Outing-1', desc: 'Weekend party near the hills' },
    { name: 'Outing-2', desc: 'Weekend party near the hills' },
    { name: 'Outing-3', desc: 'Weekend party near the hills' },
    { name: 'Outing-4', desc: 'Weekend party near the hills' },
    { name: 'Outing-5', desc: 'Weekend party near the hills' },
    { name: 'Outing-6', desc: 'Weekend party near the hills' },
    { name: 'Outing-7', desc: 'Weekend party near the hills' },
    { name: 'Outing-8', desc: 'Weekend party near the hills' },
    { name: 'Outing-9', desc: 'Weekend party near the hills' },
    { name: 'Outing-10', desc: 'Weekend party near the hills' },
  ];

  const handleRoomClick = (roomName) => {
    onRoomSelect(roomName);
    setHamburg(false);
  };

  const handleSearchChange = (e) => {
    setSearchInput(e.target.value);
  };

  const filteredOutings = outings.filter((outing) =>
    outing.name.toLowerCase().includes(searchInput.toLowerCase())
  );

  return (
    <div className={`fixed md:static top-0 left-0 h-full md:w-80 w-screen max-w-md bg-white border-r border-gray-400 transition-transform transform ${hamburg ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0`}>
      <div className="absolute top-4 right-4 text-3xl cursor-pointer md:hidden" onClick={() => setHamburg(false)}>
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
          <div className="w-12 h-12 bg-gray-300 rounded-full"></div>
          <button className="flex items-center justify-center px-4 py-2 bg-black text-white rounded-lg">
            <FiPlus className="mr-2" /> New
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
