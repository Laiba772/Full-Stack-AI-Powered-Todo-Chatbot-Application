// T022: Middleware for route protection

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // This middleware now only handles redirecting authenticated users away from auth pages.
  // Route protection for `/tasks` is now handled client-side by `AuthContext`.
  
  const token = request.cookies.get('access_token')?.value ||
                request.headers.get('authorization')?.replace('Bearer ', '');

  // If on signin/signup page and has token, redirect to tasks
  const isAuthRoute = request.nextUrl.pathname.startsWith('/signin') ||
                      request.nextUrl.pathname.startsWith('/signup');

  if (isAuthRoute && token) {
    const tasksUrl = new URL('/tasks', request.url);
    return NextResponse.redirect(tasksUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/signin', '/signup'],
};
