import { render, screen, waitFor } from '../../test-utils';
import userEvent from '@testing-library/user-event';
import { ChatContainer } from './ChatContainer';
import { ChatService } from '../../services/chatService';

// Mock the ChatService
jest.mock('../../services/chatService');
const mockChatService = ChatService as jest.Mocked<typeof ChatService>;

// Mock uuid
jest.mock('uuid', () => ({
  v4: jest.fn(() => 'mock-uuid-' + Math.random()),
}));

describe('ChatContainer Component', () => {
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

  it('renders with default title', () => {
    render(<ChatContainer />);

    expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<ChatContainer title="Custom Chat Bot" />);

    expect(screen.getByText('Custom Chat Bot')).toBeInTheDocument();
  });

  it('shows empty state initially', () => {
    render(<ChatContainer />);

    expect(screen.getByText('Start a conversation')).toBeInTheDocument();
    expect(
      screen.getByText('Send a message to begin chatting with the AI assistant.')
    ).toBeInTheDocument();
  });

  it('does not show clear button when no messages', () => {
    render(<ChatContainer />);

    expect(screen.queryByText('Clear')).not.toBeInTheDocument();
  });

  it('handles successful message sending', async () => {
    const user = userEvent.setup();

    mockSendMessage.mockImplementation(async (message, onChunk, onComplete) => {
      // Wait for initial messages to be added to state
      await new Promise((resolve) => setTimeout(resolve, 100));
      onChunk('Hello');
      onChunk(' there!');
      onComplete();
    });

    render(<ChatContainer />);

    const input = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /send message/i });

    await user.type(input, 'Hello, AI!');
    await user.click(sendButton);

    // Should show user message
    await waitFor(() => {
      expect(screen.getByText('Hello, AI!')).toBeInTheDocument();
    });

    // Should show assistant response
    await waitFor(
      () => {
        expect(screen.getByText('Hello there!')).toBeInTheDocument();
      },
      { timeout: 1000 }
    );

    // Clear button should now be visible
    expect(screen.getByText('Clear')).toBeInTheDocument();
  });

  it('shows loading state during message sending', async () => {
    const user = userEvent.setup();

    let resolveMessage: () => void;
    mockSendMessage.mockImplementation(async (message, onChunk, onComplete) => {
      return new Promise<void>((resolve) => {
        resolveMessage = () => {
          onComplete();
          resolve();
        };
      });
    });

    render(<ChatContainer />);

    const input = screen.getByPlaceholderText('Type your message...');

    await user.type(input, 'Hello, AI!');
    await user.keyboard('{Enter}');

    // Should show loading placeholder
    await waitFor(() => {
      expect(screen.getByPlaceholderText('AI is responding...')).toBeInTheDocument();
    });

    // Input should be disabled
    expect(screen.getByPlaceholderText('AI is responding...')).toBeDisabled();

    // Resolve the message
    resolveMessage!();

    // Should return to normal state
    await waitFor(() => {
      expect(screen.getByPlaceholderText('Type your message...')).toBeInTheDocument();
    });
  });

  it('handles errors correctly', async () => {
    const user = userEvent.setup();

    mockSendMessage.mockImplementation(async (message, onChunk, onComplete, onError) => {
      onError('Network connection failed');
    });

    render(<ChatContainer />);

    const input = screen.getByPlaceholderText('Type your message...');

    await user.type(input, 'Hello, AI!');
    await user.keyboard('{Enter}');

    // Should show error banner
    await waitFor(() => {
      expect(screen.getByText('Network connection failed')).toBeInTheDocument();
    });

    // Should show error icon
    expect(screen.getByText('⚠️')).toBeInTheDocument();
  });

  it('allows dismissing errors', async () => {
    const user = userEvent.setup();

    mockSendMessage.mockImplementation(async (message, onChunk, onComplete, onError) => {
      onError('Test error');
    });

    render(<ChatContainer />);

    const input = screen.getByPlaceholderText('Type your message...');

    await user.type(input, 'Hello, AI!');
    await user.keyboard('{Enter}');

    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText('Test error')).toBeInTheDocument();
    });

    // Click dismiss button
    const dismissButton = screen.getByRole('button', { name: /dismiss error/i });
    await user.click(dismissButton);

    // Error should be gone
    await waitFor(() => {
      expect(screen.queryByText('Test error')).not.toBeInTheDocument();
    });
  });

  it('clears messages when clear button is clicked', async () => {
    const user = userEvent.setup();

    mockSendMessage.mockImplementation(async (message, onChunk, onComplete) => {
      // Wait for initial messages to be added to state
      await new Promise((resolve) => setTimeout(resolve, 100));
      onChunk('Response');
      onComplete();
    });

    render(<ChatContainer />);

    const input = screen.getByPlaceholderText('Type your message...');

    // Send a message first
    await user.type(input, 'Hello, AI!');
    await user.keyboard('{Enter}');

    // Wait for messages to appear
    await waitFor(() => {
      expect(screen.getByText('Hello, AI!')).toBeInTheDocument();
    });
    await waitFor(
      () => {
        expect(screen.getByText('Response')).toBeInTheDocument();
      },
      { timeout: 1000 }
    );

    // Click clear button
    const clearButton = screen.getByText('Clear');
    await user.click(clearButton);

    // Should return to empty state
    await waitFor(() => {
      expect(screen.getByText('Start a conversation')).toBeInTheDocument();
    });

    // Messages should be gone
    expect(screen.queryByText('Hello, AI!')).not.toBeInTheDocument();
    expect(screen.queryByText('Response')).not.toBeInTheDocument();

    // Clear button should be hidden
    expect(screen.queryByText('Clear')).not.toBeInTheDocument();
  });

  it('handles streaming responses correctly', async () => {
    const user = userEvent.setup();

    mockSendMessage.mockImplementation(async (message, onChunk, onComplete) => {
      // Wait for initial messages to be added to state
      await new Promise((resolve) => setTimeout(resolve, 100));
      onChunk('Once upon a time');
      onChunk(', there was a brave knight');
      onComplete();
    });

    render(<ChatContainer />);

    const input = screen.getByPlaceholderText('Type your message...');

    await user.type(input, 'Tell me a story');
    await user.keyboard('{Enter}');

    // Wait for user message
    await waitFor(() => {
      expect(screen.getByText('Tell me a story')).toBeInTheDocument();
    });

    // Should show the streamed response
    await waitFor(
      () => {
        expect(screen.getByText('Once upon a time, there was a brave knight')).toBeInTheDocument();
      },
      { timeout: 1000 }
    );
  });

  it('prevents sending messages while loading', async () => {
    const user = userEvent.setup();

    mockSendMessage.mockImplementation(async () => {
      // Never complete to keep loading state
      return new Promise(() => {});
    });

    render(<ChatContainer />);

    const input = screen.getByPlaceholderText('Type your message...');

    // Send first message
    await user.type(input, 'First message');
    await user.keyboard('{Enter}');

    // Wait for loading state
    await waitFor(() => {
      expect(screen.getByPlaceholderText('AI is responding...')).toBeDisabled();
    });

    // Try to send second message - should not work
    const disabledInput = screen.getByPlaceholderText('AI is responding...');
    await user.type(disabledInput, 'Second message');

    // Input should remain disabled and empty (can't type into disabled input)
    expect(disabledInput).toBeDisabled();
    expect(disabledInput).toHaveValue('');

    // Should only have been called once
    expect(mockSendMessage).toHaveBeenCalledTimes(1);
  });
});
