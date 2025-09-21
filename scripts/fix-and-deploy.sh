#!/bin/bash

# Fix and Deploy Script for Venice AI Role Issue
# This script builds the fixed backend image and provides deployment instructions

echo "🔧 Building fixed backend image..."
docker build -t wijnaldum/ai-generalist-backend:v1.4 ./backend/

echo "📤 Pushing backend image to Docker Hub..."
docker push wijnaldum/ai-generalist-backend:v1.4

if [ $? -eq 0 ]; then
    echo "✅ Backend image pushed successfully!"
    echo ""
    echo "🚀 Now deploy the updated SDL file to Akash:"
    echo "   The akash-deploy-console.yaml file has been updated to use v1.4"
    echo ""
    echo "💡 The fix changes the AI role from 'ai' to 'assistant' in conversation history"
    echo "   This resolves the Venice AI API validation error you were experiencing."
else
    echo "❌ Failed to push image. Please check your Docker Hub credentials:"
    echo "   docker login"
    echo "   Then run this script again."
fi