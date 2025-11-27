#!/bin/bash

# AI Generalist Docker Build, Tag, and Push Script
# Usage: ./deploy.sh [version] [registry/username]

set -e

# Default values
VERSION="${1:-v1.12}"
REGISTRY="${2:-docker.io}"
USERNAME="${3:-wijnaldum}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  AI Generalist - Docker Build, Tag & Push${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  Version:  $VERSION"
echo "  Registry: $REGISTRY"
echo "  Username: $USERNAME"
echo "  Backend:  $REGISTRY/$USERNAME/ai-generalist-backend:$VERSION"
echo "  Frontend: $REGISTRY/$USERNAME/ai-generalist-frontend:$VERSION"
echo ""

# Check if docker is running
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running or you don't have permission to access it${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Function to build and push image
build_and_push() {
    local service=$1
    local dockerfile_path=$2
    local build_context=$3
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Building $service...${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Build the image
    echo ""
    echo -e "${BLUE}Step 1: Building Docker image...${NC}"
    docker build -f "$dockerfile_path" -t "$REGISTRY/$USERNAME/$service:$VERSION" -t "$REGISTRY/$USERNAME/$service:latest" "$build_context"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Build successful${NC}"
    else
        echo -e "${RED}✗ Build failed${NC}"
        exit 1
    fi
    
    # Check Docker login
    echo ""
    echo -e "${BLUE}Step 2: Checking Docker authentication...${NC}"
    if ! docker info > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Logging into Docker...${NC}"
        docker login -u "$USERNAME"
    else
        echo -e "${GREEN}✓ Docker authenticated${NC}"
    fi
    
    # Push the image
    echo ""
    echo -e "${BLUE}Step 3: Pushing image to registry...${NC}"
    docker push "$REGISTRY/$USERNAME/$service:$VERSION"
    docker push "$REGISTRY/$USERNAME/$service:latest"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Push successful${NC}"
        echo "  - $REGISTRY/$USERNAME/$service:$VERSION"
        echo "  - $REGISTRY/$USERNAME/$service:latest"
    else
        echo -e "${RED}✗ Push failed${NC}"
        exit 1
    fi
}

# Check if files exist
echo -e "${BLUE}Step 0: Checking required files...${NC}"
if [ ! -f "backend/Dockerfile" ]; then
    echo -e "${RED}✗ backend/Dockerfile not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ backend/Dockerfile found${NC}"

if [ ! -f "frontend/Dockerfile" ]; then
    echo -e "${RED}✗ frontend/Dockerfile not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ frontend/Dockerfile found${NC}"
echo ""

# Build and push backend
build_and_push "ai-generalist-backend" "backend/Dockerfile" "backend"

echo ""

# Build and push frontend
build_and_push "ai-generalist-frontend" "frontend/Dockerfile" "frontend"

# Summary
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Build and Push Complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Images available at:${NC}"
echo "  Backend:"
echo "    - $REGISTRY/$USERNAME/ai-generalist-backend:$VERSION"
echo "    - $REGISTRY/$USERNAME/ai-generalist-backend:latest"
echo ""
echo "  Frontend:"
echo "    - $REGISTRY/$USERNAME/ai-generalist-frontend:$VERSION"
echo "    - $REGISTRY/$USERNAME/ai-generalist-frontend:latest"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Update docker-compose.yml with new image tags"
echo "  2. Update deployment YAMLs if needed"
echo "  3. Deploy: docker-compose up -d"
echo "  4. Or deploy to Akash with updated SDL"
echo ""
