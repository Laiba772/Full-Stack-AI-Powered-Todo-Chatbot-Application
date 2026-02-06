// frontend/tests/lib/chatApi.test.ts
import axios from 'axios';
import { sendMessage, fetchConversationHistory } from '@/lib/chatApi';
import apiClient from '@/lib/api/clients';
import '@testing-library/jest-dom';

jest.mock('@/lib/api/clients'); // Mock the apiClient
jest.mock('axios', () => ({
  ...jest.requireActual('axios'),
  isAxiosError: jest.fn((payload): payload is import('axios').AxiosError => {
    // Check for a specific property that indicates it's a mocked AxiosError
    return payload && typeof payload === 'object' && 'response' in payload;
  }),
}));

const mockApiClient = apiClient as jest.Mocked<typeof apiClient>;

describe('chatApi', () => {
  const userId = 'user-123';
  const token = 'mock-jwt-token'; // Token is now handled by interceptor, but keeping for conceptual clarity

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('sendMessage', () => {
    it('sends a new message and returns chat response', async () => {
      const mockChatRequest = { message: 'Hello AI!' };
      const mockChatResponse = {
        conversation_id: 'conv-456',
        message: 'Hello AI!',
        ai_message: 'Hi there!',
        tool_invoked: false,
      };
      mockApiClient.post.mockResolvedValueOnce({ data: mockChatResponse });

      const response = await sendMessage(userId, mockChatRequest);

      expect(mockApiClient.post).toHaveBeenCalledWith(`/api/${userId}/chat`, mockChatRequest);
      expect(response).toEqual(mockChatResponse);
    });

    it('sends a message to an existing conversation', async () => {
      const mockChatRequest = { message: 'Continue conversation', conversation_id: 'conv-456' };
      const mockChatResponse = {
        conversation_id: 'conv-456',
        message: 'Continue conversation',
        ai_message: 'Understood.',
        tool_invoked: false,
      };
      mockApiClient.post.mockResolvedValueOnce({ data: mockChatResponse });

      const response = await sendMessage(userId, mockChatRequest);

      expect(mockApiClient.post).toHaveBeenCalledWith(`/api/${userId}/chat`, mockChatRequest);
      expect(response).toEqual(mockChatResponse);
    });

    it('throws an error if the API call fails', async () => {
      const mockChatRequest = { message: 'Fail me' };
      const errorMessage = 'API error';
      mockApiClient.post.mockRejectedValueOnce({ response: { data: { detail: errorMessage } } });

      await expect(sendMessage(userId, mockChatRequest)).rejects.toThrow(errorMessage);
    });
  });

  describe('fetchConversationHistory', () => {
    it('fetches conversation history for a user', async () => {
      const mockMessages = [
        { id: 'msg1', sender: 'user', content: 'Hi', timestamp: '...' },
        { id: 'msg2', sender: 'ai', content: 'Hello', timestamp: '...' },
      ];
      mockApiClient.get.mockResolvedValueOnce({ data: mockMessages });

      const history = await fetchConversationHistory(userId);

      expect(mockApiClient.get).toHaveBeenCalledWith(`/api/${userId}/chat/history`);
      expect(history).toEqual(mockMessages);
    });

    it('throws an error if fetching history fails', async () => {
      const errorMessage = 'Failed to load history';
      mockApiClient.get.mockRejectedValueOnce({ response: { data: { detail: errorMessage } } });

      await expect(fetchConversationHistory(userId)).rejects.toThrow(errorMessage);
    });
  });
});
