"use client";

import React, { useState, useEffect } from 'react'
import Sidebar from '@/components/Sidebar/Sidebar'
import { RxHamburgerMenu } from "react-icons/rx";
import { IoSend } from "react-icons/io5";
import ChatWindow from '@/components/Sidebar/chatWindow';
import { connectSocket, disconnectSocket, sendMessage, subscribeToMessages } from '../services/socketService';
const Index = () => {
  const [hamburg, setHamburg] = useState(true);
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');

  useEffect(() => {
    connectSocket();

    // Clean up socket connection on unmount
    return () => {
      disconnectSocket();
    };
  }, []);

  useEffect(() => {
    subscribeToMessages((message) => {
      setMessages([...messages, message]);
    });
  }, [messages]);

  const handleSendMessage = () => {
    if (messageInput.trim() === '') return;

    sendMessage({ text: messageInput, sender: 'user' });
    setMessages([...messages, { text: messageInput, sender: 'user' }]);
    setMessageInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const handleInputChange = (e) => {
    setMessageInput(e.target.value);
  };

  return (
    <>
      <section className="h-screen flex">
        <Sidebar hamburg={hamburg} setHamburg={setHamburg} />
        <div className="flex-1 flex flex-col">
          <header className="bg-gray-800 text-white p-4 flex justify-between items-center">
            {!hamburg && (
              <RxHamburgerMenu
                className="text-3xl cursor-pointer md:hidden"
                onClick={() => setHamburg(true)}
              />
            )}
            <div>Top</div>
          </header>
          <main className="flex-1 overflow-y-auto flex flex-col-reverse bg-gray-100 p-4">
            <ChatWindow messages={messages} />
          </main>
          <footer className="  p-4 flex items-center">
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
              onClick={handleSendMessage}
            >
              <IoSend />
            </button>
          </footer>
        </div>
      </section>
    </>
  );
};

export default Index;