
import React, { createContext, useContext, useEffect, useState } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '@/services/firebase/config';
import { useDispatch } from 'react-redux';
import { setUser, clearUser } from '@/store/ChatSlice';
import Loader from '@/components/Loader';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [loading, setLoading] = useState(true);
  const dispatch = useDispatch();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => { 
      if (user) {
        dispatch(setUser(user.uid));
      } else {
        dispatch(clearUser());
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, [dispatch]);

  if (loading) {
    return <Loader/>;
  }

  return <AuthContext.Provider value={null}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
