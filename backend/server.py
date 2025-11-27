from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, AsyncGenerator
import uuid
from datetime import datetime
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Import the new AI orchestrator and memory system
from ai_orchestrator import AIOrchestrator, QueryType
from conversation_memory import ConversationMemory, ConversationContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / '.env')

# Initialize AI orchestrator and memory systems
ai_orchestrator = AIOrchestrator()
conversation_memory = ConversationMemory(max_session_age_hours=24)
conversation_context = ConversationContext()

# Create the main app without a prefix
app = FastAPI()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class ChatMessage(BaseModel):
    message: str
    sessionId: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sessionId: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    query_type: Optional[str] = None
    model_used: Optional[str] = None
    tokens_estimated: Optional[int] = None

class ChatStreamRequest(BaseModel):
    message: str
    sessionId: Optional[str] = None
    stream: bool = True  # Enable streaming by default

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    subject: str
    message: str

class ContactResponse(BaseModel):
    success: bool
    messageId: Optional[str] = None
    error: Optional[str] = None

# Venice AI Configuration
VENICE_API_KEY = os.getenv("VENICE_API_KEY")
VENICE_BASE_URL = "https://api.venice.ai/api/v1"

# Email Configuration
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_TO = os.getenv('EMAIL_TO', 'tolu.a.shekoni@gmail.com')

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Tolu Shekoni Portfolio API - Venice AI Powered"}

@api_router.post("/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
async def chat_with_ai(request: Request, chat_input: ChatMessage):
    """
    Enhanced chat endpoint with intelligent model routing and streaming
    - Classifies queries for optimal model selection
    - Maintains rich conversation context
    - Provides metadata about model selection
    """
    
    if not VENICE_API_KEY:
        logger.error("Venice AI API key not configured")
        raise HTTPException(status_code=500, detail="Venice AI API key not configured")
    
    # Generate or use existing session ID
    session_id = chat_input.sessionId or str(uuid.uuid4())
    
    try:
        # Get or create conversation session
        session = conversation_memory.get_session(session_id)
        if not session:
            session = conversation_memory.create_session(session_id)
        
        # Get conversation context for model
        conversation_history = session.get("messages", [])
        
        # Get optimized context window
        context_window = conversation_memory.get_context_window(
            session_id,
            include_recent=8,
            include_system_summary=True
        )
        
        # Classify the query for intelligent routing
        query_type = ai_orchestrator.classify_query(
            chat_input.message, 
            context_window
        )
        
        # Get context about user/Tolu
        session_stats = conversation_memory.get_session_stats(session_id)
        user_context = conversation_context.build_context_for_query(
            chat_input.message,
            session_stats,
            [m.get("content", "")[:30] for m in conversation_history[-3:] if m.get("role") == "user"]
        )
        
        # Add user message to conversation
        conversation_memory.add_message(
            session_id,
            "user",
            chat_input.message,
            {"query_type": query_type.value}
        )
        
        logger.info(f"Session {session_id}: Query type={query_type.value}, History size={len(conversation_history)}")
        
        # Get the full response
        ai_response = await ai_orchestrator.chat(
            user_message=chat_input.message,
            conversation_history=context_window,
            query_type=query_type,
            user_context=user_context if user_context else None
        )
        
        # Add AI response to conversation
        conversation_memory.add_message(
            session_id,
            "assistant",
            ai_response,
            {"query_type": query_type.value}
        )
        
        # Get model config for response metadata
        model_config = ai_orchestrator.MODEL_CONFIG[query_type]
        
        return ChatResponse(
            response=ai_response,
            sessionId=session_id,
            query_type=query_type.value,
            model_used=model_config["model"],
            tokens_estimated=session_stats.get("estimated_tokens", 0)
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")


@api_router.post("/chat/stream")
@limiter.limit("20/minute")
async def chat_stream(request: Request, chat_input: ChatMessage):
    """
    Streaming chat endpoint for real-time token streaming
    Returns Server-Sent Events (SSE) stream
    """
    
    if not VENICE_API_KEY:
        logger.error("Venice AI API key not configured")
        raise HTTPException(status_code=500, detail="Venice AI API key not configured")
    
    # Generate or use existing session ID
    session_id = chat_input.sessionId or str(uuid.uuid4())
    
    async def generate():
        """Generator for streaming response"""
        try:
            # Get session and context
            session = conversation_memory.get_session(session_id)
            if not session:
                session = conversation_memory.create_session(session_id)
            
            context_window = conversation_memory.get_context_window(
                session_id,
                include_recent=8,
                include_system_summary=True
            )
            
            # Classify query
            query_type = ai_orchestrator.classify_query(
                chat_input.message,
                context_window
            )
            
            # Get user context
            session_stats = conversation_memory.get_session_stats(session_id)
            user_context = conversation_context.build_context_for_query(
                chat_input.message,
                session_stats,
                [m.get("content", "")[:30] for m in context_window[-3:] if m.get("role") == "user"]
            )
            
            # Add user message
            conversation_memory.add_message(
                session_id,
                "user",
                chat_input.message,
                {"query_type": query_type.value}
            )
            
            # Stream the response
            model_config = ai_orchestrator.MODEL_CONFIG[query_type]
            full_response = ""
            
            yield f"data: {json.dumps({'type': 'metadata', 'session_id': session_id, 'query_type': query_type.value, 'model': model_config['model']})}\n\n"
            
            async for token in ai_orchestrator.chat_stream(
                user_message=chat_input.message,
                conversation_history=context_window,
                query_type=query_type,
                user_context=user_context if user_context else None
            ):
                full_response += token
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
            
            # Add AI response to conversation
            conversation_memory.add_message(
                session_id,
                "assistant",
                full_response,
                {"query_type": query_type.value}
            )
            
            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"
            
        except Exception as e:
            logger.error(f"Stream error: {str(e)}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@api_router.get("/chat/stats/{session_id}")
async def get_chat_stats(session_id: str):
    """Get statistics about a chat session"""
    stats = conversation_memory.get_session_stats(session_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Session not found")
    return stats


@api_router.delete("/chat/{session_id}")
async def clear_chat_session(session_id: str):
    """Clear a chat session"""
    if conversation_memory.clear_session(session_id):
        return {"success": True, "message": f"Session {session_id} cleared"}
    raise HTTPException(status_code=404, detail="Session not found")

@api_router.post("/contact", response_model=ContactResponse)
async def submit_contact_form(contact: ContactForm):
    """Handle contact form submissions and send email"""
    
    message_id = str(uuid.uuid4())
    try:
        # Log submission
        logger.info(f"Received contact form submission {message_id} from {contact.email}")
        
        # Send email if configured
        if EMAIL_USER and EMAIL_PASS:
            await send_contact_email(contact)
        
        return ContactResponse(
            success=True,
            messageId=message_id
        )
        
    except Exception as e:
        logger.error(f"Contact form error: {str(e)}")
        return ContactResponse(
            success=False,
            error=str(e)
        )

async def send_contact_email(contact: ContactForm):
    """Send contact form email"""
    
    def send_email():
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = EMAIL_TO
            msg['Subject'] = f"Portfolio Contact: {contact.subject}"
            
            body = f"""
New contact form submission from your portfolio:

Name: {contact.name}
Email: {contact.email}
Company: {contact.company or 'Not provided'}
Subject: {contact.subject}

Message:
{contact.message}

---
This message was sent from your portfolio website.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully for contact from {contact.email}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
    
    # Run email sending in thread to avoid blocking
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, send_email)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add JSON import at module level
import json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
