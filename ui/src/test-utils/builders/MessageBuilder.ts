/**
 * Fluent builder for creating Message test data.
 * Follows the pattern from Python projects: a().b().build()
 */
import { Message } from '../../types/chat';

export class MessageBuilder {
  private message: Message;

  constructor() {
    // Set sensible defaults
    this.message = {
      id: 'test-message-id',
      content: 'Test message content',
      sender: 'user',
      timestamp: new Date('2023-01-01T12:00:00Z'),
      isStreaming: false,
    };
  }

  withId(id: string): MessageBuilder {
    this.message.id = id;
    return this;
  }

  withContent(content: string): MessageBuilder {
    this.message.content = content;
    return this;
  }

  withSender(sender: 'user' | 'assistant'): MessageBuilder {
    this.message.sender = sender;
    return this;
  }

  asUser(): MessageBuilder {
    this.message.sender = 'user';
    return this;
  }

  asAssistant(): MessageBuilder {
    this.message.sender = 'assistant';
    return this;
  }

  withTimestamp(timestamp: Date): MessageBuilder {
    this.message.timestamp = timestamp;
    return this;
  }

  isStreaming(streaming: boolean = true): MessageBuilder {
    this.message.isStreaming = streaming;
    return this;
  }

  build(): Message {
    return { ...this.message };
  }
}

/**
 * Create a new message builder with user defaults.
 * Usage: aMessage().withContent("Hello").build()
 */
export const aMessage = (): MessageBuilder => {
  return new MessageBuilder();
};

/**
 * Create a new message builder with assistant defaults.
 * Usage: anAssistantMessage().withContent("Hi there").build()
 */
export const anAssistantMessage = (): MessageBuilder => {
  return new MessageBuilder().asAssistant();
};

/**
 * Create a streaming message builder.
 * Usage: aStreamingMessage().withContent("Typing...").build()
 */
export const aStreamingMessage = (): MessageBuilder => {
  return new MessageBuilder().isStreaming(true);
};
