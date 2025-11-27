# Implementation & Deployment Guide

## 🚀 Quick Start

### Step 1: Update Backend Dependencies

The new AI orchestration system uses existing Venice AI APIs but we need to ensure async support is optimal:

```bash
cd /workspaces/AI-generalist/backend
# Current requirements.txt already has everything needed
# Just verify httpx is installed for streaming:
pip install -U httpx>=0.28.1
```

### Step 2: Verify File Structure

Ensure these new files are in place:
```
backend/
├── server.py (updated)
├── ai_orchestrator.py (new)
├── conversation_memory.py (new)
└── requirements.txt (no changes needed)

frontend/
└── src/
    └── services/
        └── api.ts (updated with streaming)
    └── components/
        └── AIChat.tsx (updated with streaming UI)
```

### Step 3: Test the Orchestrator

Run the test suite:
```bash
cd /workspaces/AI-generalist
pytest tests/test_orchestrator.py -v
```

### Step 4: Start Backend with New Features

```bash
cd /workspaces/AI-generalist/backend
python server.py
```

The server will now:
- Use intelligent query routing
- Support streaming responses
- Maintain rich conversation context
- Compress history efficiently

### Step 5: Test Streaming in Frontend

Frontend should now:
- Display real-time token streaming
- Show model and query type being used
- Maintain better conversation context
- Handle errors gracefully

## 📋 Testing Checklist

### Backend Testing
```bash
# Test simple classification
curl http://localhost:8000/api/chat -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Hi"}'

# Test streaming
curl http://localhost:8000/api/chat/stream -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain quantum computing"}' \
  -H "Accept: text/event-stream"

# Test session stats
curl http://localhost:8000/api/chat/stats/SESSION_ID
```

### Frontend Testing
1. Open portfolio website
2. Click "Chat with AI Tolu"
3. Try different questions:
   - Simple: "Hi!" (should use fast model)
   - Code: "Write a function" (should use code model)
   - Reasoning: "Why is X better than Y?" (should use reasoning model)
4. Verify real-time streaming display
5. Test multi-turn conversation

## 🔍 Monitoring & Debugging

### Check Query Classification

Add this to see classification in logs:
```bash
# Run with debug logging
LOGLEVEL=DEBUG python server.py
```

Look for logs like:
```
Query classified as: code_generation (scores: {simple_faq: 0, code_generation: 4, ...})
Using model: deepseek-coder-v2-lite for query type: code_generation
```

### Monitor Model Usage

```python
# In backend, after each response:
logger.info(f"Session {session_id}: Used {model_config['model']} for {query_type.value}")
```

### Check Streaming

Test with curl:
```bash
curl -N http://localhost:8000/api/chat/stream -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Tell me a joke"}' \
  -H "Accept: text/event-stream" | head -20
```

Should see:
```
data: {"type":"metadata","session_id":"...","query_type":"creative","model":"qwen3-235b"}
data: {"type":"token","content":"Why"}
data: {"type":"token","content":" did"}
...
data: {"type":"done","session_id":"..."}
```

## 🔧 Configuration Tuning

### Adjust Model Timing

In `ai_orchestrator.py`, modify `MODEL_CONFIG`:

```python
MODEL_CONFIG = {
    QueryType.SIMPLE_FAQ: {
        "model": "llama-3.2-3b",
        "temperature": 0.5,
        "max_tokens": 256,  # Reduce for faster responses
    },
    QueryType.REASONING: {
        "model": "deepseek-r1-671b",
        "temperature": 0.5,
        "max_tokens": 2048,  # Increase for more detailed responses
    },
}
```

### Adjust Context Window Size

In `conversation_memory.py`:

```python
# Increase context for better multi-turn understanding
context_window = conversation_memory.get_context_window(
    session_id,
    include_recent=12,  # Was 8, now more messages kept
    include_system_summary=True
)
```

### Adjust Classification Keywords

In `ai_orchestrator.py`, modify `QUERY_CLASSIFIERS`:

```python
QUERY_CLASSIFIERS = {
    QueryType.CODE_GENERATION: [
        "code", "function", "script",
        # Add more keywords relevant to your use case
        "implementation", "library"
    ]
}
```

## 🚨 Troubleshooting

### Streaming Not Working
- Check: Is `/api/chat/stream` endpoint running?
- Verify: Browser supports EventSource (all modern browsers do)
- Solution: Fall back to non-streaming `/api/chat` endpoint

```javascript
// Add fallback in api.ts
try {
  // Try streaming first
  for await (const event of chatAPI.streamMessage(request)) { ... }
} catch (e) {
  // Fall back to non-streaming
  const response = await chatAPI.sendMessage(request);
}
```

### Classification Not Working
- Check: Are keywords in `QUERY_CLASSIFIERS` matching?
- Debug: Add `logger.info()` to see classification scores
- Solution: Update keywords based on actual usage patterns

### Slow Response Time
- Check: Which model is being used? (see logs)
- Problem: Large model for simple question?
- Solution: Adjust classification thresholds or add more keywords

### Sessions Not Persisting
- Check: Session ID being returned from backend?
- Check: Frontend storing session ID in localStorage?
- Debug: Verify `conversation_memory.get_session()` returns session

## 📊 Performance Metrics to Track

1. **Response Time**: 
   - Simple FAQ: < 2s
   - Conversation: 2-5s
   - Reasoning: 5-10s

2. **Model Usage Distribution**:
   - Track which models are used most
   - Identify misclassifications

3. **Token Efficiency**:
   - Measure average tokens per response
   - Compare before/after compression

4. **Error Rate**:
   - Stream failures
   - Classification errors
   - API timeouts

## 🔄 Continuous Improvement

### Weekly Tasks
- Review logs for misclassifications
- Check average response times by model
- Monitor API error rates

### Monthly Tasks
- Analyze user conversation patterns
- Identify new query types to add
- Adjust model thresholds based on data

### Quarterly Tasks
- Evaluate new Venice AI models
- Consider adding tools/function calling
- Refactor for performance improvements

## 📚 Next Steps (Optional Enhancements)

1. **Add Tool Support**
   - Implement function calling
   - Add web search triggers
   - Create custom tools for portfolio queries

2. **User Profiling**
   - Track user preferences
   - Personalize responses
   - Maintain user-specific context

3. **Knowledge Base**
   - Store portfolio data
   - Implement semantic search
   - Add RAG capabilities

4. **Analytics Dashboard**
   - Track query classifications
   - Monitor model performance
   - Visualize conversation patterns

5. **Multi-Language Support**
   - Detect language
   - Route to appropriate model
   - Maintain context across languages

## 🎯 Success Criteria

✅ Your upgrade is successful when:
- Simple queries respond in < 2 seconds
- Complex queries use appropriate reasoning models
- Streaming displays real-time tokens
- Multi-turn conversations maintain context
- Session persistence works across refreshes
- Error handling is graceful and informative
- Model selection is visible to user

## 📞 Support & Issues

If you encounter issues:
1. Check logs: `python server.py 2>&1 | grep -i "error\|warning"`
2. Test endpoints: Use curl commands above
3. Review tests: Check `tests/test_orchestrator.py` for examples
4. Debug: Add `print()` statements and check Flask/FastAPI terminal output

---

**Congratulations! Your chatbot is now production-grade. 🚀**

