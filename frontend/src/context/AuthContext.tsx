'use client';

import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { redirect } from 'next/navigation';
import { User, AuthState, AuthContextType } from '@/types/auth';
import { useBetterAuth } from '@/hooks/useBetterAuth';
import apiClient from '@/lib/api/clients';

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthContextProvider({ children }: { children: React.ReactNode }) {
  const auth = useBetterAuth();
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    loading: true,
    error: null,
  });



  const signIn = async (email: string, password: string) => {
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const res = await auth.signIn(email, password);
      setState({
        user: { id: res.id, email: res.email },
        isAuthenticated: true,
        loading: false,
        error: null,
      });
    } catch (err: any) {
      setState(s => ({ ...s, loading: false, error: err.message }));
      throw err;
    }
  };

  // similar for signUp...
  const signUp = async (email: string, password: string) => {
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const res = await auth.signUp(email, password);
      setState({
        user: { id: res.id, email: res.email },
        isAuthenticated: true,
        loading: false,
        error: null,
      });
    } catch (err: any) {
      setState(s => ({ ...s, loading: false, error: err.message }));
      throw err;
    }
  };

  const signOut = async () => {
    try {
      await auth.signOut();
    } catch (err) {
      console.warn('SignOut failed on server', err);
    } finally {
      setState({
        user: null,
        isAuthenticated: false,
        loading: false,
        error: null,
      });
      redirect('/signin');
    }
  };

  return (
    <AuthContext.Provider
      value={{ ...state, signIn, signUp, signOut }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
};