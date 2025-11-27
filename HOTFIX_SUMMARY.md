# Production Hotfix: AIOrchestrator MODEL_CONFIG Error

## Problem
**Error in Production**: `Chat error: Error: 'AIOrchestrator' object has no attribute 'MODEL_CONFIG'`

**Location**: `AIChat.tsx:174:17` (when submitting chat)

**Root Cause**: 
- `MODEL_CONFIG` and `QUERY_CLASSIFIERS` were defined as module-level variables
- `server.py` tried to access them as class attributes: `ai_orchestrator.MODEL_CONFIG[query_type]`
- `tests/test_orchestrator.py` tried to access them as instance attributes: `self.orchestrator.MODEL_CONFIG`
- This caused AttributeError at runtime

## Solution
Added class attribute assignments in `AIOrchestrator` class:

```python
class AIOrchestrator:
    """Intelligent multi-model AI orchestrator with streaming support"""
    
    # Class attributes for model configuration
    MODEL_CONFIG = MODEL_CONFIG
    QUERY_CLASSIFIERS = QUERY_CLASSIFIERS
    
    def __init__(self):
        self.api_key = VENICE_API_KEY
        self.base_url = VENICE_BASE_URL
```

This allows both patterns to work:
1. ✅ `ai_orchestrator.MODEL_CONFIG[query_type]` - Used in server.py
2. ✅ `self.orchestrator.MODEL_CONFIG` - Used in tests
3. ✅ `orchestrator.QUERY_CLASSIFIERS` - Used in classify_query method

## File Changed
- `backend/ai_orchestrator.py` - Added 2 lines to make MODEL_CONFIG and QUERY_CLASSIFIERS class attributes

## Verification
Run the verification script:
```bash
python verify_fix.py
```

Expected output:
```
✓ Successfully imported AIOrchestrator
✓ AIOrchestrator.MODEL_CONFIG exists
✓ orchestrator.MODEL_CONFIG exists
✓ All tests passed!
```

## Deployment
### Option 1: Quick Hotfix (Recommended)
```bash
chmod +x hotfix-deploy.sh
./hotfix-deploy.sh v1.12-hotfix1 docker.io wijnaldum
```

This will:
1. ✅ Verify the fix in code
2. ✅ Build new backend image
3. ✅ Test the image locally
4. ✅ Push to Docker Hub
5. ✅ Commit and tag in git

### Option 2: Manual Deployment
```bash
# Build image
docker build -f backend/Dockerfile \
  -t docker.io/wijnaldum/ai-generalist-backend:v1.12-hotfix1 \
  -t docker.io/wijnaldum/ai-generalist-backend:latest \
  backend

# Push image
docker push docker.io/wijnaldum/ai-generalist-backend:v1.12-hotfix1
docker push docker.io/wijnaldum/ai-generalist-backend:latest

# Update your deployment
docker-compose up -d
# OR
akash deployment create deployment/akash-deploy.yaml --from mykey
```

## What to Update
1. **docker-compose.yml** - Update image tag for backend service:
   ```yaml
   backend:
     image: docker.io/wijnaldum/ai-generalist-backend:v1.12-hotfix1
   ```

2. **Akash Deployment YAMLs** - Update image tag:
   ```yaml
   services:
     backend:
       image: docker.io/wijnaldum/ai-generalist-backend:v1.12-hotfix1
   ```

3. **Redeploy**:
   ```bash
   # Local
   docker-compose down && docker-compose up -d
   
   # Akash
   akash deployment close <old-deployment-id>
   akash deployment create deployment/akash-deploy.yaml --from mykey
   ```

## Testing After Deployment
Test the streaming endpoint:
```bash
curl -N http://your-domain/api/chat/stream \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}' \
  -H "Accept: text/event-stream"
```

Expected: Streaming response with tokens appearing in real-time

## Affected Code Paths
1. **Chat Endpoint** (`POST /api/chat`)
   - Line: `model_config = ai_orchestrator.MODEL_CONFIG[query_type]`
   - Now: ✅ Works correctly

2. **Stream Endpoint** (`POST /api/chat/stream`)
   - Line: `model_config = ai_orchestrator.MODEL_CONFIG[query_type]`
   - Now: ✅ Works correctly

3. **Tests** (`tests/test_orchestrator.py`)
   - Line: `assert query_type in self.orchestrator.MODEL_CONFIG`
   - Now: ✅ Works correctly

## Performance Impact
- None - This is purely a structural fix
- No new dependencies added
- No behavior changes

## Rollback (If Needed)
If something goes wrong:
```bash
# Revert to previous version
docker-compose down
docker pull docker.io/wijnaldum/ai-generalist-backend:v1.12
docker-compose up -d

# OR on Akash
akash deployment close <current-deployment-id>
akash deployment create deployment/akash-deploy-old.yaml --from mykey
```

## Summary
- **Issue**: Missing class attributes on AIOrchestrator
- **Fix**: Added MODEL_CONFIG and QUERY_CLASSIFIERS as class attributes
- **Status**: ✅ READY FOR PRODUCTION
- **Impact**: Fixes chat error, no side effects
- **Deployment Time**: < 5 minutes
- **Risk Level**: Very Low (simple attribute assignment)

