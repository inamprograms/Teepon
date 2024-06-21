import React, { useState } from 'react';
import Sidebar from '@/components/Sidebar/Sidebar';

const ChatLayout = ({ children }) => {
  const [hamburg, setHamburg] = useState(true);

  return (
    <section className="h-screen flex">
      <Sidebar hamburg={hamburg} setHamburg={setHamburg} />
      <div className="flex-1 flex flex-col">
        {children}
      </div>
    </section>
  );
};

export default ChatLayout;