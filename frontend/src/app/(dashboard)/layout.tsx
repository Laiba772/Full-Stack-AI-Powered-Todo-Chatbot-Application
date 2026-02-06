'use client';

import React from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { Button } from '@/components/ui/Button';
import Link from 'next/link';
import FloatingChat from '@/components/chat/FloatingChat';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, signOut } = useAuth();

  return (
    <div className="relative min-h-screen bg-linear-to-br from-gray-900 via-purple-900/10 to-black text-white overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-cyan-500/5 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        <div className="absolute top-1/3 right-1/3 w-64 h-64 bg-pink-500/5 rounded-full blur-3xl animate-pulse" style={{animationDelay: '4s'}}></div>
      </div>

      {/* Top navigation bar */}
      <header className="sticky top-0 z-20 bg-gray-900/80 backdrop-blur-md border-b border-gray-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-linear-to-r from-purple-600 to-cyan-500 rounded-lg flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h1 className="text-xl font-bold bg-clip-text text-transparent bg-linear-to-r from-purple-400 to-cyan-400">
                  <Link href="/">TaskWiz Dashboard</Link>
                </h1>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {user && (
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <div className="relative">
                      <div className="w-2 h-2 bg-green-500 rounded-full absolute top-0 right-0 ring-2 ring-gray-900"></div>
                      <div className="w-8 h-8 bg-linear-to-r from-purple-600 to-cyan-500 rounded-full flex items-center justify-center">
                        <span className="text-xs font-bold text-white">{user.name?.charAt(0) || user.email?.charAt(0)}</span>
                      </div>
                    </div>
                    <div className="hidden md:block">
                      <p className="text-sm font-medium text-white">{user.name || user.email?.split('@')[0]}</p>
                      <p className="text-xs text-gray-400">Member</p>
                    </div>
                  </div>
                  <Button
                    onClick={signOut}
                    className="bg-linear-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white
                    rounded-lg px-4 py-2 text-sm font-medium
                    hover:scale-105
                    hover:shadow-[0_0_15px_rgba(239,68,68,0.3)]
                    transition-all duration-300 flex items-center gap-2"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Sign Out
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Welcome message */}
      {user && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
          <div className="bg-linear-to-r from-purple-900/30 to-cyan-900/30 border border-purple-500/30 rounded-xl p-4 mb-6">
            <div className="flex items-center">
              <div className="mr-3 text-cyan-400">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.636 18.364a9 9 0 010-12.728m12.728 0a9 9 0 010 12.728m-9.9-2.528a1 1 0 00-.287-.801M15.262 6.603a1 1 0 00-.785-.286M7.072 17.397a1 1 0 00.286-.785M11.928 6.603a1 1 0 00-.286-.785" />
                </svg>
              </div>
              <div>
                <h2 className="text-lg font-semibold">Welcome back, {user.name || user.email?.split('@')[0]}!</h2>
                <p className="text-gray-400 text-sm">We're glad to see you again. Ready to tackle your tasks today?</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 relative z-10">
        {children}
      </main>

      {/* Floating Chat Button */}
      <FloatingChat />
    </div>
  );
}
