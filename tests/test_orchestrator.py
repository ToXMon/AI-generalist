"""
Test suite for the upgraded AI chatbot orchestration system
Run with: pytest test_orchestrator.py -v
"""

import pytest
import asyncio
from ai_orchestrator import AIOrchestrator, QueryType
from conversation_memory import ConversationMemory, ConversationContext


class TestQueryClassification:
    """Test query classification logic"""
    
    def setup_method(self):
        self.orchestrator = AIOrchestrator()
    
    def test_simple_faq_classification(self):
        """Test that simple greetings are classified as FAQ"""
        query_type = self.orchestrator.classify_query(
            "Hi, who are you?", 
            []
        )
        assert query_type == QueryType.SIMPLE_FAQ
    
    def test_code_generation_classification(self):
        """Test that code requests are classified correctly"""
        query_type = self.orchestrator.classify_query(
            "Write a Python function to sort a list", 
            []
        )
        assert query_type == QueryType.CODE_GENERATION
    
    def test_reasoning_classification(self):
        """Test that reasoning questions are classified correctly"""
        query_type = self.orchestrator.classify_query(
            "Why would you choose microservices over monoliths?", 
            []
        )
        assert query_type == QueryType.REASONING
    
    def test_creative_classification(self):
        """Test that creative requests are classified correctly"""
        query_type = self.orchestrator.classify_query(
            "Write a poem about AI", 
            []
        )
        assert query_type == QueryType.CREATIVE
    
    def test_context_aware_classification(self):
        """Test that previous context influences classification"""
        history = [
            {"role": "user", "content": "How do I write code?"},
            {"role": "assistant", "content": "Here's how..."}
        ]
        query_type = self.orchestrator.classify_query(
            "Show me an example", 
            history
        )
        # Should lean towards code generation due to context
        assert query_type == QueryType.CODE_GENERATION


class TestSystemPrompts:
    """Test system prompt generation"""
    
    def setup_method(self):
        self.orchestrator = AIOrchestrator()
    
    def test_code_prompt_includes_code_instructions(self):
        """Test that code-specific prompts are generated"""
        prompt = self.orchestrator.build_system_prompt(QueryType.CODE_GENERATION)
        assert "code" in prompt.lower()
        assert "algorithm" in prompt.lower()
    
    def test_reasoning_prompt_includes_reasoning_instructions(self):
        """Test that reasoning-specific prompts are generated"""
        prompt = self.orchestrator.build_system_prompt(QueryType.REASONING)
        assert "step-by-step" in prompt.lower() or "reason" in prompt.lower()
    
    def test_prompt_includes_tolu_context(self):
        """Test that user context is added to prompts"""
        context = "User is interested in AI and machine learning"
        prompt = self.orchestrator.build_system_prompt(
            QueryType.CONVERSATION,
            user_context=context
        )
        assert context in prompt


class TestConversationHistory:
    """Test conversation history compression"""
    
    def setup_method(self):
        self.orchestrator = AIOrchestrator()
    
    def test_short_history_not_compressed(self):
        """Test that short histories are not compressed"""
        history = [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello"}
        ]
        compressed = self.orchestrator.compress_conversation_history(history)
        assert len(compressed) == 2
    
    def test_long_history_is_compressed(self):
        """Test that long histories are compressed"""
        # Create 20 messages
        history = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i}"}
            for i in range(20)
        ]
        compressed = self.orchestrator.compress_conversation_history(
            history, 
            max_messages=8
        )
        # Should have system summary + 8 recent messages
        assert len(compressed) <= 9
        # First message should be system summary
        assert compressed[0]["role"] == "system"
    
    def test_compressed_history_maintains_context(self):
        """Test that compression maintains important context"""
        history = [
            {"role": "user", "content": "I'm learning AI"},
            {"role": "assistant", "content": "Great! Here are resources..."},
            *[
                {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i}"}
                for i in range(10, 20)
            ]
        ]
        compressed = self.orchestrator.compress_conversation_history(history)
        # Should have summary of beginning + recent messages
        summary = " ".join(msg.get("content", "") for msg in compressed)
        # The summary should mention AI from the first message
        assert any(msg.get("metadata", {}).get("type") == "context_summary" for msg in compressed) or \
               any("AI" in msg.get("content", "") for msg in compressed if msg.get("role") == "system")


