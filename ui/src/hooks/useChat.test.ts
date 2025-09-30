import { renderHook, act, waitFor } from '@testing-library/react';
import { useChat } from './useChat';
import { ChatService } from '../services/chatService';

// Mock the ChatService
jest.mock('../services/chatService');
const mockChatService = ChatService as jest.Mocked<typeof ChatService>;

// Mock uuid
jest.mock('uuid', () => ({
  v4: jest.fn(() => 'mock-uuid'),
}));

describe('useChat Hook', () => {
  let mockSendMessage: jest.Mock;
  let mockGetInstance: jest.Mock;

  beforeEach(() => {
    mockSendMessage = jest.fn();
    mockGetInstance = jest.fn(() => ({
      sendMessage: mockSendMessage,
    }));
    mockChatService.getInstance = mockGetInstance;

    jest.clearAllMocks();
  });

  it('initializes with empty state', () => {
    const { result } = renderHook(() => useChat());

    expect(result.current.messages).toEqual([]);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('adds user message and assistant message when sending', async () => {
    const { result, waitForNextUpdate } = renderHook(() => useChat());

    // Mock successful streaming
    mockSendMessage.mockImplementation(async (message, onChunk, onComplete) => {
      setTimeout(() => {
        onChunk('Hello');
        onChunk(' there!');
        onComplete();
      }, 0);
    });

    await act(async () => {
      await result.current.sendMessage('Test message');
    });

    // Wait for state updates
    await waitFor(() => {
      expect(result.current.messages).toHaveLength(2);
    });

    expect(result.current.messages[0]).toMatchObject({
      content: 'Test message',
      sender: 'user',
    });
    expect(result.current.messages[1]).toMatchObject({
      content: 'Hello there!',
      sender: 'assistant',
      isStreaming: false,
    });
  });

  it('handles streaming response correctly', async () => {
    const { result } = renderHook(() => useChat());

    mockSendMessage.mockImplementation(async (message, onChunk, onComplete) => {
      setTimeout(() => {
        onChunk('Hello');
        onChunk(' world!');
        onComplete();
      }, 0);
    });

    await act(async () => {
      await result.current.sendMessage('Test message');
    });

    // Wait for streaming to complete
    await waitFor(() => {
      expect(result.current.messages[1].content).toBe('Hello world!');
    });

    expect(result.current.messages).toHaveLength(2);
    expect(result.current.messages[1]).toMatchObject({
      content: 'Hello world!',
      sender: 'assistant',
      isStreaming: false,
    });
    expect(result.current.isLoading).toBe(false);
  });

  it('handles errors correctly', async () => {
    const { result } = renderHook(() => useChat());

    mockSendMessage.mockImplementation(async (message, onChunk, onComplete, onError) => {
      setTimeout(() => {
        onError('Network error');
      }, 0);
    });

    await act(async () => {
      await result.current.sendMessage('Test message');
    });

    // Wait for error state
    await waitFor(() => {
      expect(result.current.error).toBe('Network error');
    });

    expect(result.current.isLoading).toBe(false);
    // Should only have user message, assistant message should be removed on error
    expect(result.current.messages).toHaveLength(1);
    expect(result.current.messages[0].sender).toBe('user');
  });

  it('prevents sending empty messages', async () => {
    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage('');
    });

    expect(mockSendMessage).not.toHaveBeenCalled();
    expect(result.current.messages).toHaveLength(0);

    await act(async () => {
      await result.current.sendMessage('   ');
    });

    expect(mockSendMessage).not.toHaveBeenCalled();
    expect(result.current.messages).toHaveLength(0);
  });

  it('prevents sending messages when loading', async () => {
    const { result } = renderHook(() => useChat());

    // Start first message
    mockSendMessage.mockImplementation(async () => {
      // Don't complete, keep loading
    });

    act(() => {
      result.current.sendMessage('First message');
    });

    expect(result.current.isLoading).toBe(true);

    // Try to send second message while loading
    await act(async () => {
      await result.current.sendMessage('Second message');
    });

    // Should only have been called once
    expect(mockSendMessage).toHaveBeenCalledTimes(1);
  });

  it('clears messages correctly', () => {
    const { result } = renderHook(() => useChat());

    // Add some messages first
    act(() => {
      result.current.sendMessage('Test message');
    });

    expect(result.current.messages).toHaveLength(2); // user + assistant

    act(() => {
      result.current.clearMessages();
    });

    expect(result.current.messages).toEqual([]);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('clears error correctly', () => {
    const { result } = renderHook(() => useChat());

    // Simulate error
    let onError: (error: string) => void;
    mockSendMessage.mockImplementation(async (message, onChunk, onComplete, errorCallback) => {
      onError = errorCallback;
    });

    act(() => {
      result.current.sendMessage('Test message');
    });

    act(() => {
      onError('Test error');
    });

    expect(result.current.error).toBe('Test error');

    act(() => {
      result.current.clearError();
    });

    expect(result.current.error).toBe(null);
  });

  it('trims message content before sending', async () => {
    const { result } = renderHook(() => useChat());

    mockSendMessage.mockImplementation(async (message, onChunk, onComplete) => {
      onComplete();
    });

    await act(async () => {
      await result.current.sendMessage('  Test message  ');
    });

    expect(mockSendMessage).toHaveBeenCalledWith(
      'Test message',
      expect.any(Function),
      expect.any(Function),
      expect.any(Function)
    );

    expect(result.current.messages[0].content).toBe('Test message');
  });
});
