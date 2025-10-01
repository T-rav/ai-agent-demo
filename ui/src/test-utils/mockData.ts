/**
 * Deprecated: Use builders and factories instead.
 *
 * Migration guide:
 * - Replace createMockMessage() with aMessage().build()
 * - Replace mockMessages with MessageFactory.createConversation()
 *
 * @deprecated Use test-utils/builders for fluent test data creation
 */
import { Message } from '../types/chat';
import { aMessage, anAssistantMessage } from './builders';

/**
 * @deprecated Use aMessage() builder instead
 */
export const createMockMessage = (overrides: Partial<Message> = {}): Message => {
  const builder = aMessage();

  if (overrides.id) builder.withId(overrides.id);
  if (overrides.content) builder.withContent(overrides.content);
  if (overrides.sender) builder.withSender(overrides.sender);
  if (overrides.timestamp) builder.withTimestamp(overrides.timestamp);
  if (overrides.isStreaming !== undefined) builder.isStreaming(overrides.isStreaming);

  return builder.build();
};

/**
 * @deprecated Use MessageFactory.createConversation() instead
 */
export const mockMessages: Message[] = [
  aMessage()
    .withId('1')
    .withContent('Hello, how are you?')
    .withTimestamp(new Date('2023-01-01T12:00:00Z'))
    .build(),
  anAssistantMessage()
    .withId('2')
    .withContent('I am doing well, thank you for asking! How can I help you today?')
    .withTimestamp(new Date('2023-01-01T12:01:00Z'))
    .build(),
  aMessage()
    .withId('3')
    .withContent('Can you help me with a coding question?')
    .withTimestamp(new Date('2023-01-01T12:02:00Z'))
    .build(),
];
