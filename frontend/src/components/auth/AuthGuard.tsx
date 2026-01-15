'use client';

import { useAuth } from '@/context/AuthContext';
import { usePathname, redirect } from 'next/navigation';
import { useEffect } from 'react';

const protectedRoutes = ['/tasks'];
const authRoutes = ['/signin', '/signup'];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth();
  const pathname = usePathname();

  useEffect(() => {
    if (!loading) {
      const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route));
      const isAuthRoute = authRoutes.includes(pathname);

      if (isProtectedRoute && !isAuthenticated) {
        redirect('/signin');
      }

      if (isAuthRoute && isAuthenticated) {
        redirect('/tasks');
      }
    }
  }, [isAuthenticated, loading, pathname]);

  if (loading) {
    return <div>Loading...</div>; // Or a proper spinner component
  }

  return <>{children}</>;
}
