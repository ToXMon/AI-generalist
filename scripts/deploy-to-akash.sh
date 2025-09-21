#!/bin/bash

# Akash Deployment Script
# This script helps build and deploy your application to Akash Network

set -e

echo "🚀 Starting Akash deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="docker.io"  # You can change this to your preferred registry
USERNAME="tolu"       # Replace with your registry username
FRONTEND_IMAGE="${REGISTRY}/${USERNAME}/generalist-frontend"
BACKEND_IMAGE="${REGISTRY}/${USERNAME}/generalist-backend"

echo -e "${YELLOW}Building frontend...${NC}"
cd frontend
docker build -t ${FRONTEND_IMAGE}:latest .
echo -e "${GREEN}Frontend built successfully!${NC}"

echo -e "${YELLOW}Building backend...${NC}"
cd ../backend
docker build -t ${BACKEND_IMAGE}:latest .
echo -e "${GREEN}Backend built successfully!${NC}"

cd ..

echo -e "${YELLOW}Pushing images to registry...${NC}"
echo "Make sure you're logged in to your registry:"
echo "docker login ${REGISTRY}"
read -p "Press Enter when logged in..."

docker push ${FRONTEND_IMAGE}:latest
docker push ${BACKEND_IMAGE}:latest

echo -e "${GREEN}Images pushed successfully!${NC}"

echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update akash-deploy.yaml with your actual values"
echo "2. Copy backend/.env.prod.template to backend/.env.prod and fill in secrets"
echo "3. Run: akash deploy create akash-deploy.yaml"
echo "4. After deployment, get your domain from the lease"
echo "5. Update CORS_ORIGINS in akash-deploy.yaml with your actual domain"
echo "6. Update the deployment: akash deploy update <deployment-id> akash-deploy.yaml"

echo -e "${GREEN}Deployment preparation complete!${NC}"