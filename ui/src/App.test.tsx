import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the ChatContainer component
jest.mock('./components', () => ({
  ChatContainer: ({ title }: { title: string }) => (
    <div data-testid="chat-container">
      <h1>{title}</h1>
    </div>
  ),
}));

test('renders chat container with title', () => {
  render(<App />);
  const chatContainer = screen.getByTestId('chat-container');
  expect(chatContainer).toBeInTheDocument();
  expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();
});
