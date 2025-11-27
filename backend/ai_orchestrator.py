"""
Advanced AI Orchestrator for multi-model, multi-tool agent system
Implements intelligent routing, tool orchestration, and streaming responses
"""

import httpx
import json
import logging
from typing import Optional, List, Dict, AsyncGenerator, Any
from enum import Enum
from datetime import datetime
import os

logger = logging.getLogger(__name__)

VENICE_API_KEY = os.getenv("VENICE_API_KEY")
VENICE_BASE_URL = "https://api.venice.ai/api/v1"

class QueryType(Enum):
    """Classification of query complexity and type"""
    SIMPLE_FAQ = "simple_faq"  # Uses fast model
    FACTUAL_SEARCH = "factual_search"  # Needs web search
    CODE_GENERATION = "code_generation"  # Uses code-optimized model
    REASONING = "reasoning"  # Uses largest reasoning model
    CREATIVE = "creative"  # Uses creative model
    CONVERSATION = "conversation"  # General chat

# Model selection strategy based on task type
MODEL_CONFIG = {
    QueryType.SIMPLE_FAQ: {
        "model": "llama-3.2-3b",  # Fast, lightweight
        "temperature": 0.5,
        "max_tokens": 256,
        "description": "Fast factual responses"
    },
    QueryType.FACTUAL_SEARCH: {
        "model": "qwen-2.5-qwq-32b",  # Good reasoning + search
        "temperature": 0.3,
        "max_tokens": 512,
        "web_search": "on",
        "description": "Research with web search"
    },
    QueryType.CODE_GENERATION: {
        "model": "deepseek-coder-v2-lite",  # Specialized for code
        "temperature": 0.2,
        "max_tokens": 1024,
        "description": "Code generation and explanation"
    },
    QueryType.REASONING: {
        "model": "deepseek-r1-671b",  # Large reasoning model
        "temperature": 0.5,
        "max_tokens": 2048,
        "description": "Deep reasoning and analysis"
    },
    QueryType.CREATIVE: {
        "model": "qwen3-235b",
        "temperature": 0.8,
        "max_tokens": 1024,
        "description": "Creative and exploratory responses"
    },
    QueryType.CONVERSATION: {
        "model": "qwen-2.5-coder-32b",
        "temperature": 0.7,
        "max_tokens": 512,
        "description": "General conversation"
    }
}

# Keywords for query classification
QUERY_CLASSIFIERS = {
    QueryType.CODE_GENERATION: [
        "code", "function", "script", "program", "implement", "write", "algorithm",
        "python", "javascript", "typescript", "java", "cpp", "rust", "go", "debug"
    ],
    QueryType.FACTUAL_SEARCH: [
        "what", "when", "where", "how", "news", "current", "recent", "latest",
        "fact", "information", "research", "data", "statistics", "find"
    ],
    QueryType.REASONING: [
        "why", "explain", "analyze", "compare", "contrast", "evaluate", "opinion",
        "discuss", "think about", "consider", "complex", "deep", "understand"
    ],
    QueryType.CREATIVE: [
        "create", "write", "story", "poem", "idea", "brainstorm", "imagine",
        "generate", "design", "compose", "art", "creative"
    ],
    QueryType.SIMPLE_FAQ: [
        "hello", "hi", "who", "what are you", "name", "help", "thanks", "yes", "no"
    ]
}


