import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import apiClient from '../../lib/api/clients';

const ChatWindow = () => {
  const { user } = useAuth();

  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI assistant. How can I help you manage your tasks today? Try saying 'add a task', 'show my tasks', or 'complete a task'.", sender: 'ai', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (!user) {
    return (
      <div className="h-full flex items-center justify-center bg-linear-to-br from-gray-900 to-black rounded-xl">
        <div className="text-center">
          <div className="w-16 h-16 bg-linear-to-r from-purple-500 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M14 7h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <p className="text-gray-400 text-lg">Sign in to access the AI Assistant</p>
        </div>
      </div>
    );
  }

  interface Message {
    id: number;
    text: string;
    sender: 'user' | 'ai';
    time: string;
  }

  interface ChatResponse {
    response: string;
  }

  const handleSendMessage = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    if (!inputText.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: messages.length + 1,
      text: inputText,
      sender: 'user',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    try {
      // First, try to send to the backend AI processor
      const response = await apiClient.post<ChatResponse>(`/api/${user.id}/chat`, {
        message: inputText
      });

      if (response.status === 200) {
        const data = response.data;
        const aiMessage: Message = {
          id: messages.length + 2,
          text: data.response || "I processed your request successfully.",
          sender: 'ai',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        // If backend returns an error status, handle it
        const errorMessage: Message = {
          id: messages.length + 2,
          text: "Sorry, I couldn't process your request. Please try again.",
          sender: 'ai',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      // If there's a network error (like 404), fall back to simulated responses
      console.log("Backend unavailable, using simulated responses:", error instanceof Error ? error.message : String(error));

      // Process the user's request locally as a fallback
      const lowerCaseInput = inputText.toLowerCase();
      let responseText = '';

      if (lowerCaseInput.includes('hello') || lowerCaseInput.includes('hi') || lowerCaseInput.includes('hey')) {
        responseText = "Hello! How can I help you with your tasks today?";
      } else if (lowerCaseInput.includes('add') || lowerCaseInput.includes('create') || lowerCaseInput.includes('new task')) {
        responseText = "I would add a task if I was connected to the backend. The task would be saved to your list.";
      } else if (lowerCaseInput.includes('list') || lowerCaseInput.includes('show') || lowerCaseInput.includes('my tasks')) {
        responseText = "I would show your task list if I was connected to the backend. You would see all your tasks here.";
      } else if (lowerCaseInput.includes('complete') || lowerCaseInput.includes('done') || lowerCaseInput.includes('finish')) {
        responseText = "I would mark a task as complete if I was connected to the backend. The task status would be updated.";
      } else if (lowerCaseInput.includes('delete') || lowerCaseInput.includes('remove')) {
        responseText = "I would delete the task if I was connected to the backend. The task would be removed from your list.";
      } else if (lowerCaseInput.includes('update') || lowerCaseInput.includes('edit')) {
        responseText = "I would update the task if I was connected to the backend. The task details would be modified.";
      } else {
        responseText = `I received your message: "${inputText}". I'm currently working offline, but when connected I can help you manage your tasks.`;
      }

      const aiMessage: Message = {
        id: messages.length + 2,
        text: responseText,
        sender: 'ai',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-linear-to-br from-gray-900 to-black rounded-xl border border-gray-800 shadow-2xl shadow-purple-500/10 w-full max-w-xs sm:max-w-md">
      {/* Header */}
      <div className="bg-gray-800/50 backdrop-blur-sm px-4 py-3 border-b border-gray-700">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <h3 className="font-semibold text-white text-sm sm:text-base">AI Task Assistant</h3>
          <span className="ml-auto text-xs text-gray-400">Online</span>
        </div>
      </div>

      {/* Messages Container */}
      <div className="grow p-3 overflow-y-auto max-h-60 sm:max-h-80">
        <div className="space-y-3">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] sm:max-w-[80%] rounded-2xl px-3 py-2 sm:px-4 sm:py-3 text-sm ${
                  msg.sender === 'user'
                    ? 'bg-linear-to-r from-purple-600 to-cyan-600 text-white rounded-br-none'
                    : 'bg-gray-800 text-gray-100 rounded-bl-none'
                }`}
              >
                <pre className="whitespace-pre-wrap wrap-break-word">{msg.text}</pre>
                <p className={`text-xs mt-1 ${msg.sender === 'user' ? 'text-purple-200' : 'text-gray-400'}`}>
                  {msg.time}
                </p>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-800 text-gray-100 rounded-2xl rounded-bl-none px-4 py-3 max-w-[85%] sm:max-w-[80%]">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.41s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-800 bg-gray-900/50 p-3">
        <form onSubmit={handleSendMessage} className="flex gap-1 sm:gap-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask me to manage tasks..."
            className="grow bg-gray-800 border border-gray-700 rounded-lg text-sm sm:text-base text-white px-3 py-2 sm:px-4 sm:py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent placeholder-gray-500"
          />
          <button
            type="submit"
            disabled={!inputText.trim()}
            className="bg-linear-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 text-white rounded-lg px-4 py-2 sm:px-6 sm:py-3 font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 sm:h-5 sm:w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;