import { ChatService } from './chatService';
import axios from 'axios';

// Mock fetch
global.fetch = jest.fn();
const mockFetch = fetch as jest.MockedFunction<typeof fetch>;

// Mock axios
jest.mock('axios');
const mockAxios = axios as jest.Mocked<typeof axios>;

describe('ChatService', () => {
  let chatService: ChatService;

  beforeEach(() => {
    chatService = ChatService.getInstance();
    jest.clearAllMocks();
  });

  describe('getInstance', () => {
    it('returns singleton instance', () => {
      const instance1 = ChatService.getInstance();
      const instance2 = ChatService.getInstance();
      expect(instance1).toBe(instance2);
    });
  });

  describe('sendMessage', () => {
    it('handles successful streaming response', async () => {
      const mockReader = {
        read: jest
          .fn()
          .mockResolvedValueOnce({
            done: false,
            value: new TextEncoder().encode('data: {"content":"Hello"}\n'),
          })
          .mockResolvedValueOnce({
            done: false,
            value: new TextEncoder().encode('data: {"content":" world!"}\n'),
          })
          .mockResolvedValueOnce({
            done: true,
            value: undefined,
          }),
      };

      const mockResponse = {
        ok: true,
        body: {
          getReader: () => mockReader,
        },
      };

      mockFetch.mockResolvedValue(mockResponse as any);

      const onChunk = jest.fn();
      const onComplete = jest.fn();
      const onError = jest.fn();

      await chatService.sendMessage('Test message', [], onChunk, onComplete, onError);

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'Test message' }),
      });

      expect(onChunk).toHaveBeenCalledWith('Hello');
      expect(onChunk).toHaveBeenCalledWith(' world!');
      expect(onComplete).toHaveBeenCalled();
      expect(onError).not.toHaveBeenCalled();
    });

    it('handles [DONE] signal', async () => {
      const mockReader = {
        read: jest
          .fn()
          .mockResolvedValueOnce({
            done: false,
            value: new TextEncoder().encode('data: {"content":"Hello"}\n'),
          })
          .mockResolvedValueOnce({
            done: false,
            value: new TextEncoder().encode('data: [DONE]\n'),
          }),
      };

      const mockResponse = {
        ok: true,
        body: {
          getReader: () => mockReader,
        },
      };

      mockFetch.mockResolvedValue(mockResponse as any);

      const onChunk = jest.fn();
      const onComplete = jest.fn();
      const onError = jest.fn();

      await chatService.sendMessage('Test message', [], onChunk, onComplete, onError);

      expect(onChunk).toHaveBeenCalledWith('Hello');
      expect(onComplete).toHaveBeenCalled();
      expect(onError).not.toHaveBeenCalled();
    });

    it('handles non-JSON streaming data as plain text', async () => {
      const mockReader = {
        read: jest
          .fn()
          .mockResolvedValueOnce({
            done: false,
            value: new TextEncoder().encode('Plain text response\n'),
          })
          .mockResolvedValueOnce({
            done: true,
            value: undefined,
          }),
      };

      const mockResponse = {
        ok: true,
        body: {
          getReader: () => mockReader,
        },
      };

      mockFetch.mockResolvedValue(mockResponse as any);

      const onChunk = jest.fn();
      const onComplete = jest.fn();
      const onError = jest.fn();

      await chatService.sendMessage('Test message', [], onChunk, onComplete, onError);

      expect(onChunk).toHaveBeenCalledWith('Plain text response');
      expect(onComplete).toHaveBeenCalled();
      expect(onError).not.toHaveBeenCalled();
    });

    it('handles HTTP errors', async () => {
      const mockResponse = {
        ok: false,
        status: 500,
      };

      mockFetch.mockResolvedValue(mockResponse as any);

      const onChunk = jest.fn();
      const onComplete = jest.fn();
      const onError = jest.fn();

      await chatService.sendMessage('Test message', [], onChunk, onComplete, onError);

      expect(onError).toHaveBeenCalledWith('HTTP error! status: 500');
      expect(onChunk).not.toHaveBeenCalled();
      expect(onComplete).not.toHaveBeenCalled();
    });

    it('handles missing response body', async () => {
      const mockResponse = {
        ok: true,
        body: null,
      };

      mockFetch.mockResolvedValue(mockResponse as any);

      const onChunk = jest.fn();
      const onComplete = jest.fn();
      const onError = jest.fn();

      await chatService.sendMessage('Test message', [], onChunk, onComplete, onError);

      expect(onError).toHaveBeenCalledWith('No response body reader available');
      expect(onChunk).not.toHaveBeenCalled();
      expect(onComplete).not.toHaveBeenCalled();
    });

    it('handles network errors', async () => {
      mockFetch.mockRejectedValue(new Error('Network error'));

      const onChunk = jest.fn();
      const onComplete = jest.fn();
      const onError = jest.fn();

      await chatService.sendMessage('Test message', [], onChunk, onComplete, onError);

      expect(onError).toHaveBeenCalledWith('Network error');
      expect(onChunk).not.toHaveBeenCalled();
      expect(onComplete).not.toHaveBeenCalled();
    });
  });

  describe('sendMessageSync', () => {
    it('handles successful sync response', async () => {
      const mockResponse = {
        data: {
          response: 'Hello, this is a sync response!',
        },
      };

      mockAxios.post.mockResolvedValue(mockResponse);

      const result = await chatService.sendMessageSync('Test message');

      expect(mockAxios.post).toHaveBeenCalledWith('http://localhost:8000/api/chat', {
        message: 'Test message',
      });
      expect(result).toBe('Hello, this is a sync response!');
    });

    it('handles empty response', async () => {
      const mockResponse = {
        data: {},
      };

      mockAxios.post.mockResolvedValue(mockResponse);

      const result = await chatService.sendMessageSync('Test message');

      expect(result).toBe('');
    });

    it('handles axios errors with response', async () => {
      const mockError = {
        response: {
          data: {
            error: 'Server error message',
          },
        },
      };

      mockAxios.post.mockRejectedValue(mockError);
      mockAxios.isAxiosError.mockReturnValue(true);

      await expect(chatService.sendMessageSync('Test message')).rejects.toThrow(
        'Server error message'
      );
    });

    it('handles axios errors without response data', async () => {
      const mockError = {
        message: 'Network Error',
        response: {
          data: {},
        },
      };

      mockAxios.post.mockRejectedValue(mockError);
      mockAxios.isAxiosError.mockReturnValue(true);

      await expect(chatService.sendMessageSync('Test message')).rejects.toThrow('Network Error');
    });

    it('handles non-axios errors', async () => {
      const mockError = new Error('Generic error');

      mockAxios.post.mockRejectedValue(mockError);
      mockAxios.isAxiosError.mockReturnValue(false);

      await expect(chatService.sendMessageSync('Test message')).rejects.toThrow(
        'Unknown error occurred'
      );
    });
  });

  describe('API URL configuration', () => {
    it('uses environment variable when available', () => {
      const originalEnv = process.env.REACT_APP_API_URL;
      process.env.REACT_APP_API_URL = 'https://custom-api.com';

      // Need to re-import to get new environment variable
      jest.resetModules();
      const { ChatService: NewChatService } = require('./chatService');
      const newService = NewChatService.getInstance();

      mockFetch.mockResolvedValue({
        ok: true,
        body: {
          getReader: () => ({
            read: jest.fn().mockResolvedValue({ done: true }),
          }),
        },
      } as any);

      newService.sendMessage('test', jest.fn(), jest.fn(), jest.fn());

      expect(mockFetch).toHaveBeenCalledWith(
        'https://custom-api.com/api/chat/stream',
        expect.any(Object)
      );

      // Restore original environment
      process.env.REACT_APP_API_URL = originalEnv;
    });
  });
});
