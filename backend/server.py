from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

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
VENICE_API_KEY = os.getenv('VENICE_API_KEY')
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

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(chat_input: ChatMessage):
    """Handle AI chat conversations using Venice AI"""
    
    if not VENICE_API_KEY:
        raise HTTPException(status_code=500, detail="Venice AI API key not configured")
    
    # Generate or use existing session ID
    session_id = chat_input.sessionId or str(uuid.uuid4())
    
    try:
        # Get conversation history for this session
        session_doc = await db.chat_sessions.find_one({"sessionId": session_id})
        conversation_history = []
        
        if session_doc:
            conversation_history = session_doc.get("messages", [])
        
        # Build messages for Venice AI
        messages = [
            {
                "role": "system", 
                "content": """You are Tolu Shekoni's AI assistant. You represent Tolu, an AI Generalist and Full-Stack Developer who transitioned from 8+ years in pharmaceutical manufacturing to AI development. 

Key facts about Tolu:
- Expert in AI integration, LLM development, prompt engineering
- Full-stack developer (React, Next.js, Python, Rust/WASM, Node.js)
- Strong background in process optimization, Lean Six Sigma, data analytics
- Transitioned from biopharma operations to AI/tech
- Specializes in turning complex problems into elegant solutions
- Experience with cGMP, regulatory compliance, technical troubleshooting
- Passionate about automation, efficiency, and continuous improvement

Answer questions about Tolu's background, skills, projects, and expertise. Be conversational, professional, and highlight his unique combination of operational excellence and AI development skills."""
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
        
        # Call Venice AI
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{VENICE_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {VENICE_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "venice-uncensored",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_completion_tokens": 512,
                    "venice_parameters": {
                        "include_venice_system_prompt": False,
                        "enable_web_search": "off"
                    }
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Venice AI API error: {response.status_code}")
            
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
        
        # Save conversation to database
        new_messages = conversation_history + [
            {"role": "user", "content": chat_input.message, "timestamp": datetime.utcnow()},
            {"role": "ai", "content": ai_response, "timestamp": datetime.utcnow()}
        ]
        
        await db.chat_sessions.update_one(
            {"sessionId": session_id},
            {
                "$set": {
                    "sessionId": session_id,
                    "messages": new_messages,
                    "updatedAt": datetime.utcnow()
                },
                "$setOnInsert": {"createdAt": datetime.utcnow()}
            },
            upsert=True
        )
        
        return ChatResponse(
            response=ai_response,
            sessionId=session_id
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")

@api_router.post("/contact", response_model=ContactResponse)
async def submit_contact_form(contact: ContactForm):
    """Handle contact form submissions and send email"""
    
    try:
        # Save to database
        contact_doc = {
            "_id": str(uuid.uuid4()),
            "name": contact.name,
            "email": contact.email,
            "company": contact.company,
            "subject": contact.subject,
            "message": contact.message,
            "status": "pending",
            "submittedAt": datetime.utcnow()
        }
        
        await db.contact_submissions.insert_one(contact_doc)
        
        # Send email if configured
        if EMAIL_USER and EMAIL_PASS:
            await send_contact_email(contact)
        
        return ContactResponse(
            success=True,
            messageId=contact_doc["_id"]
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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
