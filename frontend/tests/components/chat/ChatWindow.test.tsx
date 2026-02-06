import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatWindow from '@/components/chat/ChatWindow';
import * as chatApi from '@/lib/chatApi';
import * as useConversationHook from '@/hooks/useConversation';
import * as useBetterAuthHook from '@/hooks/useBetterAuth';
import { User } from 'better-auth';

// --------------------
// Mock dependencies
// --------------------
jest.mock('../../../src/lib/chatApi');
jest.mock('../../../src/hooks/useConversation');
jest.mock('../../../src/hooks/useBetterAuth');
jest.mock('@openai/chatkit-react'); // Use the shared mock from __mocks__

// Type-safe mocks
const mockUseConversation = useConversationHook.useConversation as jest.MockedFunction<typeof useConversationHook.useConversation>;
const mockUseBetterAuth = useBetterAuthHook.useBetterAuth as jest.MockedFunction<typeof useBetterAuthHook.useBetterAuth>;
const mockSendMessage = chatApi.sendMessage as jest.MockedFunction<typeof chatApi.sendMessage>;

// --------------------
// TypeScript types
// --------------------
interface Message {
  id: string;
  sender: 'user' | 'ai';
  content: string;
  timestamp?: string;
  conversation_id?: string;
  tool_invoked?: boolean;
  ai_message?: string;
}

describe('ChatWindow', () => {
  const mockUserId = 'test-user-id';
  const mockConversationId = 'test-conversation-id';
  const mockAddMessage = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();

    mockUseBetterAuth.mockReturnValue({
      user: { id: mockUserId, email: 'test@example.com' },
      loading: false,
      isAuthenticated: true,
      signIn: jest.fn(),
      signUp: jest.fn(),
      signOut: jest.fn(),
      error: null
    });

    mockSendMessage.mockResolvedValue({
      conversation_id: 'new-test-conversation-id',
      message: 'User message',
      ai_message: 'AI response',
      tool_invoked: false,
    });
  });

  // Test for loading authentication
  it('renders loading state when authenticating', () => {
    mockUseBetterAuth.mockReturnValue({
      loading: true, isAuthenticated: false,
      signIn: jest.fn(),
      signUp: jest.fn(),
      signOut: jest.fn(),
      user: null,
      error: null
    });
    // Simplified mockUseConversation for this test
    mockUseConversation.mockReturnValue({
      messages: [], loading: false, error: null, conversationId: undefined,
      startNewConversation: jest.fn(), setConversationId: jest.fn(),
      currentUserId: null,
      addMessage: mockAddMessage
    });
    render(<ChatWindow />);
    expect(screen.getByText(/Loading authentication/i)).toBeInTheDocument();
  });

  // Test for loading conversation history
  it('renders loading state when fetching conversation history', () => {
    mockUseConversation.mockReturnValue({
      messages: [], loading: true, error: null, conversationId: undefined,
      currentUserId: mockUserId,
      setConversationId: jest.fn(), startNewConversation: jest.fn(),
      addMessage: mockAddMessage
    });
    render(<ChatWindow />);
    expect(screen.getByText(/Loading conversation history/i)).toBeInTheDocument();
  });

  // Test for rendering chat interface for authenticated user
  it('renders chat interface for authenticated user', () => {
    // Default mockUseConversation for this test
    mockUseConversation.mockReturnValue({
      messages: [], loading: false, error: null, conversationId: undefined,
      startNewConversation: jest.fn(), setConversationId: jest.fn(),
      currentUserId: mockUserId,
      addMessage: mockAddMessage
    });
    render(<ChatWindow />);
    expect(screen.getByText(/AI Chat for User/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Type your message.../i)).toBeInTheDocument();
  });

  // Test for sending a message and displaying AI response
  it('sends a message and displays AI response', async () => {
    mockUseConversation.mockReturnValue({
      messages: [], loading: false, error: null, conversationId: undefined,
      startNewConversation: jest.fn(), setConversationId: jest.fn(),
      currentUserId: mockUserId,
      addMessage: mockAddMessage
    });

    render(<ChatWindow />);
    const input = screen.getByTestId('mock-message-input'); // Use data-testid from mock

    await act(async () => {
      fireEvent.change(input, { target: { value: 'Hello AI' } });
      fireEvent.submit(screen.getByRole('button', { name: /send/i }));
    });

    await waitFor(() => {
      expect(mockAddMessage).toHaveBeenCalledWith(expect.objectContaining({ content: 'Hello AI', sender: 'user' }));
    });
    await waitFor(() => {
      expect(mockSendMessage).toHaveBeenCalledWith(mockUserId, { message: 'Hello AI', conversation_id: undefined });
    });
    await waitFor(() => {
        expect(mockAddMessage).toHaveBeenCalledWith(expect.objectContaining({ content: 'AI response', sender: 'ai' }));
    });
    // This test no longer asserts on rendered messages directly. It asserts that addMessage was called.
    // The actual rendering is handled by the MessageList mock.
  });

  // Test for displaying error message if message sending fails
  it('displays error message if message sending fails', async () => {
    mockSendMessage.mockRejectedValue(new Error('Network error'));
    mockUseConversation.mockReturnValue({
      messages: [], loading: false, error: null, conversationId: undefined,
      startNewConversation: jest.fn(), setConversationId: jest.fn(),
      currentUserId: mockUserId,
      addMessage: mockAddMessage
    });

    render(<ChatWindow />);
    const input = screen.getByTestId('mock-message-input');

    await act(async () => {
      fireEvent.change(input, { target: { value: 'Fail this' } });
      fireEvent.submit(screen.getByRole('button', { name: /send/i }));
    });

    await waitFor(() => {
      expect(mockAddMessage).toHaveBeenCalledWith(expect.objectContaining({ content: 'Fail this', sender: 'user' }));
    });
    await waitFor(() => {
        expect(mockAddMessage).toHaveBeenCalledWith(expect.objectContaining({ content: 'Error: Network error', sender: 'ai' }));
    });
    // This test no longer asserts on rendered error message directly. It asserts that addMessage was called.
  });
});