class TestConversationMemory:
    """Test conversation memory management"""
    
    def setup_method(self):
        self.memory = ConversationMemory(max_session_age_hours=24)
    
    def test_session_creation(self):
        """Test creating a new session"""
        session = self.memory.create_session("test_session_1")
        assert session["id"] == "test_session_1"
        assert session["messages"] == []
    
    def test_add_message_to_session(self):
        """Test adding messages to a session"""
        self.memory.create_session("test_session_2")
        msg = self.memory.add_message(
            "test_session_2",
            "user",
            "Hello"
        )
        assert msg["role"] == "user"
        assert msg["content"] == "Hello"
        
        session = self.memory.get_session("test_session_2")
        assert len(session["messages"]) == 1
    
    def test_context_window_optimization(self):
        """Test context window optimization"""
        session_id = "test_session_3"
        self.memory.create_session(session_id)
        
        # Add 15 messages
        for i in range(15):
            role = "user" if i % 2 == 0 else "assistant"
            self.memory.add_message(session_id, role, f"Message {i}")
        
        # Get context window
        context = self.memory.get_context_window(
            session_id,
            include_recent=8,
            include_system_summary=True
        )
        
        # Should have system summary + 8 recent
        assert len(context) <= 9
    
    def test_session_statistics(self):
        """Test session statistics generation"""
        session_id = "test_session_4"
        self.memory.create_session(session_id)
        
        self.memory.add_message(session_id, "user", "Hello")
        self.memory.add_message(session_id, "assistant", "Hi there!")
        self.memory.add_message(session_id, "user", "How are you?")
        
        stats = self.memory.get_session_stats(session_id)
        assert stats["total_messages"] == 3
        assert stats["user_messages"] == 2
        assert stats["assistant_messages"] == 1
    
    def test_session_cleanup(self):
        """Test expired session cleanup"""
        self.memory.create_session("old_session")
        assert "old_session" in self.memory.sessions
        
        # Cleanup
        removed = self.memory.clear_session("old_session")
        assert removed
        assert "old_session" not in self.memory.sessions


class TestConversationContext:
    """Test conversation context building"""
    
    def setup_method(self):
        self.context = ConversationContext()
    
    def test_tolu_context_detection(self):
        """Test that Tolu-related queries get context"""
        should_include = self.context._should_include_tolu_context(
            "Tell me about your background"
        )
        assert should_include
    
    def test_non_tolu_context_detection(self):
        """Test that unrelated queries don't get Tolu context"""
        should_include = self.context._should_include_tolu_context(
            "What is quantum computing?"
        )
        assert not should_include
    
    def test_context_building(self):
        """Test full context building"""
        stats = {
            "user_messages": 5,
            "total_messages": 10
        }
        context = self.context.build_context_for_query(
            "Tell me more about machine learning",
            stats,
            ["AI basics", "Python programming"]
        )
        # Should include Tolu context for this query
        assert len(context) > 0


class TestModelConfig:
    """Test model configuration"""
    
    def setup_method(self):
        self.orchestrator = AIOrchestrator()
    
    def test_all_query_types_have_config(self):
        """Test that all query types have model configuration"""
        for query_type in QueryType:
            assert query_type in self.orchestrator.MODEL_CONFIG
    
    def test_config_has_required_fields(self):
        """Test that all configs have required fields"""
        required_fields = ["model", "temperature", "max_tokens"]
        for query_type, config in self.orchestrator.MODEL_CONFIG.items():
            for field in required_fields:
                assert field in config


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test that orchestrator initializes correctly"""
    orchestrator = AIOrchestrator()
    assert orchestrator.api_key is not None
    assert orchestrator.base_url == "https://api.venice.ai/api/v1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

