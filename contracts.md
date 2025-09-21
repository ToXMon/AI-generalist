# API Contracts & Integration Plan - Tolu Shekoni Portfolio

## Overview
This document outlines the API contracts and integration strategy for converting the frontend mock data to a fully functional full-stack application with Venice AI integration and email functionality.

## Current Mock Data Location
- **File**: `/app/frontend/src/data/mock.js`
- **Mock Chat Conversations**: Used for AI chat simulation
- **Mock Contact Submissions**: Used for form testing
- **Skills Data**: Static data display
- **Projects Data**: Static portfolio display

## Backend API Endpoints to Implement

### 1. Venice AI Chat API
**Endpoint**: `POST /api/chat`
**Purpose**: Handle AI chat conversations using Venice AI
**Request**:
```json
{
  "message": "string",
  "sessionId": "string"
}
```
**Response**:
```json
{
  "response": "string",
  "sessionId": "string",
  "timestamp": "datetime"
}
```
**Implementation Notes**:
- Use Venice AI API with model: `venice-uncensored` (as per user's API specification)
- Store conversation history in MongoDB for session management
- Environment variable: `VENICE_API_KEY`

### 2. Contact Form API
**Endpoint**: `POST /api/contact`
**Purpose**: Handle contact form submissions and send emails
**Request**:
```json
{
  "name": "string",
  "email": "string", 
  "company": "string",
  "subject": "string",
  "message": "string"
}
```
**Response**:
```json
{
  "success": true,
  "messageId": "string"
}
```
**Implementation Notes**:
- Send email to: `tolu.a.shekoni@gmail.com`
- Store submission in MongoDB
- Use nodemailer for email sending
- Environment variables: `EMAIL_HOST`, `EMAIL_USER`, `EMAIL_PASS`

### 3. Skills API (Optional Enhancement)
**Endpoint**: `GET /api/skills`
**Purpose**: Serve skills data dynamically
**Response**: Current mock skills data structure

### 4. Projects API (Optional Enhancement)  
**Endpoint**: `GET /api/projects`
**Purpose**: Serve projects data dynamically
**Response**: Current mock projects data structure

## Database Schema

### Chat Sessions Collection
```javascript
{
  _id: ObjectId,
  sessionId: String,
  messages: [{
    role: String, // 'user' | 'ai'
    content: String,
    timestamp: Date
  }],
  createdAt: Date,
  updatedAt: Date
}
```

### Contact Submissions Collection
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  company: String,
  subject: String,
  message: String,
  status: String, // 'pending' | 'responded'
  submittedAt: Date
}
```

## Environment Variables Required

### Frontend (.env)
```
REACT_APP_BACKEND_URL=existing_value (don't modify)
```

### Backend (.env)
```
MONGO_URL=existing_value (don't modify)
DB_NAME=existing_value (don't modify)
VENICE_API_KEY=user_provided_key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=sending_email_address
EMAIL_PASS=app_password
EMAIL_TO=tolu.a.shekoni@gmail.com
```

## Frontend Integration Changes

### 1. TypeScript Refactoring
- Convert `.js` files to `.tsx`
- Add proper TypeScript interfaces
- Add type definitions for API responses

### 2. API Integration Points
**Current**: `mockChatConversations` usage in `AIChat.jsx`
**Replace with**: API call to `/api/chat`

**Current**: `mockContactSubmissions` usage in `Contact.jsx`  
**Replace with**: API call to `/api/contact`

### 3. Updated Frontend Files to Modify
1. `src/components/AIChat.jsx` → `src/components/AIChat.tsx`
2. `src/components/Contact.jsx` → `src/components/Contact.tsx`
3. `src/data/mock.js` → Remove after integration
4. Add `src/types/index.ts` for TypeScript interfaces
5. Add `src/services/api.ts` for API calls

## Implementation Steps

### Phase 1: Backend Development
1. Create Venice AI chat endpoint with session management
2. Create contact form endpoint with email functionality  
3. Set up MongoDB models for chat sessions and contacts
4. Add error handling and validation

### Phase 2: Frontend TypeScript Refactoring
1. Convert components to TypeScript
2. Add type definitions and interfaces
3. Create API service layer
4. Update imports and configurations

### Phase 3: Integration
1. Replace mock data with API calls
2. Add loading states and error handling
3. Test end-to-end functionality
4. Remove mock data files

### Phase 4: Testing & Validation
1. Test Venice AI integration with real API key
2. Validate email sending functionality
3. Test session management
4. Cross-browser compatibility check

## Success Criteria
- ✅ AI Chat responds using Venice AI with conversation history
- ✅ Contact form sends emails to `tolu.a.shekoni@gmail.com`
- ✅ All frontend components converted to TypeScript
- ✅ No mock data dependencies remaining
- ✅ Proper error handling and loading states
- ✅ Data persistence in MongoDB
- ✅ Secure API key management

## Notes
- Venice AI API key will be provided by user
- Email credentials may need to be configured based on user's preference
- Session management ensures conversation continuity
- All existing UI/UX remains unchanged