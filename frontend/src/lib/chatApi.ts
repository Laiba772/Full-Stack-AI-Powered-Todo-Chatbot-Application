// frontend/src/lib/chatApi.ts
import axios from 'axios';
import apiClient from '@/lib/api/clients'; // Import the shared axios instance

interface ChatRequest {
    message: string;
    conversation_id?: string;
}

export interface Message {
    createdAt: number;
    id: string;
    sender: 'user' | 'ai';
    content: string;
    timestamp: string;
    tool_calls?: any;
    tool_output?: any;
}

interface ChatResponse {
    conversation_id: string;
    message: string;
    ai_message: string;
    tool_invoked: boolean;
}

// Function to send a chat message
export const sendMessage = async (userId: string, chatRequest: ChatRequest): Promise<ChatResponse> => {
    try {
        const response = await apiClient.post<ChatResponse>(
            `/api/${userId}/chat`,
            chatRequest
        );
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw new Error(error.response.data.detail || 'Failed to send message.');
        }
        throw new Error('An unexpected error occurred while sending message.');
    }
};

// Function to fetch conversation history
export const fetchConversationHistory = async (userId: string): Promise<Message[]> => {
    try {
        const response = await apiClient.get<Message[]>(
            `/api/${userId}/chat/history`
        );
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw new Error(error.response.data.detail || 'Failed to fetch conversation history.');
        }
        throw new Error('An unexpected error occurred while fetching conversation history.');
    }
};
