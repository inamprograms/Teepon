'use client';

import React from 'react';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '@/services/firebase/config';
import { useRouter } from 'next/navigation'; // Correct hook for App Router
import { signOut } from 'firebase/auth';

import ProtectedRoute from '@/components/ProtectedRoute';

const Home = () => {
  const [user] = useAuthState(auth);
  const router = useRouter();

  const handleLogout = () => {
    signOut(auth).then(() => {
      sessionStorage.removeItem('user');
      router.push('/sign-in');
    });
  };

  return (
    <ProtectedRoute>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <button onClick={handleLogout} className="p-2 bg-red-500 text-white rounded">
          Log out
        </button>
      
        <page />
      </main>
    </ProtectedRoute>
  );
};

export default Home;
