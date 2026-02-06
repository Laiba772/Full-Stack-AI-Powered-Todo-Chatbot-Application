// frontend/tests/integration/chat.test.ts
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { http } from 'msw';            // HTTP handlers
import { setupServer } from 'msw/node';
import ChatWindow from '../../src/components/chat/ChatWindow';
import * as useBetterAuthHook from '../../src/hooks/useBetterAuth';
import { act } from 'react-dom/test-utils'; // For explicit act calls
import { TextDecoder, TextEncoder } from 'util'; // Polyfill for TextEncoder/Decoder

// Polyfill TextEncoder/Decoder for JSDOM environment
Object.assign(global, { TextDecoder, TextEncoder });


// Mock BetterAuth for authenticated state
jest.mock('../../src/hooks/useBetterAuth', () => ({
  useBetterAuth: jest.fn(),
}));
const mockUseBetterAuth = useBetterAuthHook.useBetterAuth as jest.Mock;

jest.mock('@openai/chatkit-react'); // Use the shared mock from __mocks__


// Mock localStorage
const localStorageMock = (function () {
  let store: { [key: string]: string } = {};
  return {
    getItem: jest.fn((key: string) => store[key] || null),
    setItem: jest.fn((key: string, value: string) => {
      store[key] = value.toString();
    }),
    removeItem: jest.fn((key: string) => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    }),
  };
})();
Object.defineProperty(window, 'localStorage', { value: localStorageMock });


// Mock jwt-decode
jest.mock('jwt-decode', () => ({
  jwtDecode: jest.fn(() => ({ sub: 'test-user-id' })),
}));


const mockUserId = 'test-user-id';
const mockConversationId = 'test-conversation-id-123';
const mockAccessToken = 'mock-jwt-access-token';

// Setup Mock Service Worker (MSW) server
interface ChatPostRequestBody {
  message: string;
  conversation_id?: string;
}

interface ChatPostResponseBody {
  conversation_id: string;
  message: string;
  ai_message: string;
  tool_invoked: boolean;
}

interface ChatHistoryMessage {
  id: string;
  conversation_id: string;
  sender: string;
  content: string;
  timestamp: string;
}

interface MockAuthHeaders {
  authorization?: string | null;
}

interface ChatPostRequestBody {
  message: string;
  conversation_id?: string;
}

interface ChatPostResponseBody {
  conversation_id: string;
  message: string;
  ai_message: string;
  tool_invoked: boolean;
}

interface ChatHistoryMessage {
  id: string;
  conversation_id: string;
  sender: string;
  content: string;
  timestamp: string;
}

interface MockAuthHeaders {
  authorization?: string | null;
}

const server = setupServer(
  http.post<ChatPostRequestBody, ChatPostResponseBody, MockAuthHeaders>(
    `*/api/${mockUserId}/chat`,
    async ({ request, cookies, params }) => {
      const { message, conversation_id }: ChatPostRequestBody = await request.json();
      const authHeader = request.headers.get('authorization');
      if (!authHeader?.startsWith('Bearer ' + mockAccessToken)) {
        return new Response(JSON.stringify({ detail: 'Unauthorized' }), { status: 401 });
      }
      return Response.json({
        conversation_id: conversation_id || mockConversationId,
        message: message,
        ai_message: `AI Echo: ${message}`,
        tool_invoked: false,
      } as ChatPostResponseBody);
    }
  ),
  http.get(
    `*/api/${mockUserId}/chat/history`,
    ({ request }) => {
      const authHeader = request.headers.get('authorization');
      if (!authHeader?.startsWith('Bearer ' + mockAccessToken)) {
        return new Response(JSON.stringify({ detail: 'Unauthorized' }), { status: 401 });
      }
      // Return empty history by default
      return Response.json([] as ChatHistoryMessage[]);
    }
  )
);

beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  localStorageMock.clear(); // Clear local storage after each test
  // Clear all Mocks as well for good measure
  jest.clearAllMocks();
});
afterAll(() => server.close());


describe('ChatWindow Integration', () => {
  beforeEach(() => {
    // Default authenticated state
    mockUseBetterAuth.mockReturnValue({
      user: { id: mockUserId, email: 'test@example.com' },
      loading: false,
      isAuthenticated: true,
    });
    localStorageMock.setItem('access_token', mockAccessToken); // Ensure token is in local storage
  });

  it('renders chat interface and sends a new message successfully', async () => {
    render(<ChatWindow />);

    // Wait for history to load (even if empty)
    await waitFor(() => expect(screen.getByText(/AI Chat for User/i)).toBeInTheDocument());

    const input = screen.getByPlaceholderText(/Type your message.../i);
    fireEvent.change(input, { target: { value: 'Hello AI' } });

    await act(async () => {
        fireEvent.submit(input);
    });
    

    // Expect user message to appear immediately
    expect(await screen.findByText('Hello AI')).toBeInTheDocument();
    
    // Expect AI response to appear
    expect(await screen.findByText('AI Echo: Hello AI')).toBeInTheDocument();
  });

  it('sends a message to an existing conversation', async () => {
    // Mock history endpoint to return a conversation with some messages
    server.use(
      http.get(`*/api/${mockUserId}/chat/history`, () => {
        return Response.json([
          { id: 'hist-msg1', conversation_id: mockConversationId, sender: 'user', content: 'Old message user', timestamp: '...' },
          { id: 'hist-msg2', conversation_id: mockConversationId, sender: 'ai', content: 'Old message AI', timestamp: '...' },
        ]);
      })
    );

    render(<ChatWindow />);

    // Wait for history to load
    await waitFor(() => expect(screen.getByText('Old message user')).toBeInTheDocument());
    expect(screen.getByText('Old message AI')).toBeInTheDocument();

    const input = screen.getByPlaceholderText(/Type your message.../i);
    fireEvent.change(input, { target: { value: 'New message to existing chat' } });
    
    await act(async () => {
        fireEvent.submit(input);
    });

    // Expect new user message and AI response
    expect(await screen.findByText('New message to existing chat')).toBeInTheDocument();
    expect(await screen.findByText('AI Echo: New message to existing chat')).toBeInTheDocument();
  });

  it('handles unauthorized access when sending a message', async () => {
    // Mock the backend to return 401 for chat messages
    server.use(
      http.post(`*/api/${mockUserId}/chat`, () => {
        return new Response(JSON.stringify({ detail: 'Unauthorized' }), { status: 401 });
      })
    );

    render(<ChatWindow />);

    const input = screen.getByPlaceholderText(/Type your message.../i);
    fireEvent.change(input, { target: { value: 'Unauthorized message' } });
    
    await act(async () => {
        fireEvent.submit(input);
    });

    expect(await screen.findByText(/Error: Unauthorized/i)).toBeInTheDocument();
  });

  it('handles network error when fetching history', async () => {
    server.use(
      http.get(`*/api/${mockUserId}/chat/history`, () => {
        return new Response(JSON.stringify({ detail: 'Network error' }), { status: 500 });
      })
    );
    render(<ChatWindow />);
    expect(await screen.findByText(/Failed to fetch conversation history/i)).toBeInTheDocument();
  });
});