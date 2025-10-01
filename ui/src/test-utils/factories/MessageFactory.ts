/**
 * Factory for creating message arrays and common test scenarios.
 * Separate from builders - factories create complete test doubles.
 */
import { Message } from '../../types/chat';
import { aMessage, anAssistantMessage } from '../builders';

export class MessageFactory {
  /**
   * Create a conversation with alternating user/assistant messages.
   */
  static createConversation(messageCount: number = 4): Message[] {
    const messages: Message[] = [];

    for (let i = 0; i < messageCount; i++) {
      const isUser = i % 2 === 0;
      const timestamp = new Date('2023-01-01T12:00:00Z');
      timestamp.setMinutes(timestamp.getMinutes() + i);

      const message = isUser
        ? aMessage()
            .withId(`msg-${i + 1}`)
            .withContent(`User message ${i + 1}`)
            .withTimestamp(timestamp)
            .build()
        : anAssistantMessage()
            .withId(`msg-${i + 1}`)
            .withContent(`Assistant response ${i + 1}`)
            .withTimestamp(timestamp)
            .build();

      messages.push(message);
    }

    return messages;
  }

  /**
   * Create a conversation about a specific topic.
   */
  static createTopicConversation(topic: string): Message[] {
    return [
      aMessage()
        .withId('1')
        .withContent(`Tell me about ${topic}`)
        .withTimestamp(new Date('2023-01-01T12:00:00Z'))
        .build(),
      anAssistantMessage()
        .withId('2')
        .withContent(`Here's information about ${topic}...`)
        .withTimestamp(new Date('2023-01-01T12:01:00Z'))
        .build(),
    ];
  }

  /**
   * Create a single streaming message (used during active typing).
   */
  static createStreamingMessage(): Message {
    return aMessage().asAssistant().withContent('').isStreaming(true).build();
  }

  /**
   * Create an empty conversation.
   */
  static createEmptyConversation(): Message[] {
    return [];
  }
}
