"""
Placeholder API server
This is a minimal FastAPI server that will be expanded with actual functionality.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Agent API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# Placeholder for future chat endpoint
@app.post("/api/chat/stream")
async def chat_stream():
    """
    Placeholder for streaming chat endpoint
    Will be implemented with actual LLM integration
    """
    return {"message": "Chat endpoint not yet implemented"}

