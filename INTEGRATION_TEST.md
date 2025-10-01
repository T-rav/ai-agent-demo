# UI ↔ API Integration Testing

## Connection Status: ✅ CONFIGURED

The UI and API are **properly configured** to communicate:

### Configuration
- **UI**: Calls `http://localhost:8000/api/chat/stream`
- **API**: Serves on `http://localhost:8000`
- **Format**: Both use SSE with `{"type": "token", "content": "..."}`
- **CORS**: Enabled (allow all origins)

### To Test End-to-End

1. **Set up API environment variables** (required):
   ```bash
   cd api
   cp env.example .env
   # Edit .env with your actual API keys:
   # - OPENAI_API_KEY
   # - PINECONE_API_KEY
   # - PINECONE_ENVIRONMENT
   ```

2. **Set up UI environment** (optional - has defaults):
   ```bash
   cd ui
   cp .env.example .env.local
   # Default REACT_APP_API_URL=http://localhost:8000 is fine
   ```

3. **Start both services**:
   ```bash
   # Option A: Docker Compose (recommended)
   docker-compose -f docker-compose.dev.yml up

   # Option B: Separate terminals
   # Terminal 1 - API
   cd api
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2 - UI
   cd ui
   npm start
   ```

4. **Test in browser**:
   - Open http://localhost:3000
   - Type a message in the chat
   - Should see streaming response from API

### Response Flow

```
User types → UI (React)
    ↓
POST /api/chat/stream
    {message: "What is RAG?"}
    ↓
API (FastAPI + LangGraph)
    ↓
SSE Stream:
data: {"type": "token", "content": "RAG"}
data: {"type": "token", "content": " stands"}
data: {"type": "token", "content": " for..."}
data: {"type": "done"}
    ↓
UI displays streaming text
```

### Troubleshooting

**API won't start?**
- Check `.env` has all required keys
- Run `cd api && python -m pytest tests/` to verify setup

**UI can't connect?**
- Check API is running on port 8000
- Check browser console for CORS errors
- Verify `REACT_APP_API_URL` in `.env.local`

**No streaming?**
- Check browser supports SSE (all modern browsers do)
- Check API logs for errors
- Verify OpenAI/Pinecone keys are valid

