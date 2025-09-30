import { render, screen } from '../../test-utils';
import { Message } from './Message';
import { createMockMessage } from '../../test-utils/mockData';

describe('Message Component', () => {
  it('renders user message correctly', () => {
    const userMessage = createMockMessage({
      content: 'Hello, this is a user message',
      sender: 'user',
    });

    render(<Message message={userMessage} />);

    expect(screen.getByText('Hello, this is a user message')).toBeInTheDocument();
    expect(screen.getByText('5:00 AM')).toBeInTheDocument();
  });

  it('renders assistant message correctly', () => {
    const assistantMessage = createMockMessage({
      content: 'Hello, this is an assistant message',
      sender: 'assistant',
    });

    render(<Message message={assistantMessage} />);

    expect(screen.getByText('Hello, this is an assistant message')).toBeInTheDocument();
    expect(screen.getByText('5:00 AM')).toBeInTheDocument();
  });

  it('applies correct CSS classes for user messages', () => {
    const userMessage = createMockMessage({
      content: 'User message',
      sender: 'user',
    });

    render(<Message message={userMessage} />);
    const messageElement = screen.getByText('User message').closest('.message');

    expect(messageElement).toHaveClass('message', 'user');
  });

  it('applies correct CSS classes for assistant messages', () => {
    const assistantMessage = createMockMessage({
      content: 'Assistant message',
      sender: 'assistant',
    });

    render(<Message message={assistantMessage} />);
    const messageElement = screen.getByText('Assistant message').closest('.message');

    expect(messageElement).toHaveClass('message', 'assistant');
  });

  it('shows streaming cursor when message is streaming', () => {
    const streamingMessage = createMockMessage({
      content: 'Streaming message',
      sender: 'assistant',
      isStreaming: true,
    });

    render(<Message message={streamingMessage} />);

    expect(screen.getByText('|')).toBeInTheDocument();
  });

  it('does not show streaming cursor when message is not streaming', () => {
    const normalMessage = createMockMessage({
      content: 'Normal message',
      sender: 'assistant',
      isStreaming: false,
    });

    render(<Message message={normalMessage} />);

    expect(screen.queryByText('|')).not.toBeInTheDocument();
  });

  it('formats timestamp correctly', () => {
    const message = createMockMessage({
      timestamp: new Date('2023-01-01T14:30:00Z'),
    });

    render(<Message message={message} />);

    expect(screen.getByText('7:30 AM')).toBeInTheDocument();
  });

  it('handles multiline content correctly', () => {
    const multilineMessage = createMockMessage({
      content: 'Line 1\nLine 2\nLine 3',
    });

    render(<Message message={multilineMessage} />);

    expect(screen.getByText(/Line 1.*Line 2.*Line 3/s)).toBeInTheDocument();
  });
});
