import { render, screen, waitFor } from '../../test-utils';
import userEvent from '@testing-library/user-event';
import { MessageInput } from './MessageInput';

describe('MessageInput Component', () => {
  const mockOnSendMessage = jest.fn();

  beforeEach(() => {
    mockOnSendMessage.mockClear();
  });

  it('renders with default placeholder', () => {
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    expect(screen.getByPlaceholderText('Type your message...')).toBeInTheDocument();
  });

  it('renders with custom placeholder', () => {
    render(<MessageInput onSendMessage={mockOnSendMessage} placeholder="Custom placeholder" />);

    expect(screen.getByPlaceholderText('Custom placeholder')).toBeInTheDocument();
  });

  it('calls onSendMessage when form is submitted with valid message', async () => {
    const user = userEvent.setup();
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /send message/i });

    await user.type(textarea, 'Hello, world!');
    await user.click(sendButton);

    expect(mockOnSendMessage).toHaveBeenCalledWith('Hello, world!');
  });

  it('calls onSendMessage when Enter key is pressed', async () => {
    const user = userEvent.setup();
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const textarea = screen.getByPlaceholderText('Type your message...');

    await user.type(textarea, 'Hello, world!');
    await user.keyboard('{Enter}');

    expect(mockOnSendMessage).toHaveBeenCalledWith('Hello, world!');
  });

  it('does not call onSendMessage when Shift+Enter is pressed', async () => {
    const user = userEvent.setup();
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const textarea = screen.getByPlaceholderText('Type your message...');

    await user.type(textarea, 'Hello, world!');
    await user.keyboard('{Shift>}{Enter}{/Shift}');

    expect(mockOnSendMessage).not.toHaveBeenCalled();
    expect(textarea).toHaveValue('Hello, world!\n');
  });

  it('clears input after sending message', async () => {
    const user = userEvent.setup();
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const textarea = screen.getByPlaceholderText('Type your message...');

    await user.type(textarea, 'Hello, world!');
    await user.keyboard('{Enter}');

    await waitFor(() => {
      expect(textarea).toHaveValue('');
    });
  });

  it('does not send empty or whitespace-only messages', async () => {
    const user = userEvent.setup();
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const textarea = screen.getByPlaceholderText('Type your message...');

    // Test empty message
    await user.keyboard('{Enter}');
    expect(mockOnSendMessage).not.toHaveBeenCalled();

    // Test whitespace-only message
    await user.type(textarea, '   ');
    await user.keyboard('{Enter}');
    expect(mockOnSendMessage).not.toHaveBeenCalled();
  });

  it('trims whitespace from messages before sending', async () => {
    const user = userEvent.setup();
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const textarea = screen.getByPlaceholderText('Type your message...');

    await user.type(textarea, '  Hello, world!  ');
    await user.keyboard('{Enter}');

    expect(mockOnSendMessage).toHaveBeenCalledWith('Hello, world!');
  });

  it('disables input and button when disabled prop is true', () => {
    render(<MessageInput onSendMessage={mockOnSendMessage} disabled />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /send message/i });

    expect(textarea).toBeDisabled();
    expect(sendButton).toBeDisabled();
  });

  it('disables send button when input is empty', () => {
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const sendButton = screen.getByRole('button', { name: /send message/i });

    expect(sendButton).toBeDisabled();
  });

  it('enables send button when input has content', async () => {
    const user = userEvent.setup();
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /send message/i });

    await user.type(textarea, 'Hello');

    expect(sendButton).not.toBeDisabled();
  });

  it('handles form submission correctly', async () => {
    const user = userEvent.setup();
    render(<MessageInput onSendMessage={mockOnSendMessage} />);

    const textarea = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /send message/i });

    await user.type(textarea, 'Test message');
    await user.click(sendButton);

    expect(mockOnSendMessage).toHaveBeenCalledWith('Test message');
  });
});
