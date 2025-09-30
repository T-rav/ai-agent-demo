# AI Chat UI

A modern React TypeScript chat interface for AI conversations with streaming response support.

## Features

- 🎯 **Modern UI**: Clean, responsive design inspired by popular chat applications
- ⚡ **Real-time Streaming**: Support for streaming responses from AI models
- 🧪 **Comprehensive Testing**: Full test coverage with Jest and React Testing Library
- 🔧 **TypeScript**: Full type safety and excellent developer experience
- 🐳 **Docker Ready**: Production and development Docker configurations
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## Quick Start

### Development

```bash
# Install dependencies
npm install

# Start development server
npm start

# Run tests
npm test

# Run tests with coverage
npm run test -- --coverage
```

### Production Build

```bash
# Build for production
npm run build

# Serve production build locally
npx serve -s build
```

### Docker

```bash
# Development
docker-compose -f docker-compose.dev.yml up frontend-dev

# Production
docker-compose up frontend
```

## Project Structure

```
src/
├── components/          # React components
│   ├── ChatContainer/   # Main chat container
│   ├── MessageList/     # Message display component
│   ├── MessageInput/    # Message input component
│   └── Message/         # Individual message component
├── hooks/               # Custom React hooks
│   └── useChat.ts       # Chat state management hook
├── services/            # API services
│   └── chatService.ts   # Chat API communication
├── types/               # TypeScript type definitions
│   └── chat.ts          # Chat-related types
└── test-utils/          # Testing utilities
    ├── index.ts         # Custom render function
    └── mockData.ts      # Mock data for tests
```

## API Integration

The chat interface expects a backend API with the following endpoints:

### Streaming Chat (Recommended)
```
POST /api/chat/stream
Content-Type: application/json

{
  "message": "User message here"
}

Response: Server-Sent Events stream
data: {"content": "Partial response"}
data: {"content": " more content"}
data: [DONE]
```

### Synchronous Chat (Fallback)
```
POST /api/chat
Content-Type: application/json

{
  "message": "User message here"
}

Response:
{
  "response": "Complete AI response"
}
```

## Configuration

Set the API URL via environment variable:

```bash
REACT_APP_API_URL=http://localhost:8000
```

## Testing

The project includes comprehensive tests for all components and functionality:

- **Unit Tests**: Individual component testing
- **Integration Tests**: Full chat flow testing
- **Hook Tests**: Custom hook behavior testing
- **Service Tests**: API service testing

Run tests with:
```bash
npm test                    # Interactive mode
npm run test -- --coverage # With coverage report
npm run test -- --watchAll # Watch all files
```

## Styling

The UI uses vanilla CSS with a modern design system:

- **Color Scheme**: iOS-inspired colors with light theme
- **Typography**: System fonts for optimal readability
- **Layout**: Flexbox-based responsive design
- **Animations**: Smooth transitions and loading states

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the existing code style and patterns
2. Write tests for new functionality
3. Ensure all tests pass before submitting
4. Use TypeScript for type safety

## License

This project is part of the AI Agent Demo application.