'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar/Sidebar';
import { RxHamburgerMenu } from 'react-icons/rx';
import { IoSend } from 'react-icons/io5';
import ChatWindow from '@/components/ChatWindow';
import { useSelector, useDispatch } from 'react-redux';
import { connectSocket, disconnectSocket, sendMessage, joinRoom } from '@/services/socketService';
import { setCurrentRoom } from '@/store/ChatSlice';
import ProtectedRoute from '@/components/ProtectedRoute';

const Index = () => {
  const [hamburg, setHamburg] = useState(true);
  const [messageInput, setMessageInput] = useState('');
  const messages = useSelector((state) => state.chat.messages);
  const currentRoom = useSelector((state) => state.chat.currentRoom);
  const dispatch = useDispatch();
  const currentuser = useSelector((state) => state.chat.user);
  useEffect(() => {
    connectSocket();

    return () => {
      disconnectSocket();
    };
  }, []);

  const handleJoin = (roomName) => {
    joinRoom(roomName);
    dispatch(setCurrentRoom(roomName));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(messageInput, currentRoom, currentuser);
    console.log('user in chat',currentuser)
    setMessageInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  const handleInputChange = (e) => {
    setMessageInput(e.target.value);
  };

  const handleRoomSelect = (roomName) => {
    handleJoin(roomName);
  };

  return (
    <ProtectedRoute>
      <section className="h-screen flex">
        <Sidebar hamburg={hamburg} setHamburg={setHamburg} onRoomSelect={handleRoomSelect} />
        <div className="flex-1 flex flex-col">
          {currentRoom && (
            <>
              <header className="bg-gray-800 text-white p-4 flex justify-between items-center">
                {!hamburg && (
                  <RxHamburgerMenu
                    className="text-3xl cursor-pointer md:hidden"
                    onClick={() => setHamburg(true)}
                  />
                )}
                <div>{currentRoom}</div> {/* Display current room */}
              </header>
              <main className="flex-1 overflow-y-auto flex flex-col-reverse bg-gray-100 p-4">
                <ChatWindow messages={messages}  />
              </main>
              <footer className="p-4 flex items-center">
                <input
                  className="flex-1 p-2 border border-gray-400 rounded focus:outline-none"
                  style={{ background: 'none', resize: 'none', minHeight: '40px' }}
                  placeholder="Type your message..."
                  value={messageInput}
                  onChange={handleInputChange}
                  onKeyPress={handleKeyPress}
                />
                <button
                  className="ml-2 px-4 py-2 bg-black text-white rounded-lg"
                  onClick={handleSubmit}
                >
                  <IoSend />
                </button>
              </footer>
            </>
          )}
        </div>
      </section>
    </ProtectedRoute>
  );
};

export default Index;
