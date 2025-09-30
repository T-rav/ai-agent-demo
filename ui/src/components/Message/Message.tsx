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
    }).format(timestamp);
  };

  return (
    <div className={`message ${message.sender}`}>
      <div className="message-content">
        <div className="message-text">
          {message.content}
          {message.isStreaming && <span className="cursor">|</span>}
        </div>
        <div className="message-time">{formatTime(message.timestamp)}</div>
      </div>
    </div>
  );
};
