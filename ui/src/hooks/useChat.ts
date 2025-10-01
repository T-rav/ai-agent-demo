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
    let conversationHistory: Array<{ role: string; content: string }> = [];

    setState((prev) => {
      // Check if already loading
      if (prev.isLoading) return prev;

      shouldProceed = true;

      // Build conversation history from existing messages (before adding new ones)
      conversationHistory = prev.messages.map((msg) => ({
        role: msg.sender,
        content: msg.content,
      }));

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
        conversationHistory,
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
        },
        // On mode received (simple/research)
        (mode: string) => {
          setState((prev) => ({
            ...prev,
            messages: prev.messages.map((msg) =>
              msg.id === assistantMessageId ? { ...msg, mode: mode as 'simple' | 'research' } : msg
            ),
          }));
        },
        // On sources received
        (sources: any[]) => {
          setState((prev) => ({
            ...prev,
            messages: prev.messages.map((msg) =>
              msg.id === assistantMessageId ? { ...msg, sources } : msg
            ),
          }));
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

  const exportToMarkdown = useCallback(() => {
    if (state.messages.length === 0) return;

    let markdown = '# Chat Export\n\n';
    markdown += `*Exported on ${new Date().toLocaleString()}*\n\n---\n\n`;

    state.messages.forEach((message) => {
      const sender = message.sender === 'user' ? 'User' : 'Assistant';
      const timestamp = new Date(message.timestamp).toLocaleTimeString();
      
      // Add mode for assistant messages
      const modeText = message.mode ? ` [${message.mode.toUpperCase()}]` : '';
      markdown += `## ${sender} (${timestamp})${modeText}\n\n`;
      markdown += `${message.content}\n\n`;

      // Add sources if available
      if (message.sources && message.sources.length > 0) {
        markdown += `### Sources\n\n`;
        message.sources.forEach((source: any, index: number) => {
          const title = source.metadata?.document_title || source.title || 'Untitled';
          const fileName = source.metadata?.file_name || source.source || '';
          const chunkIndex = source.metadata?.chunk_index;
          const score = source.score;

          markdown += `${index + 1}. **${title}**\n`;
          if (fileName) markdown += `   - File: ${fileName}\n`;
          if (chunkIndex !== undefined) markdown += `   - Chunk: ${chunkIndex}\n`;
          if (score !== undefined) markdown += `   - Relevance: ${(score * 100).toFixed(1)}%\n`;
          if (source.url) markdown += `   - URL: ${source.url}\n`;
          markdown += '\n';
        });
      }

      markdown += '---\n\n';
    });

    // Create and download the file
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `chat-export-${new Date().toISOString().slice(0, 10)}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }, [state.messages]);

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    sendMessage,
    clearMessages,
    clearError,
    exportToMarkdown,
  };
};
