import { Message } from '../types/chat';

export const createMockMessage = (overrides: Partial<Message> = {}): Message => ({
  id: 'test-message-id',
  content: 'Test message content',
  sender: 'user',
  timestamp: new Date('2023-01-01T12:00:00Z'),
  isStreaming: false,
  ...overrides,
});

export const mockMessages: Message[] = [
  createMockMessage({
    id: '1',
    content: 'Hello, how are you?',
    sender: 'user',
    timestamp: new Date('2023-01-01T12:00:00Z'),
  }),
  createMockMessage({
    id: '2',
    content: 'I am doing well, thank you for asking! How can I help you today?',
    sender: 'assistant',
    timestamp: new Date('2023-01-01T12:01:00Z'),
  }),
  createMockMessage({
    id: '3',
    content: 'Can you help me with a coding question?',
    sender: 'user',
    timestamp: new Date('2023-01-01T12:02:00Z'),
  }),
];
