import { render, screen } from '../../test-utils';
import { MessageList } from './MessageList';
import { mockMessages } from '../../test-utils/mockData';

// Mock the Message component to simplify testing
jest.mock('../Message/Message', () => ({
  Message: ({ message }: { message: any }) => (
    <div data-testid={`message-${message.id}`}>
      {message.content} - {message.sender}
    </div>
  ),
}));

describe('MessageList Component', () => {
  it('renders empty state when no messages', () => {
    render(<MessageList messages={[]} isLoading={false} />);

    expect(screen.getByText('Start a conversation')).toBeInTheDocument();
    expect(
      screen.getByText('Send a message to begin chatting with the AI assistant.')
    ).toBeInTheDocument();
    expect(screen.getByText('💬')).toBeInTheDocument();
  });

  it('renders messages when provided', () => {
    render(<MessageList messages={mockMessages} isLoading={false} />);

    expect(screen.getByTestId('message-1')).toBeInTheDocument();
    expect(screen.getByTestId('message-2')).toBeInTheDocument();
    expect(screen.getByTestId('message-3')).toBeInTheDocument();

    expect(screen.getByText('Hello, how are you? - user')).toBeInTheDocument();
    expect(
      screen.getByText(
        'I am doing well, thank you for asking! How can I help you today? - assistant'
      )
    ).toBeInTheDocument();
    expect(screen.getByText('Can you help me with a coding question? - user')).toBeInTheDocument();
  });

  it('shows typing indicator when loading', () => {
    render(<MessageList messages={mockMessages} isLoading={true} />);

    const typingIndicator = screen.getByRole('generic', { hidden: true });
    expect(typingIndicator.querySelector('.typing-indicator')).toBeInTheDocument();
  });

  it('does not show typing indicator when not loading', () => {
    render(<MessageList messages={mockMessages} isLoading={false} />);

    expect(screen.queryByText('.typing-indicator')).not.toBeInTheDocument();
  });

  it('applies correct CSS classes for empty state', () => {
    render(<MessageList messages={[]} isLoading={false} />);

    const emptyState = screen.getByText('Start a conversation');
    const messageList = emptyState.closest('.message-list');
    expect(messageList).toHaveClass('empty');
  });

  it('does not apply empty class when messages exist', () => {
    render(<MessageList messages={mockMessages} isLoading={false} />);

    const firstMessage = screen.getByText('Hello, AI!');
    const messageList = firstMessage.closest('.message-list');
    expect(messageList).not.toHaveClass('empty');
  });

  it('renders messages in correct order', () => {
    render(<MessageList messages={mockMessages} isLoading={false} />);

    const messages = screen.getAllByTestId(/^message-/);
    expect(messages).toHaveLength(3);
    expect(messages[0]).toHaveAttribute('data-testid', 'message-1');
    expect(messages[1]).toHaveAttribute('data-testid', 'message-2');
    expect(messages[2]).toHaveAttribute('data-testid', 'message-3');
  });

  it('handles single message correctly', () => {
    const singleMessage = [mockMessages[0]];
    render(<MessageList messages={singleMessage} isLoading={false} />);

    expect(screen.getByTestId('message-1')).toBeInTheDocument();
    expect(screen.queryByTestId('message-2')).not.toBeInTheDocument();
    expect(screen.queryByText('Start a conversation')).not.toBeInTheDocument();
  });

  it('shows both messages and typing indicator when loading with messages', () => {
    render(<MessageList messages={mockMessages} isLoading={true} />);

    // Messages should still be visible
    expect(screen.getByTestId('message-1')).toBeInTheDocument();
    expect(screen.getByTestId('message-2')).toBeInTheDocument();
    expect(screen.getByTestId('message-3')).toBeInTheDocument();

    // Typing indicator should also be visible
    const typingIndicator = screen.getByRole('status');
    expect(typingIndicator).toHaveClass('typing-indicator');
  });
});
