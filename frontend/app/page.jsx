'use client'

import { useEffect, useState } from 'react';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '@/app/firebase/config';
import { useRouter } from 'next/navigation';
import { signOut } from 'firebase/auth';


export default function Home() {
  const [user] = useAuthState(auth);
  const [userSession, setUserSession] = useState(null);
  const router = useRouter();

  useEffect(() => {
    // Check if we're running on the client side
    if (typeof window !== 'undefined') {
      const session = sessionStorage.getItem('user');
      setUserSession(session);
    }
  }, []);

  useEffect(() => {
    if (!user && !userSession) {
      router.push('/sign-up');
    }
  }, [user, userSession, router]);

  const handleLogout = () => {
    signOut(auth).then(() => {
      sessionStorage.removeItem('user');
      router.push('/sign-in');
    });
  };

  if (!user && !userSession) {
    return null; 
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <button onClick={handleLogout} className="p-2 bg-red-500 text-white rounded">
        Log out
      </button>
      <page/>
    </main>
  );
}
