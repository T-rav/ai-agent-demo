export interface Source {
  content: string;
  metadata: {
    file_name: string;
    document_title: string;
    chunk_index: number;
  };
  score: number;
}

export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  isStreaming?: boolean;
  mode?: 'simple' | 'research';
  sources?: Source[];
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

export interface StreamingResponse {
  content: string;
  isComplete: boolean;
}
