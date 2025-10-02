import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export class ChatService {
  private static instance: ChatService;

  public static getInstance(): ChatService {
    if (!ChatService.instance) {
      ChatService.instance = new ChatService();
    }
    return ChatService.instance;
  }

  /**
   * Send a message to the LLM and handle streaming response
   */
  public async sendMessage(
    message: string,
    conversationHistory: Array<{ role: string; content: string }>,
    onChunk: (chunk: string) => void,
    onComplete: () => void,
    onError: (error: string) => void,
    onMode?: (mode: string) => void,
    onSources?: (sources: any[]) => void
  ): Promise<void> {
    // Guard against duplicate onComplete calls
    let completed = false;
    const safeOnComplete = () => {
      if (completed) return;
      completed = true;
      onComplete();
    };

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          conversation_history: conversationHistory,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body reader available');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          safeOnComplete();
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.trim() === '') continue;

          try {
            // Handle Server-Sent Events format
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                safeOnComplete();
                return;
              }

              const parsed = JSON.parse(data);

              // Handle different chunk types
              if (parsed.type === 'token' && parsed.content) {
                onChunk(parsed.content);
              } else if (parsed.type === 'step' && parsed.content) {
                // Emit mode/step information (like "simple" or "research")
                if (onMode) {
                  onMode(parsed.content);
                }
              } else if (parsed.type === 'sources' && parsed.sources) {
                // Emit sources
                if (onSources) {
                  onSources(parsed.sources);
                }
              } else if (parsed.type === 'done') {
                safeOnComplete();
                return;
              } else if (parsed.type === 'error') {
                onError(parsed.error || 'Unknown error');
                return;
              }
            }
          } catch (parseError) {
            // eslint-disable-next-line no-console
            console.warn('Failed to parse streaming chunk:', parseError);
          }
        }
      }
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error('Chat service error:', error);
      onError(error instanceof Error ? error.message : 'Unknown error occurred');
    }
  }

  /**
   * Fallback method for non-streaming requests
   */
  public async sendMessageSync(message: string): Promise<string> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        message,
      });

      return response.data.response || '';
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error('Sync chat service error:', error);
      throw new Error(
        axios.isAxiosError(error)
          ? error.response?.data?.error || error.message
          : 'Unknown error occurred'
      );
    }
  }
}
