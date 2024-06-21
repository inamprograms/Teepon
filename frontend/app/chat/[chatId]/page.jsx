'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { useSelector, useDispatch } from 'react-redux';
import { connectSocket, disconnectSocket, sendMessage, joinRoom } from '@/services/socketService';
import { setCurrentRoom } from '@/store/ChatSlice';
import { IoSend } from 'react-icons/io5';
import ChatWindow from '@/components/ChatWindow';
import ProtectedRoute from '@/components/ProtectedRoute';
import ChatLayout from '@/components/ChatLayout';

const ChatRoom = () => {
  const { chatId } = useParams(); // use useParams to get the dynamic route parameter
 
  const [messageInput, setMessageInput] = useState('');
  const messages = useSelector((state) => state.chat.messages);
  const currentRoom = useSelector((state) => state.chat.currentRoom);
  const dispatch = useDispatch();
  const currentuser = useSelector((state) => state.chat.user);

  useEffect(() => {
    connectSocket();
    if (chatId) {
      handleJoin(chatId);
    }

    return () => {
      disconnectSocket();
    };
  }, [chatId]);

  const handleJoin = (roomName) => {
    joinRoom(roomName);
    dispatch(setCurrentRoom(roomName));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(messageInput, currentRoom, currentuser);
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

  return (
    <ProtectedRoute>
      <ChatLayout>
        {currentRoom && (
          <>
            <header className="bg-gray-200 text-white p-4 flex justify-between items-center">
              <div className="text-lg pl-10 text-black">{currentRoom}</div>
            </header>
            <main className="flex-1 overflow-y-auto flex flex-col-reverse bg-gray-100 p-4">
              <ChatWindow messages={messages} />
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
      </ChatLayout>
    </ProtectedRoute>
  );
};

export default ChatRoom;
