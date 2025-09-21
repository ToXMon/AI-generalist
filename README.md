# AI Generalist Portfolio

A full-stack web application featuring an AI chatbot powered by Venice AI that can search the web and answer user questions.

## Features

- 🤖 AI Chatbot with web search capabilities
- 💬 Real-time conversation interface
- 🔍 Web search integration via Venice AI
- 📱 Responsive React frontend
- ⚡ FastAPI backend
- 🗄️ MongoDB for conversation persistence

## Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-generalist
   ```

2. **Set up environment variables**
   - Copy your Venice AI API key to `backend/.env` (already done)
   - The `VENICE_API_KEY` should be set in `backend/.env`

3. **Run with Docker Compose**
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Production Deployment

For production deployment with optimized multi-stage builds and Nginx reverse proxy:

1. **Build and run production services**
   ```bash
   docker compose -f docker-compose.prod.yml up --build
   ```

2. **Access the application**
   - Application: http://localhost
   - Backend API: http://localhost/api (proxied through Nginx)

The production setup uses:
- Multi-stage Docker build for the frontend (build stage with Node.js, runtime with Nginx)
- Nginx serving static files and proxying API requests to the backend
- Optimized Docker layers for faster builds and smaller images

## Manual Setup

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MongoDB** (if not using Docker)
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:7.0
   ```

4. **Run the backend**
   ```bash
   python server.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   yarn install
   ```

3. **Start the development server**
   ```bash
   yarn start
   ```

## API Endpoints

- `GET /api/` - Health check
- `POST /api/chat` - Send chat message to AI
- `POST /api/contact` - Submit contact form

## Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
CORS_ORIGINS=*
VENICE_API_KEY=your_venice_api_key_here
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password
EMAIL_TO=recipient@email.com
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8000
```

## Testing

Run the backend tests:
```bash
python backend_test.py
```

## Technologies Used

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI, Venice AI
- **Database**: MongoDB
- **Deployment**: Docker, Docker Compose
