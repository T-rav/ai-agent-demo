import { render, screen, aMessage, anAssistantMessage } from '../../test-utils';
import { Message } from './Message';

describe('Message Component', () => {
  it('renders user message correctly', () => {
    // Use fluent builder pattern
    const userMessage = aMessage().withContent('Hello, this is a user message').asUser().build();

    render(<Message message={userMessage} />);

    expect(screen.getByText('Hello, this is a user message')).toBeInTheDocument();
    // Check that timestamp is rendered (format varies by timezone)
    expect(screen.getByText(/\d{1,2}:\d{2}\s[AP]M/)).toBeInTheDocument();
  });

  it('renders assistant message correctly', () => {
    // Use fluent builder pattern with assistant helper
    const assistantMessage = anAssistantMessage()
      .withContent('Hello, this is an assistant message')
      .build();

    render(<Message message={assistantMessage} />);

    expect(screen.getByText('Hello, this is an assistant message')).toBeInTheDocument();
    // Check that timestamp is rendered (format varies by timezone)
    expect(screen.getByText(/\d{1,2}:\d{2}\s[AP]M/)).toBeInTheDocument();
  });

  it('applies correct CSS classes for user messages', () => {
    const userMessage = aMessage().withContent('User message').asUser().build();

    render(<Message message={userMessage} />);
    const messageElement = screen.getByText('User message').closest('.message');

    expect(messageElement).toHaveClass('message', 'user');
  });

  it('applies correct CSS classes for assistant messages', () => {
    const assistantMessage = anAssistantMessage().withContent('Assistant message').build();

    render(<Message message={assistantMessage} />);
    const messageElement = screen.getByText('Assistant message').closest('.message');

    expect(messageElement).toHaveClass('message', 'assistant');
  });

  it('shows typing dots when streaming with no content', () => {
    const streamingMessage = anAssistantMessage().withContent('').isStreaming(true).build();

    render(<Message message={streamingMessage} />);

    const typingDots = document.querySelector('.typing-dots');
    expect(typingDots).toBeInTheDocument();
    expect(typingDots?.querySelectorAll('span')).toHaveLength(3);
  });

  it('shows streaming cursor when message is streaming with content', () => {
    const streamingMessage = anAssistantMessage()
      .withContent('Streaming message')
      .isStreaming(true)
      .build();

    render(<Message message={streamingMessage} />);

    expect(screen.getByText('|')).toBeInTheDocument();
  });

  it('does not show streaming cursor when message is not streaming', () => {
    const normalMessage = anAssistantMessage()
      .withContent('Normal message')
      .isStreaming(false)
      .build();

    render(<Message message={normalMessage} />);

    expect(screen.queryByText('|')).not.toBeInTheDocument();
  });

  it('formats timestamp correctly', () => {
    const message = aMessage().withTimestamp(new Date('2023-01-01T14:30:00Z')).build();

    render(<Message message={message} />);

    // Check that timestamp is rendered in correct format (actual time varies by timezone)
    expect(screen.getByText(/\d{1,2}:\d{2}\s[AP]M/)).toBeInTheDocument();
  });

  it('handles multiline content correctly', () => {
    const multilineMessage = aMessage().withContent('Line 1\nLine 2\nLine 3').build();

    render(<Message message={multilineMessage} />);

    expect(screen.getByText(/Line 1.*Line 2.*Line 3/s)).toBeInTheDocument();
  });
});
