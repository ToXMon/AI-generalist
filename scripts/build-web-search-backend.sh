#!/bin/bash

# Build and push updated backend with web search capable model
echo "Building backend with web search model (qwen3-235b)..."

# Navigate to the backend directory
cd backend

# Build the new backend image
docker build -t wijnaldum/ai-generalist-backend:v1.5 .

# Push to Docker Hub
echo "Pushing backend v1.5 to Docker Hub..."
docker push wijnaldum/ai-generalist-backend:v1.5

echo "Backend v1.5 with web search model built and pushed successfully!"
echo "Now update your akash-deploy-console.yaml to use v1.5"