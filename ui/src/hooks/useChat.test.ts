import { renderHook, act, waitFor } from '@testing-library/react';
import { useChat } from './useChat';
import { ChatService } from '../services/chatService';

// Mock the ChatService
jest.mock('../services/chatService');
const mockChatService = ChatService as jest.Mocked<typeof ChatService>;

// Mock uuid - return unique IDs for each call
jest.mock('uuid', () => {
  let counter = 0;
  return {
    v4: () => `mock-uuid-${++counter}`,
  };
});

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
    const { result } = renderHook(() => useChat());

    // Mock successful streaming - call sync to test
    mockSendMessage.mockImplementation(async (message, history, onChunk, onComplete) => {
      // Call immediately without delay
      onChunk('Hello');
      onChunk(' there!');
      onComplete();
    });

    await act(async () => {
      await result.current.sendMessage('Test message');
    });

    // Verify mock was called
    expect(mockSendMessage).toHaveBeenCalledTimes(1);

    // Use waitFor for final assertions
    await waitFor(() => {
      expect(result.current.messages).toHaveLength(2);
    });

    await waitFor(() => {
      expect(result.current.messages[1]).toMatchObject({
        content: 'Hello there!',
        isStreaming: false,
      });
    });

    expect(result.current.messages[0]).toMatchObject({
      content: 'Test message',
      sender: 'user',
    });
  });

  it('handles streaming response correctly', async () => {
    const { result } = renderHook(() => useChat());

    mockSendMessage.mockImplementation(async (message, history, onChunk, onComplete) => {
      // Wait for state to settle, then call callbacks
      await new Promise((resolve) => setTimeout(resolve, 100));
      onChunk('Hello');
      onChunk(' world!');
      onComplete();
    });

    await act(async () => {
      await result.current.sendMessage('Test message');
    });

    // Wait for streaming to complete
    await waitFor(() => {
      expect(result.current.messages).toHaveLength(2);
    });

    await waitFor(() => {
      expect(result.current.messages[1].content).toBe('Hello world!');
    });

    expect(result.current.messages[1]).toMatchObject({
      content: 'Hello world!',
      sender: 'assistant',
      isStreaming: false,
    });
    expect(result.current.isLoading).toBe(false);
  });

  it('handles errors correctly', async () => {
    const { result } = renderHook(() => useChat());

    mockSendMessage.mockImplementation(async (message, history, onChunk, onComplete, onError) => {
      // Wait for state to settle, then call error callback
      await new Promise((resolve) => setTimeout(resolve, 100));
      onError('Network error');
    });

    await act(async () => {
      await result.current.sendMessage('Test message');
    });

    // Wait for error state
    await waitFor(() => {
      expect(result.current.error).toBe('Network error');
    });

    await waitFor(() => {
      expect(result.current.messages).toHaveLength(1);
    });

    expect(result.current.isLoading).toBe(false);
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
    mockSendMessage.mockImplementation(async (message, history, onChunk, onComplete, errorCallback) => {
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

    mockSendMessage.mockImplementation(async (message, history, onChunk, onComplete) => {
      onComplete();
    });

    await act(async () => {
      await result.current.sendMessage('  Test message  ');
    });

    expect(mockSendMessage).toHaveBeenCalledWith(
      'Test message',
      expect.any(Array),
      expect.any(Function),
      expect.any(Function),
      expect.any(Function),
      expect.any(Function),
      expect.any(Function)
    );

    expect(result.current.messages[0].content).toBe('Test message');
  });

  describe('exportToMarkdown', () => {
    let mockCreateObjectURL: jest.Mock;
    let mockRevokeObjectURL: jest.Mock;
    let mockClick: jest.Mock;
    let mockAppendChild: jest.Mock;
    let mockRemoveChild: jest.Mock;
    let createdLink: HTMLAnchorElement;

    beforeEach(() => {
      mockCreateObjectURL = jest.fn(() => 'blob:mock-url');
      mockRevokeObjectURL = jest.fn();
      mockClick = jest.fn();
      mockAppendChild = jest.fn();
      mockRemoveChild = jest.fn();

      global.URL.createObjectURL = mockCreateObjectURL;
      global.URL.revokeObjectURL = mockRevokeObjectURL;

      // Mock document.createElement to capture the created link
      const originalCreateElement = document.createElement.bind(document);
      jest.spyOn(document, 'createElement').mockImplementation((tagName: string) => {
        const element = originalCreateElement(tagName);
        if (tagName === 'a') {
          createdLink = element as HTMLAnchorElement;
          element.click = mockClick;
        }
        return element;
      });

      jest.spyOn(document.body, 'appendChild').mockImplementation(mockAppendChild);
      jest.spyOn(document.body, 'removeChild').mockImplementation(mockRemoveChild);
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    it('does not export when there are no messages', () => {
      const { result } = renderHook(() => useChat());

      act(() => {
        result.current.exportToMarkdown();
      });

      expect(mockCreateObjectURL).not.toHaveBeenCalled();
      expect(mockClick).not.toHaveBeenCalled();
    });

    it('exports messages with mode and sources to markdown', async () => {
      const { result } = renderHook(() => useChat());

      // Add messages with sources
      mockSendMessage.mockImplementation(
        async (message, history, onChunk, onComplete, onError, onMode, onSources) => {
          onMode('simple');
          onChunk('This is a response');
          onSources([
            {
              metadata: {
                document_title: 'Test Document',
                file_name: 'test.md',
                chunk_index: 0,
              },
              score: 0.95,
            },
          ]);
          onComplete();
        }
      );

      await act(async () => {
        await result.current.sendMessage('Test question');
      });

      await waitFor(() => {
        expect(result.current.messages).toHaveLength(2);
      });

      // Export
      act(() => {
        result.current.exportToMarkdown();
      });

      // Verify blob was created
      expect(mockCreateObjectURL).toHaveBeenCalledWith(expect.any(Blob));

      // Verify link was created and clicked
      expect(mockClick).toHaveBeenCalled();
      expect(createdLink.href).toBe('blob:mock-url');
      expect(createdLink.download).toMatch(/chat-export-\d{4}-\d{2}-\d{2}\.md/);

      // Verify cleanup
      expect(mockAppendChild).toHaveBeenCalled();
      expect(mockRemoveChild).toHaveBeenCalled();
      expect(mockRevokeObjectURL).toHaveBeenCalledWith('blob:mock-url');

      // Verify markdown content
      const blobCall = mockCreateObjectURL.mock.calls[0][0];
      const reader = new FileReader();
      const readPromise = new Promise((resolve) => {
        reader.onload = () => resolve(reader.result);
      });
      reader.readAsText(blobCall);
      const markdown = await readPromise;

      expect(markdown).toContain('# Chat Export');
      expect(markdown).toContain('## User');
      expect(markdown).toContain('Test question');
      expect(markdown).toContain('## Assistant');
      expect(markdown).toContain('[SIMPLE]');
      expect(markdown).toContain('This is a response');
      expect(markdown).toContain('### Sources');
      expect(markdown).toContain('**Test Document**');
      expect(markdown).toContain('File: test.md');
      expect(markdown).toContain('Chunk: 0');
      expect(markdown).toContain('Relevance: 95.0%');
    });

    it('exports messages without mode or sources', async () => {
      const { result } = renderHook(() => useChat());

      mockSendMessage.mockImplementation(async (message, history, onChunk, onComplete) => {
        onChunk('Simple response');
        onComplete();
      });

      await act(async () => {
        await result.current.sendMessage('Test question');
      });

      await waitFor(() => {
        expect(result.current.messages).toHaveLength(2);
      });

      act(() => {
        result.current.exportToMarkdown();
      });

      const blobCall = mockCreateObjectURL.mock.calls[0][0];
      const reader = new FileReader();
      const readPromise = new Promise((resolve) => {
        reader.onload = () => resolve(reader.result);
      });
      reader.readAsText(blobCall);
      const markdown = await readPromise;

      expect(markdown).toContain('## User');
      expect(markdown).toContain('## Assistant');
      expect(markdown).not.toContain('[SIMPLE]');
      expect(markdown).not.toContain('### Sources');
    });
  });
});
