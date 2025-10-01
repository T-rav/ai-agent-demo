import React from 'react';
import { MessageList } from '../MessageList/MessageList';
import { MessageInput } from '../MessageInput/MessageInput';
import { useChat } from '../../hooks/useChat';
import './ChatContainer.css';

interface ChatContainerProps {
  title?: string;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({ title = 'AI Assistant' }) => {
  const { messages, isLoading, error, sendMessage, clearMessages, clearError, exportToMarkdown } =
    useChat();

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="header-content">
          <h1 className="chat-title">{title}</h1>
          {messages.length > 0 && (
            <div className="header-buttons">
              <button
                onClick={exportToMarkdown}
                className="export-button"
                aria-label="Export chat to markdown"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M7 10L12 15L17 10"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M12 15V3"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                Export
              </button>
              <button
                onClick={clearMessages}
                className="clear-button"
                aria-label="Clear conversation"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M3 6H5H21"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                Clear
              </button>
            </div>
          )}
        </div>
      </header>

      {error && (
        <div className="error-banner">
          <div className="error-content">
            <span className="error-icon">⚠️</span>
            <span className="error-message">{error}</span>
            <button onClick={clearError} className="error-dismiss" aria-label="Dismiss error">
              ×
            </button>
          </div>
        </div>
      )}

      <main className="chat-main">
        <MessageList messages={messages} isLoading={isLoading} />
        <MessageInput
          onSendMessage={sendMessage}
          disabled={isLoading}
          placeholder={isLoading ? 'AI is responding...' : 'Type your message...'}
        />
      </main>
    </div>
  );
};