class AIOrchestrator:
    """Intelligent multi-model AI orchestrator with streaming support"""
    
    # Class attributes for model configuration
    MODEL_CONFIG = MODEL_CONFIG
    QUERY_CLASSIFIERS = QUERY_CLASSIFIERS
    
    def __init__(self):
        self.api_key = VENICE_API_KEY
        self.base_url = VENICE_BASE_URL
        
    def classify_query(self, user_message: str, conversation_history: List[Dict]) -> QueryType:
        """
        Classify user query to determine best model and approach
        Uses keyword matching and conversation context
        """
        message_lower = user_message.lower()
        
        # Check for previous context to infer type
        if len(conversation_history) > 1:
            # Look at last few messages for context
            recent_context = " ".join([
                msg.get("content", "").lower() 
                for msg in conversation_history[-4:] 
                if msg.get("role") != "system"
            ])
        else:
            recent_context = message_lower
        
        # Score each query type
        scores: Dict[QueryType, int] = {qt: 0 for qt in QueryType}
        
        for query_type, keywords in QUERY_CLASSIFIERS.items():
            for keyword in keywords:
                if keyword in message_lower or keyword in recent_context:
                    scores[query_type] += 1
        
        # Special rules
        if any(keyword in message_lower for keyword in ["error", "fix", "bug", "wrong"]):
            scores[QueryType.CODE_GENERATION] += 3
        
        if len(message_lower) < 20 and any(word in message_lower for word in ["hi", "hello", "thanks"]):
            scores[QueryType.SIMPLE_FAQ] += 5
        
        # Default to conversation if no clear classification
        best_type = max(scores, key=scores.get)
        if scores[best_type] == 0:
            best_type = QueryType.CONVERSATION
        
        logger.info(f"Query classified as: {best_type.value} (scores: {scores})")
        return best_type
    
    def build_system_prompt(self, query_type: QueryType, user_context: Optional[str] = None) -> str:
        """Build optimized system prompt based on query type"""
        
        base_prompt = """You are an expert AI assistant powered by Venice AI. You have access to web search capabilities.

Key attributes:
- You are deeply knowledgeable about AI, software engineering, career development, and technology
- You embody Tolu's expertise in AI/ML, full-stack development, and innovation
- You provide accurate, well-reasoned responses
- You cite sources and verify information when using web search
- You engage thoughtfully with complex questions"""
        
        type_specific = {
            QueryType.CODE_GENERATION: """
Additional instructions for code tasks:
- Provide well-commented, production-ready code
- Explain complex algorithms clearly
- Follow best practices for the language
- Include error handling and edge cases
- Suggest performance optimizations when relevant""",
            
            QueryType.FACTUAL_SEARCH: """
Additional instructions for research:
- Use web search to find current information
- Cite your sources clearly
- Distinguish between facts and interpretations
- Provide multiple perspectives when relevant
- Include timestamps for recent information""",
            
            QueryType.REASONING: """
Additional instructions for complex analysis:
- Break down complex problems step-by-step
- Show your reasoning clearly
- Consider multiple viewpoints
- Identify assumptions and limitations
- Provide nuanced analysis rather than oversimplification""",
            
            QueryType.CREATIVE: """
Additional instructions for creative content:
- Be imaginative and engaging
- Use vivid language and storytelling
- Balance creativity with accuracy
- Tailor tone to the request
- Add personality to the response""",
        }
        
        prompt = base_prompt
        if query_type in type_specific:
            prompt += type_specific[query_type]
        
        if user_context:
            prompt += f"\n\nContext about the user: {user_context}"
        
        return prompt
    
    def compress_conversation_history(
        self, 
        history: List[Dict], 
        max_messages: int = 8,
        summary_threshold: int = 15
    ) -> List[Dict]:
        """
        Compress conversation history for better token efficiency
        Keeps recent messages full, summarizes older ones
        """
        if len(history) <= max_messages:
            return history
        
        # Keep last N messages full (recent context is most important)
        recent_messages = history[-max_messages:]
        older_messages = history[:-max_messages]
        
        # Create a summary of older messages to maintain context
        if older_messages:
            summary_text = f"[Earlier conversation summary: The user and assistant discussed "
            user_topics = []
            assistant_responses = []
            
            for msg in older_messages:
                content = msg.get("content", "")[:100]  # First 100 chars
                if msg.get("role") == "user":
                    user_topics.append(content)
                elif msg.get("role") == "assistant":
                    assistant_responses.append(content)
            
            summary_text += "; ".join(user_topics[:3])
            summary_text += ". Relevant context was provided.]"
            
            summary_msg = {
                "role": "system",
                "content": summary_text
            }
            
            return [summary_msg] + recent_messages
        
        return recent_messages
    
    async def chat_stream(
        self,
        user_message: str,
        conversation_history: List[Dict],
        query_type: Optional[QueryType] = None,
        user_context: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat responses with intelligent model selection
        Yields tokens as they arrive from the API
        """
        
        # Auto-classify if not provided
        if query_type is None:
            query_type = self.classify_query(user_message, conversation_history)
        
        # Get model config
        config = MODEL_CONFIG[query_type]
        model = config["model"]
        
        logger.info(f"Using model: {model} for query type: {query_type.value}")
        
        # Build optimized system prompt
        system_prompt = self.build_system_prompt(query_type, user_context)
        
        # Compress conversation history for efficiency
        compressed_history = self.compress_conversation_history(conversation_history)
        
        # Build messages
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add compressed history
        for msg in compressed_history:
            if msg.get("role") != "system":  # Don't duplicate system message
                messages.append({
                    "role": msg.get("role"),
                    "content": msg.get("content")
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Build request
        request_body = {
            "model": model,
            "messages": messages,
            "temperature": config.get("temperature", 0.7),
            "max_completion_tokens": config.get("max_tokens", 512),
            "stream": True,
        }
        
        # Add web search if configured for this query type
        if config.get("web_search"):
            request_body["venice_parameters"] = {
                "enable_web_search": config["web_search"],
                "enable_web_citations": True,
                "include_venice_system_prompt": False
            }
        else:
            request_body["venice_parameters"] = {
                "include_venice_system_prompt": False
            }
        
        logger.info(f"Streaming request to {model} with web_search={config.get('web_search', 'off')}")
        
        # Stream from Venice AI
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=request_body
            ) as response:
                if response.status_code != 200:
                    error_text = await response.atext()
                    logger.error(f"Venice API error: {response.status_code} - {error_text}")
                    yield f"Error: Failed to get AI response (Status {response.status_code})"
                    return
                
                # Process streaming response
                buffer = ""
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            delta = data.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
    
    async def chat(
        self,
        user_message: str,
        conversation_history: List[Dict],
        query_type: Optional[QueryType] = None,
        user_context: Optional[str] = None
    ) -> str:
        """
        Non-streaming chat response (collects all tokens then returns)
        Useful for error handling and synchronous responses
        """
        full_response = ""
        async for token in self.chat_stream(
            user_message, 
            conversation_history, 
            query_type, 
            user_context
        ):
            full_response += token
        return full_response

