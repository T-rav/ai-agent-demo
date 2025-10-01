import React from 'react';
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
      timeZone: 'UTC',
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
              {message.content}
              {message.isStreaming && <span className="cursor">|</span>}
            </>
          )}
        </div>
        <div className="message-metadata">
          <div className="message-time">{formatTime(message.timestamp)}</div>
          {message.mode && (
            <div
              className="message-mode"
              title={message.mode === 'simple' ? 'Simple Answer' : 'Research Mode'}
            >
              {message.mode === 'simple' ? '⚡' : '🔍'}
            </div>
          )}
          {message.sources && message.sources.length > 0 && (
            <div className="message-sources">
              {message.sources.map((source, index) => (
                <div
                  key={index}
                  className="message-source-icon"
                  title={`${source.metadata.title}\nFile: ${source.metadata.file_name}`}
                >
                  📚
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
