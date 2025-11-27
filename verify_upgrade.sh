#!/bin/bash

# AI Chatbot Upgrade Verification Script
# Run this to verify all files are in place and the system is ready

set -e

echo "🔍 AI Chatbot Upgrade Verification Script"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (NOT FOUND)"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (NOT FOUND)"
        return 1
    fi
}

# Track errors
ERRORS=0

echo "📁 Checking Backend Files..."
echo "---"
check_file "backend/ai_orchestrator.py" || ((ERRORS++))
check_file "backend/conversation_memory.py" || ((ERRORS++))
check_file "backend/server.py" || ((ERRORS++))
check_file "backend/requirements.txt" || ((ERRORS++))
echo ""

echo "📱 Checking Frontend Files..."
echo "---"
check_file "frontend/src/services/api.ts" || ((ERRORS++))
check_file "frontend/src/components/AIChat.tsx" || ((ERRORS++))
echo ""

echo "📚 Checking Documentation..."
echo "---"
check_file "docs/CHATBOT_UPGRADE_GUIDE.md" || ((ERRORS++))
check_file "docs/IMPLEMENTATION_GUIDE.md" || ((ERRORS++))
check_file "docs/UPGRADE_SUMMARY.md" || ((ERRORS++))
check_file "docs/QUICK_REFERENCE.md" || ((ERRORS++))
echo ""

echo "🧪 Checking Tests..."
echo "---"
check_file "tests/test_orchestrator.py" || ((ERRORS++))
echo ""

echo "🔧 Checking Python Dependencies..."
echo "---"
# Check if httpx is in requirements
if grep -q "httpx" backend/requirements.txt; then
    echo -e "${GREEN}✓${NC} httpx in requirements.txt"
else
    echo -e "${YELLOW}⚠${NC} httpx might need verification (used for streaming)"
fi

if grep -q "fastapi" backend/requirements.txt; then
    echo -e "${GREEN}✓${NC} fastapi in requirements.txt"
else
    echo -e "${RED}✗${NC} fastapi missing from requirements.txt"
    ((ERRORS++))
fi
echo ""

echo "📋 Configuration Check..."
echo "---"
# Check if VENICE_API_KEY would be available
if [ -n "$VENICE_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} VENICE_API_KEY environment variable is set"
else
    echo -e "${YELLOW}⚠${NC} VENICE_API_KEY not set (will be needed at runtime)"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
    echo ""
    echo "🚀 Next Steps:"
    echo "1. cd backend && python server.py"
    echo "2. Test: curl http://localhost:8000/api/"
    echo "3. Test streaming: curl -N http://localhost:8000/api/chat/stream -X POST \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -d '{\"message\":\"Hello\"}' \\"
    echo "     -H 'Accept: text/event-stream'"
    echo "4. Run tests: pytest tests/test_orchestrator.py -v"
    echo ""
    echo "📖 Read the docs:"
    echo "- QUICK_REFERENCE.md - Quick overview"
    echo "- UPGRADE_SUMMARY.md - What changed"
    echo "- IMPLEMENTATION_GUIDE.md - Deployment steps"
    exit 0
else
    echo -e "${RED}❌ $ERRORS check(s) failed${NC}"
    echo ""
    echo "⚠️  Please fix the issues above before proceeding"
    exit 1
fi
