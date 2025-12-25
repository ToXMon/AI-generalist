from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
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


# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / '.env')

# In-memory storage for chat sessions
chat_sessions: Dict[str, Dict] = {}

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


class AIOrchestrator:
    """AI Orchestrator class for managing AI model configurations and interactions."""
    
    MODEL_CONFIG = {
        "model": os.getenv("AI_MODEL", "qwen3-235b"),
        "temperature": float(os.getenv("AI_TEMPERATURE", "0.7")),
        "max_completion_tokens": int(os.getenv("AI_MAX_TOKENS", "512")),
        "venice_parameters": {
            "include_venice_system_prompt": False,
            "enable_web_search": "on"
        }
    }
    
    SYSTEM_PROMPT = """You are a helpful AI assistant powered by Venice AI. You have access to web search capabilities to provide accurate and up-to-date information. 

You can:
- Answer questions on any topic using your knowledge and web search
- Provide explanations, summaries, and insights
- Help with problem-solving and research
- Engage in general conversation

When answering questions:
- Use web search when you need current information or to verify facts
- Be informative, accurate, and helpful
- Cite sources when appropriate
- Keep responses clear and well-structured"""
    
    def __init__(self):
        self.api_key = VENICE_API_KEY
        self.base_url = VENICE_BASE_URL
    
    def get_model_config(self) -> Dict:
        """Get the current model configuration."""
        return self.MODEL_CONFIG.copy()
    
    async def generate_response(self, messages: List[Dict], session_id: str) -> str:
        """Generate AI response using Venice AI."""
        if not self.api_key:
            raise HTTPException(status_code=500, detail="Venice AI API key not configured")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            logger.info(f"Making Venice AI request to: {self.base_url}/chat/completions")
            
            request_payload = {
                "messages": messages,
                **self.MODEL_CONFIG
            }
            
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=request_payload
            )
            
            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_detail = response.json()
                except Exception:
                    pass
                logger.error(f"Venice AI API error: {response.status_code} - {error_detail}")
                raise HTTPException(status_code=500, detail=f"Venice AI API error: {response.status_code}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]


# Global AI orchestrator instance
ai_orchestrator = AIOrchestrator()

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
@limiter.limit("10/minute")
async def chat_with_ai(request: Request, chat_input: ChatMessage):
    """Handle AI chat conversations using Venice AI"""
    
    if not ai_orchestrator.api_key:
        logger.error("Venice AI API key not configured")
        raise HTTPException(status_code=500, detail="Venice AI API key not configured")
    
    # Log API key status for debugging (without exposing the key)
    logger.info(f"Venice API key configured: {bool(ai_orchestrator.api_key)}, length: {len(ai_orchestrator.api_key) if ai_orchestrator.api_key else 0}")
    
    # Generate or use existing session ID
    session_id = chat_input.sessionId or str(uuid.uuid4())
    
    try:
        # Get conversation history for this session from in-memory storage
        session_data = chat_sessions.get(session_id, {})
        conversation_history = session_data.get("messages", [])
        
        # Build messages for Venice AI
        messages = [
            {
                "role": "system", 
                "content": ai_orchestrator.SYSTEM_PROMPT
            }
        ]
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Last 10 messages for context
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": chat_input.message
        })
        
        # Use AI orchestrator to generate response
        ai_response = await ai_orchestrator.generate_response(messages, session_id)
        
        # Save conversation to in-memory storage
        new_messages = conversation_history + [
            {"role": "user", "content": chat_input.message, "timestamp": datetime.utcnow().isoformat()},
            {"role": "assistant", "content": ai_response, "timestamp": datetime.utcnow().isoformat()}
        ]
        
        chat_sessions[session_id] = {
            "messages": new_messages,
            "updatedAt": datetime.utcnow().isoformat()
        }
        
        return ChatResponse(
            response=ai_response,
            sessionId=session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
