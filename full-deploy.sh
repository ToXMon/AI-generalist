#!/bin/bash

# Complete deployment workflow script
# Handles: git commit → tag → docker build → docker push

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get version from argument or prompt
VERSION="${1:-}"
REGISTRY="${2:-docker.io}"
USERNAME="${3:-wijnaldum}"

if [ -z "$VERSION" ]; then
    echo -e "${YELLOW}Enter version (e.g., v1.12):${NC}"
    read VERSION
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Complete Deployment Workflow${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  Version:  $VERSION"
echo "  Registry: $REGISTRY"
echo "  Username: $USERNAME"
echo ""

# Confirmation
echo -e "${YELLOW}This will:${NC}"
echo "  1. Commit all changes with tag $VERSION"
echo "  2. Build backend Docker image"
echo "  3. Build frontend Docker image"
echo "  4. Push both images to $REGISTRY"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Aborted${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  STEP 1: Git Commit & Tag${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Check git status
if ! git diff-index --quiet HEAD --; then
    echo -e "${BLUE}Stage 1: Add changes${NC}"
    git add -A
    echo -e "${GREEN}✓ Changes staged${NC}"
    
    echo -e "${BLUE}Stage 2: Commit${NC}"
    git commit -m "Release $VERSION: AI chatbot upgrade with intelligent orchestration, streaming, and multi-model routing"
    echo -e "${GREEN}✓ Committed${NC}"
else
    echo -e "${YELLOW}⚠ No uncommitted changes${NC}"
fi

echo -e "${BLUE}Stage 3: Create tag${NC}"
git tag -a "$VERSION" -m "AI Chatbot Upgrade - Multi-model orchestration, streaming, context compression"
echo -e "${GREEN}✓ Tagged: $VERSION${NC}"

echo -e "${BLUE}Stage 4: Push to GitHub${NC}"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git push origin "$BRANCH"
git push origin "$VERSION"
echo -e "${GREEN}✓ Pushed to GitHub${NC}"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  STEP 2: Docker Build & Push${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Check Docker
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Build Backend
echo -e "${BLUE}Stage 1: Build Backend Image${NC}"
docker build -f backend/Dockerfile \
    -t "$REGISTRY/$USERNAME/ai-generalist-backend:$VERSION" \
    -t "$REGISTRY/$USERNAME/ai-generalist-backend:latest" \
    backend

echo -e "${GREEN}✓ Backend image built${NC}"
echo "  - $REGISTRY/$USERNAME/ai-generalist-backend:$VERSION"
echo "  - $REGISTRY/$USERNAME/ai-generalist-backend:latest"
echo ""

# Build Frontend
echo -e "${BLUE}Stage 2: Build Frontend Image${NC}"
docker build -f frontend/Dockerfile \
    -t "$REGISTRY/$USERNAME/ai-generalist-frontend:$VERSION" \
    -t "$REGISTRY/$USERNAME/ai-generalist-frontend:latest" \
    frontend

echo -e "${GREEN}✓ Frontend image built${NC}"
echo "  - $REGISTRY/$USERNAME/ai-generalist-frontend:$VERSION"
echo "  - $REGISTRY/$USERNAME/ai-generalist-frontend:latest"
echo ""

# Login check
echo -e "${BLUE}Stage 3: Docker Registry Authentication${NC}"
if ! docker info | grep -q "Logged in"; then
    echo -e "${YELLOW}⚠ Please log in to Docker${NC}"
    docker login -u "$USERNAME"
fi
echo -e "${GREEN}✓ Docker authenticated${NC}"
echo ""

# Push Backend
echo -e "${BLUE}Stage 4: Push Backend Image${NC}"
docker push "$REGISTRY/$USERNAME/ai-generalist-backend:$VERSION"
docker push "$REGISTRY/$USERNAME/ai-generalist-backend:latest"
echo -e "${GREEN}✓ Backend image pushed${NC}"
echo ""

# Push Frontend
echo -e "${BLUE}Stage 5: Push Frontend Image${NC}"
docker push "$REGISTRY/$USERNAME/ai-generalist-frontend:$VERSION"
docker push "$REGISTRY/$USERNAME/ai-generalist-frontend:latest"
echo -e "${GREEN}✓ Frontend image pushed${NC}"
echo ""

# Summary
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Git Repository:${NC}"
echo "  Branch: $BRANCH"
echo "  Tag: $VERSION"
echo "  Pushed to: https://github.com/ToXMon/AI-generalist/releases/tag/$VERSION"
echo ""

echo -e "${YELLOW}Docker Images:${NC}"
echo "  Backend:"
echo "    - $REGISTRY/$USERNAME/ai-generalist-backend:$VERSION"
echo "    - $REGISTRY/$USERNAME/ai-generalist-backend:latest"
echo ""
echo "  Frontend:"
echo "    - $REGISTRY/$USERNAME/ai-generalist-frontend:$VERSION"
echo "    - $REGISTRY/$USERNAME/ai-generalist-frontend:latest"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "  Option 1: Update docker-compose.yml and run locally"
echo "    1. Update image tags in docker-compose.yml"
echo "    2. docker-compose up -d"
echo "    3. Access at http://localhost:3000"
echo ""
echo "  Option 2: Deploy to Akash Network"
echo "    1. Update image tags in deployment YAML files"
echo "    2. Go to https://console.akash.network"
echo "    3. Create new deployment with updated YAML"
echo "    4. Or use: akash deployment create deployment/akash-deploy.yaml --from mykey"
echo ""
echo "  Option 3: Deploy using Kubernetes"
echo "    1. Update image tags in k8s manifests (if available)"
echo "    2. kubectl apply -f manifests/"
echo ""

echo -e "${YELLOW}Verify Images:${NC}"
echo "  docker images | grep ai-generalist"
echo "  docker push $REGISTRY/$USERNAME/ai-generalist-backend:$VERSION --dry-run"
echo ""

echo -e "${GREEN}✓ Deployment workflow complete!${NC}"
echo ""
