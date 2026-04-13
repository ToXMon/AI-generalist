# AI Generalist — Agent Documentation

## Repo Purpose
Full-stack AI chatbot portfolio application with web search capabilities. FastAPI backend proxies to Venice AI for LLM inference, React frontend provides a real-time chat interface. Deployed on Akash Network via Docker Compose with Nginx reverse proxy.

## Tech Stack
- **Backend**: Python 3 + FastAPI + Uvicorn + Pydantic + httpx
- **Frontend**: React 19 + TypeScript + Tailwind CSS + Craco
- **AI**: Venice AI API (LLM inference + web search)
- **Email**: SMTP via smtplib (contact form)
- **Rate Limiting**: SlowAPI
- **Auth**: python-jose (JWT) + passlib (bcrypt)
- **Data**: pandas + numpy (data processing)
- **Cloud**: AWS boto3 + S3
- **Deployment**: Docker + Docker Compose + Nginx + Akash Network SDL

## Module Map

| Directory | Purpose |
|-----------|---------|
| `backend/` | FastAPI server — Venice AI proxy, chat sessions, email, rate limiting |
| `frontend/src/` | React + TypeScript — chat UI, responsive layout |
| `deployment/` | Akash Network SDL files (console + standard + providers) |
| `scripts/` | Build and deployment helper scripts |
| `docs/` | Deployment guides, API references, build instructions |
| `tests/` | Backend unit tests + CORS test page |

## Global Standards
- Python backend: FastAPI with Pydantic models, async/await patterns
- Frontend: TypeScript with Tailwind CSS utility classes
- API prefix: `/api` on all backend routes
- Rate limiting: SlowAPI with per-IP key function
- Environment: `.env` files loaded via python-dotenv
- Docker: Multi-stage builds for production

## Environment Setup
Env vars in `.env.example`. Key groups:
- **AI**: VENICE_API_KEY (required for chat)
- **Email**: EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, EMAIL_TO (contact form)
- **CORS**: CORS_ORIGINS (comma-separated allowed origins)

## Key Patterns

### Venice AI Integration
Backend proxies chat requests to Venice AI API via httpx. Chat sessions stored in-memory dict (no external DB). Rate limited via SlowAPI.

### Chat Flow
Frontend sends POST /api/chat → Backend proxies to Venice AI → Streams response back → Session stored with UUID key.

### Deployment Architecture
```
Client → Nginx (:80) → Frontend (static) + Backend (:8000/api)
```
Production uses docker-compose.prod.yml with multi-stage frontend build and Nginx reverse proxy.
