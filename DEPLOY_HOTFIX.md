# Quick Deployment Guide - Production Hotfix

## 🚨 Production Issue Fixed

**Error**: `'AIOrchestrator' object has no attribute 'MODEL_CONFIG'`  
**Status**: ✅ FIXED  
**Severity**: High (Breaks chat functionality)  
**Fix Complexity**: Minimal (2 lines added)

---

## 🔧 What Was Fixed

Added `MODEL_CONFIG` and `QUERY_CLASSIFIERS` as class attributes in `AIOrchestrator`:

```python
class AIOrchestrator:
    # Class attributes for model configuration
    MODEL_CONFIG = MODEL_CONFIG
    QUERY_CLASSIFIERS = QUERY_CLASSIFIERS
```

This allows:
- ✅ `server.py` to access: `ai_orchestrator.MODEL_CONFIG[query_type]`
- ✅ Tests to access: `self.orchestrator.MODEL_CONFIG`
- ✅ Chat endpoint to work correctly

---

## 🚀 Deploy in 3 Minutes

### Step 1: Build & Push (Choose One)

**Option A: Automated (Recommended)**
```bash
chmod +x hotfix-deploy.sh
./hotfix-deploy.sh v1.12-hotfix1 docker.io wijnaldum
```

**Option B: Manual**
```bash
# Build
docker build -f backend/Dockerfile \
  -t docker.io/wijnaldum/ai-generalist-backend:v1.12-hotfix1 \
  -t docker.io/wijnaldum/ai-generalist-backend:latest \
  backend

# Push
docker push docker.io/wijnaldum/ai-generalist-backend:v1.12-hotfix1
docker push docker.io/wijnaldum/ai-generalist-backend:latest
```

### Step 2: Update Deployment

**For docker-compose.yml:**
```yaml
services:
  backend:
    image: docker.io/wijnaldum/ai-generalist-backend:v1.12-hotfix1
    # ... rest of config
```

**For Akash SDL:**
```yaml
services:
  backend:
    image: docker.io/wijnaldum/ai-generalist-backend:v1.12-hotfix1
    # ... rest of config
```

### Step 3: Redeploy

**Local (docker-compose):**
```bash
docker-compose down
docker-compose up -d
```

**Akash Network:**
```bash
# Close old deployment
akash deployment close <old-deployment-id>

# Create new deployment
akash deployment create deployment/akash-deploy.yaml --from mykey
```

---

## ✅ Verify Fix Works

### Test Endpoint (After Redeployment)
```bash
curl -N http://localhost:8000/api/chat/stream \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}' \
  -H "Accept: text/event-stream"
```

### Expected Response
```
data: {"type":"metadata","session_id":"...","query_type":"simple_faq","model":"llama-3.2-3b"}
data: {"type":"token","content":"Hello"}
data: {"type":"token","content":" there"}
...
data: {"type":"done","session_id":"..."}
```

### Check Logs
```bash
# Docker Compose
docker logs ai-generalist-backend-1 | grep -E "MODEL_CONFIG|Query classified"

# Akash (if accessible)
akash provider lease-logs <provider> <deployment> <lease> backend
```

---

## 📋 Files Changed

| File | Change | Status |
|------|--------|--------|
| `backend/ai_orchestrator.py` | Added class attributes | ✅ Done |
| `verify_fix.py` | Created verification script | ✅ New |
| `hotfix-deploy.sh` | Created deployment script | ✅ New |
| `HOTFIX_SUMMARY.md` | Full documentation | ✅ New |

---

## 🎯 Expected Outcomes

After deployment:
- ✅ Chat endpoint works: `POST /api/chat`
- ✅ Stream endpoint works: `POST /api/chat/stream`
- ✅ Real-time tokens display
- ✅ Query classification works
- ✅ Model routing works
- ✅ No more "MODEL_CONFIG" errors

---

## ⏱️ Deployment Timeline

| Step | Time |
|------|------|
| Build image | 2-3 min |
| Push to Docker Hub | 1-2 min |
| Redeploy locally | 30 sec |
| OR Redeploy to Akash | 2-5 min |
| **Total** | **5-10 min** |

---

## 🔄 Rollback (If Needed)

If something goes wrong, revert immediately:

```bash
# Stop current deployment
docker-compose down

# Pull previous version
docker pull docker.io/wijnaldum/ai-generalist-backend:v1.12

# Update docker-compose.yml with v1.12

# Restart
docker-compose up -d
```

---

## 📞 Support

If issues persist after deployment:

1. **Check logs for errors:**
   ```bash
   docker logs <container-name> --tail 50
   ```

2. **Verify the fix:**
   ```bash
   python verify_fix.py
   ```

3. **Test endpoint manually:**
   ```bash
   curl http://localhost:8000/api/ -v
   ```

4. **Check Python import:**
   ```bash
   python -c "from backend.ai_orchestrator import AIOrchestrator; o = AIOrchestrator(); print(hasattr(o, 'MODEL_CONFIG'))"
   ```

---

## ✨ Summary

- **What**: Added class attributes to AIOrchestrator
- **Why**: Fixes chat error in production
- **How**: 2-line code fix
- **Risk**: Minimal
- **Time**: 5-10 minutes
- **Status**: ✅ Ready to deploy

**Recommended Action**: Deploy immediately to fix production chat error.

