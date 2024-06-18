import React, { useRef, useEffect } from 'react';

const ChatWindow = ({ messages }) => {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Automatically scroll to the bottom when new messages are added
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className='w-full overflow-x-auto'>
      <div className='chat-content bg-transparent p-4 rounded-lg shadow-lg'>
        <div className='flex flex-col gap-2'>
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} items-start gap-2`}
            >
              {message.sender === 'bot' && (
                <div className="flex items-center gap-2 justify-start">
                    <img src='errre' alt="Chatbot" className="w-8 h-8 rounded-full" />
                  <div className={`p-2 max-w-xs bg-black text-white rounded-br-none rounded-lg break-words`}>
                    {message.text}
                  </div>
                
                </div>
              )}
              {message.sender === 'user' && (
                <div className="flex items-center gap-2 justify-start">
                 
                  <div className={`p-2 max-w-xs bg-black text-white rounded-br-none rounded-lg break-words`}>
                    {message.text}
                  </div>
                </div>
              )}
            </div>
          ))}
          {/* Ref for scrolling to bottom */}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
