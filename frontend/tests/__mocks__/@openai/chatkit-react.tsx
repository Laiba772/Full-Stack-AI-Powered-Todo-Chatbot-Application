// frontend/tests/__mocks__/@openai/chatkit-react.tsx
import React from 'react';
import { screen } from '@testing-library/react'; // Import screen for accessing elements in mock

// This is a shared mock for @openai/chatkit-react components
// It provides simple functional components that render their children or basic elements
// using React.createElement to avoid JSX parsing issues in some test environments.

// Mock for useChatKit hook - enhanced to support message submission callbacks
export const useChatKit = jest.fn(({ initialThread, api, events }) => {
  // Create a ref to hold event listeners and message handlers
  const eventListenersRef = React.useRef<Record<string, Array<(event: any) => void>>>({});
  // Store a callback for message submission
  const onMessageSubmitRef = React.useRef<((message: string) => void) | null>(null);

  return {
    control: {},
    ref: {
      current: {
        addEventListener: (eventType: string, listener: (event: any) => void) => {
          if (!eventListenersRef.current[eventType]) {
            eventListenersRef.current[eventType] = [];
          }
          eventListenersRef.current[eventType].push(listener);
        },
        removeEventListener: (eventType: string, listener: (event: any) => void) => {
          if (eventListenersRef.current[eventType]) {
            eventListenersRef.current[eventType] = eventListenersRef.current[eventType].filter(l => l !== listener);
          }
        },
        dispatchEvent: (event: CustomEvent) => {
          const listeners = eventListenersRef.current[event.type] || [];
          listeners.forEach(listener => listener(event));
        },
        // Allow registering a callback for message submission
        setMessageSubmissionHandler: (handler: (message: string) => void) => {
          onMessageSubmitRef.current = handler;
        }
      }
    },
    // Mock methods that might be called
    setThreadId: jest.fn(),
    // Function to trigger the message submission handler
    triggerMessageSubmission: (message: string) => {
      if (onMessageSubmitRef.current) {
        onMessageSubmitRef.current(message);
      }
    }
  };
});

export const ChatProvider = ({ children }: { children: React.ReactNode }) => {
  return React.createElement('div', { 'data-testid': 'mock-chat-provider' }, children);
};

export const MessageList = ({ messages }: { messages: any[] }) => {
  return React.createElement('div', { 'data-testid': 'mock-message-list' },
    messages.map((msg: any) =>
      React.createElement('div', { key: msg.id, 'data-testid': 'mock-message-item', className: `message-${msg.sender}` }, msg.content)
    )
  );
};

export const MessageInput = ({ onSubmit, isLoading, placeholder, disabled, dataTestId }:
  { onSubmit: (text: string) => void; isLoading?: boolean; placeholder?: string; disabled?: boolean; dataTestId?: string }) => {
  const testId = dataTestId || 'mock-message-input';
  return React.createElement('form', {
    onSubmit: (e: React.FormEvent) => {
      e.preventDefault();
      const input = (screen.getByTestId(testId) as HTMLInputElement);
      onSubmit(input.value);
    }
  },
    React.createElement('input', {
      'data-testid': testId,
      type: 'text',
      placeholder: placeholder,
      disabled: isLoading || disabled,
    }),
    React.createElement('button', { type: 'submit', disabled: isLoading || disabled }, 'Send')
  );
};

export const ChatKit = ({ control, ref, children }: { control: any; ref: any; children?: React.ReactNode }) => {
  // ChatKit should render its own MessageInput and MessageList components
  // Use ref to connect message submission functionality if available
  const handleSubmit = (text: string) => {
    // Trigger message submission through the ref if method exists
    if (ref && ref.current && typeof ref.current.setMessageSubmissionHandler === 'function') {
      // If setMessageSubmissionHandler exists, it means ChatKit might register a handler
      // For now, assume that the parent component will directly handle this
    } else if (ref && ref.current && typeof ref.current.triggerMessageSubmission === 'function') {
      // Or directly call triggerMessageSubmission if available
      ref.current.triggerMessageSubmission(text);
    }
  };

  return React.createElement('div', { 'data-testid': 'mock-chatkit-root', ref },
    // Render a MessageInput with the expected placeholder
    React.createElement(MessageInput, {
      onSubmit: handleSubmit,
      placeholder: "Type your message...",
      dataTestId: "mock-message-input"
    }),
    children // Render any additional children
  );
};

export default {
  ChatProvider,
  MessageList,
  MessageInput,
  ChatKit,
  useChatKit,
};