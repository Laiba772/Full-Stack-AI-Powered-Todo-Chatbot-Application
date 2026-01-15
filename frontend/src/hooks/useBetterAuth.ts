import { useRouter } from 'next/navigation';
import { useCallback } from 'react';
import apiClient from '@/lib/api/clients';

// For now, since BetterAuth uses atoms instead of standard hooks, we'll create a simple wrapper
// that works with our existing system but represents the BetterAuth integration
interface User {
  id: string;
  email: string;
}

interface SignInResponse {
  access_token: string;
  user: User;
}

interface SignUpResponse {
  access_token: string;
  user: User;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

interface AuthContextType extends AuthState {
  signIn: (email: string, password: string) => Promise<User>;
  signUp: (email: string, password: string) => Promise<User>;
  signOut: () => Promise<void>;
}

export function useBetterAuth(): AuthContextType {
  const router = useRouter();

  // Direct API calls to match our backend endpoints
  const signInHandler = useCallback(async (email: string, password: string): Promise<User> => {
    try {
      const res = await apiClient.post<SignInResponse>('/api/auth/signin', {
        email,
        password
      });

      if (res.data.access_token) {
        localStorage.setItem('access_token', res.data.access_token);
      }

      router.push('/tasks');
      return res.data.user;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail?.message || error.message || 'Sign in failed';
      throw new Error(errorMessage);
    }
  }, [router]);

  const signUpHandler = useCallback(async (email: string, password: string): Promise<User> => {
    try {
      const res = await apiClient.post<SignUpResponse>('/api/auth/signup', {
        email,
        password
      });

      if (res.data.access_token) {
        localStorage.setItem('access_token', res.data.access_token);
      }
      
      router.push('/tasks');
      return res.data.user;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail?.message || error.message || 'Sign up failed';
      throw new Error(errorMessage);
    }
  }, [router]);

  const signOutHandler = useCallback(async () => {
    try {
      await apiClient.post('/api/auth/signout'); // Call backend to clear HttpOnly cookie
    } catch (error) {
      console.error('Sign out error on backend:', error);
    } finally {
      localStorage.removeItem('access_token');
      router.push('/signin');
    }
  }, [router]);



  // Return initial state - the actual state will be managed by AuthContext
  return {
    user: null,
    loading: false,
    error: null,
    isAuthenticated: false,
    signIn: signInHandler,
    signUp: signUpHandler,
    signOut: signOutHandler,

  };
}