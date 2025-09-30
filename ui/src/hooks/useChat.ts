import { useState, useCallback, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { ChatState } from '../types/chat';
import { ChatService } from '../services/chatService';

export const useChat = () => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
  });

  const chatService = useRef(ChatService.getInstance());
  const currentStreamingMessageId = useRef<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    const trimmedContent = content.trim();
    if (!trimmedContent) return;

    // Create IDs upfront
    const userMessageId = uuidv4();
    const assistantMessageId = uuidv4();

    // Single atomic state update to add both messages and set loading
    let shouldProceed = false;
    setState((prev) => {
      // Check if already loading
      if (prev.isLoading) return prev;

      shouldProceed = true;
      return {
        ...prev,
        messages: [
          ...prev.messages,
          {
            id: userMessageId,
            content: trimmedContent,
            sender: 'user' as const,
            timestamp: new Date(),
          },
          {
            id: assistantMessageId,
            content: '',
            sender: 'assistant' as const,
            timestamp: new Date(),
            isStreaming: true,
          },
        ],
        isLoading: true,
        error: null,
      };
    });

    if (!shouldProceed) return;

    currentStreamingMessageId.current = assistantMessageId;

    // Track if error was handled via callback to avoid redundant cleanup
    let errorHandled = false;

    try {
      await chatService.current.sendMessage(
        trimmedContent,
        // On chunk received
        (chunk: string) => {
          setState((prev) => ({
            ...prev,
            messages: prev.messages.map((msg) =>
              msg.id === assistantMessageId ? { ...msg, content: msg.content + chunk } : msg
            ),
          }));
        },
        // On complete
        () => {
          setState((prev) => ({
            ...prev,
            messages: prev.messages.map((msg) =>
              msg.id === assistantMessageId ? { ...msg, isStreaming: false } : msg
            ),
            isLoading: false,
          }));
          currentStreamingMessageId.current = null;
        },
        // On error - handled via callback
        (error: string) => {
          errorHandled = true;

          setState((prev) => ({
            ...prev,
            messages: prev.messages.filter((msg) => msg.id !== assistantMessageId),
            isLoading: false,
            error,
          }));
          currentStreamingMessageId.current = null;
        }
      );
    } catch (error) {
      // Only handle synchronous errors that weren't already handled via callback
      if (!errorHandled) {
        setState((prev) => ({
          ...prev,
          messages: prev.messages.filter((msg) => msg.id !== assistantMessageId),
          isLoading: false,
          error: error instanceof Error ? error.message : 'Unknown error occurred',
        }));
        currentStreamingMessageId.current = null;
      }
    }
  }, []);

  const clearMessages = useCallback(() => {
    setState({
      messages: [],
      isLoading: false,
      error: null,
    });
    currentStreamingMessageId.current = null;
  }, []);

  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    sendMessage,
    clearMessages,
    clearError,
  };
};
