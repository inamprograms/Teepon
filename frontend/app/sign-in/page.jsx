'use client';

import { useState } from 'react';
import { useSignInWithEmailAndPassword } from 'react-firebase-hooks/auth';
import { auth, googleProvider } from '@/services/firebase/config';
import { useRouter } from 'next/navigation';
import { FcGoogle } from 'react-icons/fc';
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [signInWithEmailAndPassword, user, loading, error] = useSignInWithEmailAndPassword(auth);
  const router = useRouter();

  const handleSignIn = async () => {
    try {
      const res = await signInWithEmailAndPassword(email, password);
      if (res) {
        console.log({ res });
        sessionStorage.setItem('user', true);
        setEmail('');
        setPassword('');
        router.push('/');
      } else {
        console.error('Authentication failed');
      }
    } catch (e) {
      console.error('Sign-in error:', e);
    }
  };

  const handleGoogleSignIn = async () => {
    try {
      const provider = new GoogleAuthProvider()
      provider.addScope('https://www.googleapis.com/auth/calendar.events.readonly')
      const res = await signInWithPopup(auth, provider)
      .then((result) => {
        // This gives you a Google Access Token. You can use it to access the Google API.
        const credential = GoogleAuthProvider.credentialFromResult(result);
        console.log(credential);
      })
      if (res) {
        console.log({ res });
        sessionStorage.setItem('user', true);
        router.push('/');
      } else {
        console.error('Google authentication failed');
      }
    } catch (e) {
      console.error('Google sign-in error:', e);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-10 rounded-lg shadow-xl w-96">
        <h1 className="text-white text-2xl mb-5">Sign In</h1>
        {error && <p className="text-red-500 mb-5">{error.message}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-3 mb-4 bg-gray-700 rounded outline-none text-white placeholder-gray-500"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 mb-4 bg-gray-700 rounded outline-none text-white placeholder-gray-500"
        />
        <div className='flex gap-4 mb-4'>
          <button
            onClick={handleSignIn}
            className="w-full p-3 bg-indigo-600 rounded text-white hover:bg-indigo-500"
          >
            Sign In
          </button>
          <button
            onClick={() => router.push('/sign-up')}
            className="w-full p-3 bg-indigo-600 rounded text-white hover:bg-indigo-500"
          >
            Sign Up
          </button>
        </div>
        <button
          onClick={handleGoogleSignIn}
          className="w-full p-3 bg-white rounded text-gray-700 hover:bg-gray-200 flex items-center justify-center gap-2"
        >
          <FcGoogle size={24} />
          Sign in with Google
        </button>
      </div>
    </div>
  );
};

export default SignIn;
