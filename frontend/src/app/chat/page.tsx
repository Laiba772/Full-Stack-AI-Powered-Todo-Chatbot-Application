"use client";

import ChatWindow from "@/components/chat/ChatWindow";
import { useAuth } from "@/context/AuthContext";
import React from "react";

export default function ChatPage() {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white">
        Please sign in to access the chat.
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
      <div className="w-full max-w-2xl bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <ChatWindow />
      </div>
    </div>
  );
}
