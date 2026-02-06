'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import ChatWindow from './ChatWindow';

const FloatingChat = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const { user } = useAuth();

  // Set mounted state to avoid hydration issues
  useEffect(() => {
    setIsMounted(true);
    console.log("FloatingChat mounted, user:", user); // Debug log
  }, []);

  // Log user changes
  useEffect(() => {
    console.log("FloatingChat user changed:", user); // Debug log
  }, [user]);

  // Toggle chat window visibility
  const toggleChat = () => {
    if (!user) {
      alert('Please sign in to access the chat');
      return;
    }
    setIsOpen(!isOpen);
  };

  // Close chat when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const chatContainer = document.getElementById('floating-chat-container');
      if (isOpen && chatContainer && !chatContainer.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  if (!isMounted) {
    return null; // Don't render until mounted to avoid hydration issues
  }

  console.log("FloatingChat - user object:", user); // Debug log
  console.log("FloatingChat - isAuthenticated:", !!user); // Debug log

  if (!user) {
    console.log("FloatingChat - Hiding chat button, user not authenticated"); // Debug log
    return null; // Don't show chat button for non-authenticated users
  }

  console.log("FloatingChat - Showing chat button, user authenticated"); // Debug log

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-linear-to-r from-purple-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-purple-500/50 hover:shadow-purple-500/80 cursor-pointer transform transition-transform hover:scale-110 hover:shadow-xl"
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
      </button>

      {/* Floating Chat Window */}
      {isOpen && (
        <div 
          id="floating-chat-container"
          className="fixed bottom-20 right-6 z-50 w-80 h-96 bg-gray-800 rounded-lg shadow-xl border border-gray-700 flex flex-col"
        >
          <div className="flex justify-between items-center p-3 bg-gray-700 rounded-t-lg">
            <h3 className="font-semibold">AI Assistant</h3>
            <button 
              onClick={() => setIsOpen(false)}
              className="text-gray-300 hover:text-white"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
          <div className="grow overflow-hidden p-2">
            <ChatWindow />
          </div>
        </div>
      )}
    </>
  );
};

export default FloatingChat;