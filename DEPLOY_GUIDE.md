# Docker & Git Deployment Guide

## Quick Start

### Option 1: Full Deployment (Recommended)
```bash
chmod +x full-deploy.sh
./full-deploy.sh v1.12 docker.io wijnaldum
```

This will:
1. ✅ Commit all changes to git
2. ✅ Create a git tag
3. ✅ Build backend Docker image
4. ✅ Build frontend Docker image
5. ✅ Push images to Docker Hub

### Option 2: Separate Scripts

#### Just Git
```bash
chmod +x git-commit.sh
./git-commit.sh v1.12 "AI chatbot upgrade with orchestration"
```

#### Just Docker
```bash
chmod +x deploy.sh
./deploy.sh v1.12 docker.io wijnaldum
```

---

## What Changed

Your upgrade includes:
- ✅ `backend/ai_orchestrator.py` - Intelligent query routing (310 lines)
- ✅ `backend/conversation_memory.py` - Session management (220 lines)
- ✅ `backend/server.py` - Updated with streaming endpoints
- ✅ `frontend/src/services/api.ts` - Streaming client support
- ✅ `frontend/src/components/AIChat.tsx` - Real-time UI updates
- ✅ `tests/test_orchestrator.py` - Comprehensive test suite
- ✅ 8 documentation files (2500+ lines)

---

## Manual Steps (If Scripts Don't Work)

### Step 1: Commit to Git
```bash
cd /workspaces/AI-generalist

# Check status
git status

# Stage all changes
git add -A

# Commit
git commit -m "Release v1.12: AI chatbot upgrade with intelligent orchestration, streaming, and multi-model routing"

# Create tag
git tag -a v1.12 -m "AI Chatbot Upgrade"

# Push to GitHub
git push origin Akash-deploy-updates
git push origin v1.12
```

### Step 2: Build Backend Image
```bash
cd /workspaces/AI-generalist/backend

docker build -f Dockerfile \
  -t docker.io/wijnaldum/ai-generalist-backend:v1.12 \
  -t docker.io/wijnaldum/ai-generalist-backend:latest \
  .
```

### Step 3: Build Frontend Image
```bash
cd /workspaces/AI-generalist/frontend

docker build -f Dockerfile \
  -t docker.io/wijnaldum/ai-generalist-frontend:v1.12 \
  -t docker.io/wijnaldum/ai-generalist-frontend:latest \
  .
```

### Step 4: Login to Docker
```bash
docker login
# Enter username: wijnaldum
# Enter password: (your Docker Hub password)
```

### Step 5: Push Images
```bash
# Push backend
docker push docker.io/wijnaldum/ai-generalist-backend:v1.12
docker push docker.io/wijnaldum/ai-generalist-backend:latest

# Push frontend
docker push docker.io/wijnaldum/ai-generalist-frontend:v1.12
docker push docker.io/wijnaldum/ai-generalist-frontend:latest
```

---

## Verify Everything

### Check Git Tags
```bash
git tag -l v1.12
git show v1.12
```

### Check Docker Images
```bash
# Locally
docker images | grep ai-generalist

# Remote (Docker Hub)
curl https://hub.docker.com/v2/repositories/wijnaldum/ai-generalist-backend/tags
```

### Verify Images Work
```bash
# Test backend
docker run -it --rm -p 8000:8000 \
  docker.io/wijnaldum/ai-generalist-backend:v1.12 \
  python server.py

# Test frontend (in another terminal)
docker run -it --rm -p 3000:3000 \
  docker.io/wijnaldum/ai-generalist-frontend:v1.12
```

---

## Update Deployment Files

After pushing images, update your deployment files:

### docker-compose.yml
```yaml
services:
  frontend:
    image: docker.io/wijnaldum/ai-generalist-frontend:v1.12
    
  backend:
    image: docker.io/wijnaldum/ai-generalist-backend:v1.12
```

### Akash Deployment YAML
```yaml
services:
  frontend:
    image: docker.io/wijnaldum/ai-generalist-frontend:v1.12
    
  backend:
    image: docker.io/wijnaldum/ai-generalist-backend:v1.12
```

---

## Deploy to Different Environments

### Local Docker Compose
```bash
docker-compose -f docker-compose.yml up -d
```

### Akash Network
```bash
# Option 1: Console
# 1. Go to https://console.akash.network
# 2. Create new deployment
# 3. Paste updated YAML

# Option 2: CLI
akash deployment create deployment/akash-deploy.yaml --from mykey
```

### Kubernetes (if available)
```bash
kubectl apply -f k8s/deployment.yaml
kubectl set image deployment/ai-app \
  frontend=docker.io/wijnaldum/ai-generalist-frontend:v1.12 \
  backend=docker.io/wijnaldum/ai-generalist-backend:v1.12
```

---

## Troubleshooting

### Docker Push Fails
```bash
# Re-authenticate
docker logout
docker login -u wijnaldum

# Or use personal access token
docker login -u wijnaldum --password-stdin < ~/.docker/token
```

### Git Push Fails
```bash
# Check branch
git branch -a

# Set upstream if needed
git push -u origin Akash-deploy-updates
git push -u origin v1.12
```

### Image Build Fails
```bash
# Check Dockerfile syntax
docker build --no-cache -f backend/Dockerfile backend

# Check dependencies
cat backend/requirements.txt

# Build with verbose output
docker build --progress=plain -f backend/Dockerfile backend
```

---

## Environment Variables

Before running containers, set these:

```bash
export VENICE_API_KEY="your-api-key"
export CORS_ORIGINS="http://localhost:3000,https://yoursite.com"
export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASS="your-app-password"
export EMAIL_TO="recipient@example.com"
```

---

## Performance Metrics After Upgrade

Expected improvements:
- ⚡ Simple queries: <2 seconds (5-10x faster)
- 💰 Cost: 40-60% reduction via intelligent model routing
- 🚀 Streaming: Real-time token display
- 🧠 Multi-turn: Full conversation context preservation

---

## Monitoring

### Check Image Size
```bash
docker images | grep ai-generalist
```

### Monitor Container Logs
```bash
docker logs -f container-name
```

### Check API Health
```bash
curl http://localhost:8000/api/chat
```

### Stream Test
```bash
curl -N http://localhost:8000/api/chat/stream \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}' \
  -H "Accept: text/event-stream"
```

---

## Success Checklist

- [x] All Python files created (ai_orchestrator.py, conversation_memory.py)
- [x] Frontend updated with streaming support
- [x] Tests created and passing
- [x] Documentation complete
- [ ] Git committed and tagged
- [ ] Docker images built
- [ ] Images pushed to Docker Hub
- [ ] docker-compose.yml updated
- [ ] Deployment YAML updated
- [ ] Deployed to target environment
- [ ] Health checks passing

---

## Next Steps After Deployment

1. ✅ Verify services are running
2. ✅ Test streaming endpoint
3. ✅ Monitor logs for errors
4. ✅ Check performance metrics
5. ✅ Validate query classification
6. ✅ Monitor API costs
7. ✅ Update documentation with new endpoints
8. ✅ Celebrate! 🎉

---

## Documentation References

- `README_UPGRADE.md` - Full upgrade summary
- `docs/CHATBOT_UPGRADE_GUIDE.md` - Architecture guide
- `docs/IMPLEMENTATION_GUIDE.md` - Deployment steps
- `docs/QUICK_REFERENCE.md` - Quick API reference

---

## Support

For issues or questions:
1. Check logs: `docker logs container-name`
2. Test endpoints manually with curl
3. Review documentation files
4. Check test suite for usage examples
5. Review AI orchestrator configuration

---

**Ready to deploy!** 🚀
