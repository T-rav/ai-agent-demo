import { useState, useCallback, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Message, ChatState } from '../types/chat';
import { ChatService } from '../services/chatService';

export const useChat = () => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
  });

  const chatService = useRef(ChatService.getInstance());
  const currentStreamingMessageId = useRef<string | null>(null);

  const addMessage = useCallback((message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: uuidv4(),
      timestamp: new Date(),
    };

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, newMessage],
      error: null,
    }));

    return newMessage.id;
  }, []);

  const updateMessage = useCallback((id: string, updates: Partial<Message>) => {
    setState((prev) => ({
      ...prev,
      messages: prev.messages.map((msg) => (msg.id === id ? { ...msg, ...updates } : msg)),
    }));
  }, []);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || state.isLoading) return;

      // Add user message
      addMessage({
        content: content.trim(),
        sender: 'user',
      });

      // Add initial assistant message for streaming
      const assistantMessageId = addMessage({
        content: '',
        sender: 'assistant',
        isStreaming: true,
      });

      currentStreamingMessageId.current = assistantMessageId;

      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        await chatService.current.sendMessage(
          content.trim(),
          // On chunk received
          (chunk: string) => {
            if (currentStreamingMessageId.current) {
              setState((prev) => ({
                ...prev,
                messages: prev.messages.map((msg) =>
                  msg.id === currentStreamingMessageId.current
                    ? { ...msg, content: msg.content + chunk }
                    : msg
                ),
              }));
            }
          },
          // On complete
          () => {
            if (currentStreamingMessageId.current) {
              updateMessage(currentStreamingMessageId.current, {
                isStreaming: false,
              });
            }
            currentStreamingMessageId.current = null;
            setState((prev) => ({ ...prev, isLoading: false }));
          },
          // On error
          (error: string) => {
            setState((prev) => ({
              ...prev,
              isLoading: false,
              error,
            }));

            // Remove the empty streaming message on error
            if (currentStreamingMessageId.current) {
              setState((prev) => ({
                ...prev,
                messages: prev.messages.filter(
                  (msg) => msg.id !== currentStreamingMessageId.current
                ),
              }));
            }
            currentStreamingMessageId.current = null;
          }
        );
      } catch (error) {
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: error instanceof Error ? error.message : 'Unknown error occurred',
        }));

        // Remove the empty streaming message on error
        if (currentStreamingMessageId.current) {
          setState((prev) => ({
            ...prev,
            messages: prev.messages.filter((msg) => msg.id !== currentStreamingMessageId.current),
          }));
        }
        currentStreamingMessageId.current = null;
      }
    },
    [state.isLoading, addMessage, updateMessage]
  );

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
