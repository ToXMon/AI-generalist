#!/bin/bash

# Git Tag, Commit, and Push Script
# Usage: ./git-commit.sh "version" "message"

set -e

VERSION="${1:-v1.12}"
MESSAGE="${2:-AI chatbot upgrade with orchestration and streaming}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Git Commit, Tag & Push${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  Version: $VERSION"
echo "  Message: $MESSAGE"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}✗ Not a git repository${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Git repository found${NC}"
echo ""

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "${BLUE}Current branch: ${YELLOW}$BRANCH${NC}"
echo ""

# Show status
echo -e "${BLUE}Git status:${NC}"
git status --short
echo ""

# Add all changes
echo -e "${BLUE}Step 1: Adding all changes...${NC}"
git add -A
echo -e "${GREEN}✓ Changes added${NC}"
echo ""

# Commit
echo -e "${BLUE}Step 2: Committing changes...${NC}"
git commit -m "$MESSAGE"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Committed${NC}"
else
    echo -e "${YELLOW}⚠ Nothing to commit or commit failed${NC}"
fi
echo ""

# Tag
echo -e "${BLUE}Step 3: Creating tag $VERSION...${NC}"
git tag -a "$VERSION" -m "Release $VERSION: $MESSAGE"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Tagged: $VERSION${NC}"
else
    echo -e "${RED}✗ Tag failed${NC}"
    exit 1
fi
echo ""

# Push commits
echo -e "${BLUE}Step 4: Pushing commits to origin/$BRANCH...${NC}"
git push origin "$BRANCH"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Pushed${NC}"
else
    echo -e "${RED}✗ Push failed${NC}"
    exit 1
fi
echo ""

# Push tags
echo -e "${BLUE}Step 5: Pushing tags to origin...${NC}"
git push origin "$VERSION"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Tags pushed${NC}"
else
    echo -e "${RED}✗ Tag push failed${NC}"
    exit 1
fi
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Git operations complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Summary:${NC}"
echo "  Commits pushed to: origin/$BRANCH"
echo "  Tag created: $VERSION"
echo "  Tag pushed: origin/$VERSION"
echo ""
echo -e "${YELLOW}View tag:${NC}"
echo "  git tag -l $VERSION"
echo ""
