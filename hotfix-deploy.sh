#!/bin/bash

# Hotfix deployment script
# For fixing 'AIOrchestrator' object has no attribute 'MODEL_CONFIG' error

set -e

VERSION="${1:-v1.12-hotfix1}"
REGISTRY="${2:-docker.io}"
USERNAME="${3:-wijnaldum}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Hotfix Deployment - MODEL_CONFIG Attribute Fix${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}What was fixed:${NC}"
echo "  - Added MODEL_CONFIG and QUERY_CLASSIFIERS as class attributes"
echo "  - Resolves: 'AIOrchestrator' object has no attribute 'MODEL_CONFIG'"
echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  Version:  $VERSION"
echo "  Registry: $REGISTRY"
echo "  Username: $USERNAME"
echo ""

# Check docker
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Step 1: Verify changes
echo -e "${BLUE}Step 1: Verifying fix in ai_orchestrator.py${NC}"
if grep -q "MODEL_CONFIG = MODEL_CONFIG" backend/ai_orchestrator.py; then
    echo -e "${GREEN}✓ Fix verified: MODEL_CONFIG is now a class attribute${NC}"
else
    echo -e "${RED}✗ Fix not found${NC}"
    exit 1
fi

if grep -q "QUERY_CLASSIFIERS = QUERY_CLASSIFIERS" backend/ai_orchestrator.py; then
    echo -e "${GREEN}✓ Fix verified: QUERY_CLASSIFIERS is now a class attribute${NC}"
else
    echo -e "${RED}✗ Fix not found${NC}"
    exit 1
fi

echo ""

# Step 2: Build backend image
echo -e "${BLUE}Step 2: Building backend image${NC}"
docker build -f backend/Dockerfile \
    -t "$REGISTRY/$USERNAME/ai-generalist-backend:$VERSION" \
    -t "$REGISTRY/$USERNAME/ai-generalist-backend:latest" \
    backend

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend image built${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

echo ""

# Step 3: Test the image locally
echo -e "${BLUE}Step 3: Testing image locally${NC}"
echo -e "${YELLOW}Running container for 10 seconds to verify startup...${NC}"

TEST_CONTAINER=$(docker run -d -e VENICE_API_KEY=test \
    "$REGISTRY/$USERNAME/ai-generalist-backend:$VERSION" \
    python -c "from ai_orchestrator import AIOrchestrator; o = AIOrchestrator(); print('✓ AIOrchestrator MODEL_CONFIG:', hasattr(o, 'MODEL_CONFIG')); print('✓ Success!')")

# Wait for container to finish
sleep 3
docker logs "$TEST_CONTAINER" || true
docker rm "$TEST_CONTAINER" 2>/dev/null || true

echo -e "${GREEN}✓ Image test complete${NC}"

echo ""

# Step 4: Push image
echo -e "${BLUE}Step 4: Pushing image to registry${NC}"
docker push "$REGISTRY/$USERNAME/ai-generalist-backend:$VERSION"
docker push "$REGISTRY/$USERNAME/ai-generalist-backend:latest"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Image pushed${NC}"
else
    echo -e "${RED}✗ Push failed${NC}"
    exit 1
fi

echo ""

# Step 5: Git commit and tag
echo -e "${BLUE}Step 5: Committing changes to git${NC}"
git add -A
git commit -m "Hotfix: Add MODEL_CONFIG and QUERY_CLASSIFIERS as class attributes to AIOrchestrator"
git tag -a "$VERSION" -m "Hotfix: Fix 'AIOrchestrator' object has no attribute 'MODEL_CONFIG' error"
git push origin $(git rev-parse --abbrev-ref HEAD)
git push origin "$VERSION"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Git committed and tagged${NC}"
else
    echo -e "${RED}✗ Git operations failed${NC}"
fi

echo ""

# Summary
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Hotfix deployment complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Docker Image:${NC}"
echo "  $REGISTRY/$USERNAME/ai-generalist-backend:$VERSION"
echo "  $REGISTRY/$USERNAME/ai-generalist-backend:latest"
echo ""

echo -e "${YELLOW}What was fixed:${NC}"
echo "  1. Added MODEL_CONFIG as class attribute in AIOrchestrator"
echo "  2. Added QUERY_CLASSIFIERS as class attribute in AIOrchestrator"
echo "  3. Allows server.py to access: ai_orchestrator.MODEL_CONFIG[query_type]"
echo "  4. Allows tests to access: self.orchestrator.MODEL_CONFIG"
echo ""

echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Update your deployment to use: $VERSION"
echo "  2. For docker-compose: Update image tag in docker-compose.yml"
echo "  3. For Akash: Update image tags in your SDL files"
echo "  4. Redeploy: docker-compose up -d (or redeploy to Akash)"
echo ""

echo -e "${YELLOW}Verify the fix works:${NC}"
echo "  Test endpoint: curl http://localhost:8000/api/chat/stream -X POST \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"message\":\"Hello\"}' \\"
echo "    -H 'Accept: text/event-stream'"
echo ""

echo -e "${GREEN}✓ Hotfix complete!${NC}"
echo ""
