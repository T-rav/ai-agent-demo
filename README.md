# AI Agent Demo

A modern, dockerized chat application with a React TypeScript frontend and Python backend (backend to be implemented).

## 🚀 Features

### Frontend (React UI)
- ✅ **Modern Chat Interface**: Clean, responsive design inspired by popular messaging apps
- ✅ **Real-time Streaming**: Support for streaming responses from AI models
- ✅ **TypeScript**: Full type safety and excellent developer experience
- ✅ **Comprehensive Testing**: Full test coverage with Jest and React Testing Library
- ✅ **Docker Ready**: Production and development Docker configurations
- ✅ **Mobile Responsive**: Works seamlessly on desktop and mobile devices

### Backend (Python API)
- 🔄 **To be implemented**: Python FastAPI backend with LLM integration

## 📁 Project Structure

```
ai-agent-demo/
├── ui/                          # React TypeScript frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── ChatContainer/   # Main chat container
│   │   │   ├── MessageList/     # Message display
│   │   │   ├── MessageInput/    # Message input
│   │   │   └── Message/         # Individual message
│   │   ├── hooks/               # Custom React hooks
│   │   ├── services/            # API services
│   │   ├── types/               # TypeScript definitions
│   │   └── test-utils/          # Testing utilities
│   ├── Dockerfile               # Production Docker config
│   ├── Dockerfile.dev           # Development Docker config
│   └── nginx.conf               # Nginx configuration
├── backend/                     # Python backend (to be implemented)
├── docker-compose.yml           # Production compose
├── docker-compose.dev.yml       # Development compose
└── README.md                    # This file
```

## 🛠️ Quick Start

### Using Makefile (Recommended)

```bash
# See all available commands
make help

# Start all services (UI + API when available)
make start

# Start only UI development server
make ui

# Stop all services
make stop

# Check service status
make status

# Install dependencies
make install

# Run tests
make test

# Build for production
make build
```

### Manual Setup

#### Frontend Only
```bash
cd ui
npm install
npm start
```

#### With Docker (Development)
```bash
# Start frontend in development mode
docker-compose -f docker-compose.dev.yml up frontend-dev
```

### Production

```bash
# Build and start all services
docker-compose up --build
# Or using Makefile
make build
```

## 🧪 Testing

The React frontend includes comprehensive tests:

```bash
cd ui
npm test                    # Interactive mode
npm run test -- --coverage # With coverage report
```

## 🎨 UI Features

### Chat Interface
- **Empty State**: Welcoming message when no conversation exists
- **Message Display**: User and assistant messages with timestamps
- **Streaming Responses**: Real-time display of AI responses as they arrive
- **Input Field**: Auto-resizing textarea with send button
- **Error Handling**: User-friendly error messages with dismiss option
- **Clear Conversation**: Option to clear chat history

### Design System
- **Colors**: iOS-inspired color palette
- **Typography**: System fonts for optimal readability
- **Layout**: Flexbox-based responsive design
- **Animations**: Smooth transitions and loading states
- **Accessibility**: ARIA labels and keyboard navigation

## 🔌 API Integration

The frontend expects a backend API with these endpoints:

### Streaming Chat (Primary)
```http
POST /api/chat/stream
Content-Type: application/json

{
  "message": "User message here"
}

Response: Server-Sent Events
data: {"content": "Partial response"}
data: {"content": " more content"}
data: [DONE]
```

### Synchronous Chat (Fallback)
```http
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

## ⚙️ Configuration

### Environment Variables

```bash
# Frontend
REACT_APP_API_URL=http://localhost:8000

# Backend (when implemented)
PORT=8000
DEBUG=1
```

## 🐳 Docker

### Development
- **Frontend**: React dev server with hot reload
- **Backend**: Python with auto-reload (to be implemented)

### Production
- **Frontend**: Nginx serving optimized React build
- **Backend**: Gunicorn with Python app (to be implemented)

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🛠️ Makefile Commands

The project includes a comprehensive Makefile for easy development:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make start` | Start all services (auto-detects Docker availability) |
| `make stop` | Stop all running services |
| `make ui` | Start only the UI development server |
| `make api` | Start only the API server (when implemented) |
| `make build` | Build all services for production |
| `make install` | Install dependencies for all services |
| `make test` | Run all tests |
| `make test-ui` | Run UI tests only |
| `make check` | Check TypeScript compilation |
| `make status` | Show status of running services |
| `make logs` | Show logs from running services |
| `make clean` | Clean build artifacts and dependencies |

## 🔮 Next Steps

1. **Implement Python Backend**:
   - FastAPI server
   - LLM integration (OpenAI, Anthropic, etc.)
   - Streaming response endpoints
   - Error handling and validation

2. **Enhanced Features**:
   - Message persistence
   - User authentication
   - Multiple conversation threads
   - File upload support
   - Markdown rendering

3. **Deployment**:
   - Production Docker orchestration
   - CI/CD pipeline
   - Environment-specific configurations

## 🤝 Contributing

1. Follow existing code patterns and TypeScript conventions
2. Write tests for new functionality
3. Ensure all tests pass before submitting
4. Use meaningful commit messages

## 📄 License

This project is a demonstration application for AI chat interfaces.