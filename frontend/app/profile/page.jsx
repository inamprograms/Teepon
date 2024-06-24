'use client';
import React, { useState } from 'react'; // Import useState for state management
import { MdKeyboardArrowLeft } from 'react-icons/md'; // Import React icons
import { useRouter } from 'next/navigation'; // Import useRouter for navigation
import CustomInput from '@/components/common/CustomInput'; // Import your custom input component
import { FaUserEdit } from "react-icons/fa";
import { FaSave } from "react-icons/fa";

const Profile = () => {
  const router = useRouter();
  const [editMode, setEditMode] = useState(false); // State for edit mode
  const [name, setName] = useState('John Doe'); // Example name
  const [userId, setUserId] = useState('ghostfreak123'); // Example user ID
  const [email, setEmail] = useState('johndoe@example.com'); // Example email
  const [link, setLink] = useState('https://example.com'); // Example link
  const [bio, setBio] = useState('Frontend Developer'); // Example bio

  const handleEditToggle = () => {
    setEditMode(!editMode);
  };

  return (
    <section className="bg-slate-200 h-screen w-full flex flex-col justify-between">
      <header className="flex items-center w-full bg-gray-100 rounded-t-lg p-4">
        <MdKeyboardArrowLeft
          className="my-5 text-3xl ms-3 cursor-pointer"
          onClick={() => {
            router.back();
          }}
        />
        <span className="text-xl my-5 mx-auto">Profile</span>
      </header>

      <main className="m-auto flex flex-col gap-4 p-4">
        <span className="text-4xl font-bold text-center my-4">P</span>

        {/* Name Input */}
        <CustomInput
          inputType="text"
          label="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={!editMode}
        />

        {/* User ID Input (Disabled) */}
        <CustomInput
          inputType="text"
          label="UserID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          disabled
        />

        {/* Email Input */}
        <CustomInput
          inputType="email"
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={!editMode}
        />

        {/* Link Input */}
        <CustomInput
          inputType="text"
          label="Link"
          value={link}
          onChange={(e) => setLink(e.target.value)}
          disabled={!editMode}
        />

        {/* Bio Input (Textarea) */}
        <CustomInput
          inputType="text"
          label="Bio"
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          disabled={!editMode}
        />
      </main>

      {/* Edit/Save Button */}
      <footer className="flex justify-end text-4xl p-5">
        <button onClick={handleEditToggle}>{editMode ? ( <FaSave />) : (<FaUserEdit  />)}</button>
      
      </footer>
   
     
    </section>
  );
};

export default Profile;
