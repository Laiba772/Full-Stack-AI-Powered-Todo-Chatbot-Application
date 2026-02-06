// frontend/src/hooks/useConversation.ts
import { useState, useEffect } from 'react';
import { fetchConversationHistory, Message } from '../lib/chatApi'; // Import Message interface
import { useBetterAuth } from './useBetterAuth'; // Import useBetterAuth hook
import { jwtDecode } from 'jwt-decode'; // Import jwtDecode

interface UseConversationResult {
  [x: string]: any;
  messages: Message[];
  loading: boolean;
  error: string | null;
  conversationId: string | undefined; // The conversation ID loaded or created
  currentUserId: string | null;
  startNewConversation: () => void;
  setConversationId: (id: string | undefined) => void;
  addMessage: (message: Message) => void;
}

export const useConversation = (): UseConversationResult => {
  const { isAuthenticated } = useBetterAuth();
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);

  // Derive userId from JWT token if authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const decodedToken: { sub: string } = jwtDecode(token);
          setCurrentUserId(decodedToken.sub);
        } catch (error) {
          console.error("Error decoding token:", error);
        }
      }
    } else {
      setCurrentUserId(null);
      setMessages([]); // Clear messages if not authenticated
      setConversationId(undefined); // Clear conversationId
    }
  }, [isAuthenticated]);


  // Effect to load conversation history on mount or when userId/conversationId changes
  useEffect(() => {
    const loadConversation = async () => {
      if (!currentUserId || !isAuthenticated) {
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const history = await fetchConversationHistory(currentUserId);
        setMessages(history);
        if (history.length > 0) {
          // We don't have conversation_id in the message, so we need to derive it differently
          // For now, we'll leave conversationId undefined since it's not available in the message
          setConversationId(undefined); // No conversation_id in message, so set to undefined
        } else {
          setConversationId(undefined); // No history, new conversation to be started
        }
      } catch (err: any) {
        setError(err.message || 'Failed to fetch conversation history.');
        setMessages([]);
        setConversationId(undefined);
      } finally {
        setLoading(false);
      }
    };

    loadConversation();
  }, [currentUserId, isAuthenticated]); // Re-run when currentUserId or isAuthenticated changes

  const startNewConversation = () => {
    setConversationId(undefined);
    setMessages([]);
    setError(null);
    // The next message sent will initiate a new conversation on the backend
  };

  const addMessage = (message: Message) => {
    setMessages(prev => [...prev, message]);
  };

  return { messages, loading, error, conversationId, startNewConversation, setConversationId, currentUserId, addMessage };
};
