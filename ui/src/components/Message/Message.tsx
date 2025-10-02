import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message as MessageType } from '../../types/chat';
import './Message.css';

interface MessageProps {
  message: MessageType;
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const formatTime = (timestamp: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    }).format(timestamp);
  };

  return (
    <div className={`message ${message.sender}`}>
      <div className="message-content">
        <div className="message-text">
          {message.isStreaming && !message.content ? (
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          ) : (
            <>
              {message.sender === 'assistant' ? (
                <>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
                  {message.isStreaming && <span className="cursor">|</span>}
                </>
              ) : (
                <>
                  {message.content}
                  {message.isStreaming && <span className="cursor">|</span>}
                </>
              )}
            </>
          )}
        </div>
        <div className="message-metadata">
          <div className="message-time">{formatTime(message.timestamp)}</div>
          {message.mode && (
            <span
              className="message-mode"
              data-tooltip={message.mode === 'simple' ? 'Simple Answer' : 'Research Mode'}
            >
              {message.mode === 'simple' ? '⚡' : '🔍'}
            </span>
          )}
          {message.sources && message.sources.length > 0 && (
            <div className="message-sources">
              {message.sources.map((source, index) => (
                <span
                  key={index}
                  className="message-source-icon"
                  data-tooltip={`${source.metadata.document_title || 'Unknown'} - ${
                    source.metadata.file_name || 'Unknown file'
                  }`}
                >
                  📚
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
