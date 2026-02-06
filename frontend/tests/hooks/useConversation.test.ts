// frontend/tests/hooks/useConversation.test.ts
import { renderHook, act, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import * as useBetterAuthHook from '@/hooks/useBetterAuth';
import * as chatApi from '@/lib/chatApi';
import { useConversation } from '@/hooks/useConversation';

// Mock dependencies
jest.mock('@/lib/chatApi');
jest.mock('@/hooks/useBetterAuth');

const mockUseBetterAuth = useBetterAuthHook.useBetterAuth as jest.Mock;
const mockFetchConversationHistory = chatApi.fetchConversationHistory as jest.Mock;
const mockJwtDecode = jest.fn(); // Mock jwtDecode

// Manually mock the jwt-decode module
jest.mock('jwt-decode', () => ({
  jwtDecode: (token: string) => mockJwtDecode(token),
}));

const mockLocalStorageGetItem = jest.fn();

describe('useConversation', () => {
  const mockUserId = 'test-user-id';
  const mockAccessToken = 'mock-jwt-access-token';

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: mockLocalStorageGetItem, // Use the mock function here
        setItem: jest.fn(),
        removeItem: jest.fn(),
      },
      writable: true,
    });

    // Default mock for useBetterAuth - authenticated
    mockUseBetterAuth.mockReturnValue({
      user: { id: mockUserId, email: 'test@example.com' },
      loading: false,
      isAuthenticated: true,
    });

    // Default mock for jwtDecode
    mockJwtDecode.mockReturnValue({ sub: mockUserId });

    // Default mock for localStorage.getItem
    mockLocalStorageGetItem.mockReturnValue(mockAccessToken);

    // Default mock for chatApi
    mockFetchConversationHistory.mockResolvedValue([]);
  });

  it('initializes with empty messages and loading state when not authenticated', async () => {
    mockUseBetterAuth.mockReturnValue({ user: null, loading: false, isAuthenticated: false });
    mockJwtDecode.mockReturnValue({}); // No token to decode, so jwtDecode returns empty object
    mockLocalStorageGetItem.mockReturnValue(null);
    const { result, rerender } = renderHook(() => useConversation());
    rerender();

    expect(result.current.messages).toEqual([]);
    expect(result.current.loading).toBe(false); // No loading if not authenticated initially
    expect(result.current.error).toBeNull();
    expect(result.current.conversationId).toBeUndefined();
    await waitFor(() => expect(result.current.currentUserId).toBeNull());
    expect(mockFetchConversationHistory).not.toHaveBeenCalled();
  });

  it('fetches conversation history on mount if authenticated', async () => {
    const mockHistory = [
      { id: 'msg1', conversation_id: 'conv1', sender: 'user', content: 'Hi', timestamp: '...' },
      { id: 'msg2', conversation_id: 'conv1', sender: 'ai', content: 'Hello', timestamp: '...' },
    ];
    mockFetchConversationHistory.mockResolvedValue(mockHistory);

    const { result, rerender } = renderHook(() => useConversation());
    rerender();

    expect(result.current.loading).toBe(true); // Should be loading initially
    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.messages).toEqual(mockHistory);
    expect(result.current.conversationId).toBe('conv1');
    await waitFor(() => expect(result.current.currentUserId).toBe(mockUserId));
    expect(mockFetchConversationHistory).toHaveBeenCalledWith(mockUserId);
  });

  it('handles error during history fetch', async () => {
    mockFetchConversationHistory.mockRejectedValue(new Error('API error'));

    const { result } = renderHook(() => useConversation());

    expect(result.current.loading).toBe(true);
    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.messages).toEqual([]);
    expect(result.current.error).toBe('API error');
    expect(result.current.conversationId).toBeUndefined();
  });

  it('starts a new conversation', async () => {
    const mockHistory = [
      { id: 'msg1', conversation_id: 'conv1', sender: 'user', content: 'Hi', timestamp: '...' },
    ];
    mockFetchConversationHistory.mockResolvedValue(mockHistory);

    const { result } = renderHook(() => useConversation());

    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.conversationId).toBe('conv1');

    act(() => {
      result.current.startNewConversation();
    });

    expect(result.current.messages).toEqual([]);
    expect(result.current.conversationId).toBeUndefined();
    expect(result.current.error).toBeNull();
  });

  it('updates conversationId correctly', async () => {
    mockFetchConversationHistory.mockResolvedValue([]); // Start with no history

    const { result } = renderHook(() => useConversation());

    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.conversationId).toBeUndefined();

    const newConvId = 'new-conversation-id';
    act(() => {
      result.current.setConversationId(newConvId);
    });

    expect(result.current.conversationId).toBe(newConvId);
  });

  it('clears state on sign out', async () => {
    const mockHistory = [
      { id: 'msg1', conversation_id: 'conv1', sender: 'user', content: 'Hi', timestamp: '...' },
    ];
    mockFetchConversationHistory.mockResolvedValue(mockHistory);

    const { result, rerender } = renderHook(() => useConversation()); // Destructure rerender here

    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.messages).toEqual(mockHistory);

    act(() => {
      mockUseBetterAuth.mockReturnValue({ loading: false, isAuthenticated: false }); // Simulate sign out
      rerender(); // Rerender hook to trigger useEffect
    });

    await waitFor(() => {
        expect(result.current.messages).toEqual([]);
        expect(result.current.conversationId).toBeUndefined();
        expect(result.current.currentUserId).toBeNull();
    });
  });
});
