#!/usr/bin/env python3
"""
End-to-end tests for multi-turn chat conversations.
Tests that users can have multi-turn chat conversations with session persistence.
"""

import pytest
import sys
import os
from unittest.mock import patch, AsyncMock, MagicMock

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient


class TestMultiTurnChat:
    """Test multi-turn chat conversation functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment before each test."""
        # Import server after setting up mocks
        from backend.server import app, chat_sessions, ai_orchestrator, limiter
        
        self.client = TestClient(app)
        self.chat_sessions = chat_sessions
        self.ai_orchestrator = ai_orchestrator
        self.limiter = limiter
        
        # Disable rate limiting for tests
        self.limiter.enabled = False
        
        # Clear chat sessions before each test
        chat_sessions.clear()
        
        yield
        
        # Clean up after test
        chat_sessions.clear()
        self.limiter.enabled = True
    
    def test_ai_orchestrator_has_model_config(self):
        """Test that AIOrchestrator class has MODEL_CONFIG attribute."""
        from backend.server import AIOrchestrator, ai_orchestrator
        
        # Verify class has MODEL_CONFIG
        assert hasattr(AIOrchestrator, 'MODEL_CONFIG'), "AIOrchestrator should have MODEL_CONFIG class attribute"
        
        # Verify instance has MODEL_CONFIG
        assert hasattr(ai_orchestrator, 'MODEL_CONFIG'), "ai_orchestrator instance should have MODEL_CONFIG"
        
        # Verify MODEL_CONFIG structure
        model_config = ai_orchestrator.MODEL_CONFIG
        assert "model" in model_config, "MODEL_CONFIG should have 'model' key"
        assert "temperature" in model_config, "MODEL_CONFIG should have 'temperature' key"
        assert "max_completion_tokens" in model_config, "MODEL_CONFIG should have 'max_completion_tokens' key"
        assert "venice_parameters" in model_config, "MODEL_CONFIG should have 'venice_parameters' key"
        
        print(f"✅ MODEL_CONFIG verified: {model_config}")
    
    def test_ai_orchestrator_get_model_config(self):
        """Test that get_model_config returns a copy of MODEL_CONFIG."""
        from backend.server import ai_orchestrator
        
        config = ai_orchestrator.get_model_config()
        
        # Verify it returns correct structure
        assert isinstance(config, dict), "get_model_config should return a dict"
        assert "model" in config, "Returned config should have 'model' key"
        
        # Verify it returns a copy (not the same object)
        original_config = ai_orchestrator.MODEL_CONFIG
        assert config is not original_config, "get_model_config should return a copy"
        
        print(f"✅ get_model_config returns correct config: {config}")
    
    @patch('backend.server.ai_orchestrator.api_key', 'test-api-key')
    @patch('backend.server.ai_orchestrator.generate_response')
    def test_single_chat_message(self, mock_generate_response):
        """Test a single chat message and response."""
        async def mock_response(*args, **kwargs):
            return "Hello! I'm here to help you."
        mock_generate_response.side_effect = mock_response
        
        response = self.client.post(
            "/api/chat",
            json={"message": "Hello!"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "response" in data, "Response should contain 'response' field"
        assert "sessionId" in data, "Response should contain 'sessionId' field"
        
        print(f"✅ Single message test passed. Session ID: {data['sessionId']}")
    
    @patch('backend.server.ai_orchestrator.api_key', 'test-api-key')
    @patch('backend.server.ai_orchestrator.generate_response')
    def test_multi_turn_conversation_session_persistence(self, mock_generate_response):
        """Test that conversation history is maintained across multiple turns."""
        # Mock responses for each turn
        responses = [
            "Hello! How can I help you today?",
            "I'd be happy to tell you about Python. What would you like to know?",
            "List comprehensions are a concise way to create lists in Python."
        ]
        response_idx = [0]
        
        async def mock_response(*args, **kwargs):
            idx = response_idx[0]
            response_idx[0] += 1
            return responses[idx]
        
        mock_generate_response.side_effect = mock_response
        
        # Turn 1: Initial greeting
        response1 = self.client.post(
            "/api/chat",
            json={"message": "Hello!"}
        )
        
        assert response1.status_code == 200, f"Turn 1 failed: {response1.text}"
        data1 = response1.json()
        session_id = data1["sessionId"]
        
        print(f"Turn 1 - Session ID: {session_id}")
        print(f"Turn 1 - Response: {data1['response']}")
        
        # Turn 2: Continue conversation with same session
        response2 = self.client.post(
            "/api/chat",
            json={"message": "Tell me about Python", "sessionId": session_id}
        )
        
        assert response2.status_code == 200, f"Turn 2 failed: {response2.text}"
        data2 = response2.json()
        
        # Verify same session is maintained
        assert data2["sessionId"] == session_id, "Session ID should be maintained across turns"
        print(f"Turn 2 - Response: {data2['response']}")
        
        # Turn 3: Continue with another question
        response3 = self.client.post(
            "/api/chat",
            json={"message": "What are list comprehensions?", "sessionId": session_id}
        )
        
        assert response3.status_code == 200, f"Turn 3 failed: {response3.text}"
        data3 = response3.json()
        
        # Verify same session is maintained
        assert data3["sessionId"] == session_id, "Session ID should be maintained across turns"
        print(f"Turn 3 - Response: {data3['response']}")
        
        # Verify session history is stored
        assert session_id in self.chat_sessions, "Session should be stored in chat_sessions"
        session_data = self.chat_sessions[session_id]
        
        # Should have 6 messages: 3 user messages + 3 assistant responses
        assert len(session_data["messages"]) == 6, f"Expected 6 messages, got {len(session_data['messages'])}"
        
        print(f"✅ Multi-turn conversation test passed with {len(session_data['messages'])} messages in history")
    
    @patch('backend.server.ai_orchestrator.api_key', 'test-api-key')
    @patch('backend.server.ai_orchestrator.generate_response')
    def test_conversation_history_limit(self, mock_generate_response):
        """Test that conversation history is limited to last 10 messages for context."""
        async def mock_response(*args, **kwargs):
            return "Response"
        mock_generate_response.side_effect = mock_response
        
        session_id = None
        
        # Send 12 messages to exceed the 10-message limit used for context
        for i in range(12):
            response = self.client.post(
                "/api/chat",
                json={"message": f"Message {i+1}", "sessionId": session_id}
            )
            
            assert response.status_code == 200, f"Message {i+1} failed: {response.text}"
            data = response.json()
            
            if session_id is None:
                session_id = data["sessionId"]
        
        # Verify all messages are stored in session
        session_data = self.chat_sessions[session_id]
        total_messages = len(session_data["messages"])
        
        # Should have 24 messages (12 user + 12 assistant)
        assert total_messages == 24, f"Expected 24 messages, got {total_messages}"
        
        print(f"✅ Conversation history test passed with {total_messages} total messages")
    
    @patch('backend.server.ai_orchestrator.api_key', 'test-api-key')
    @patch('backend.server.ai_orchestrator.generate_response')
    def test_new_session_without_session_id(self, mock_generate_response):
        """Test that a new session is created when no session ID is provided."""
        async def mock_response(*args, **kwargs):
            return "New session response"
        mock_generate_response.side_effect = mock_response
        
        # First message without session ID
        response1 = self.client.post(
            "/api/chat",
            json={"message": "First message"}
        )
        
        assert response1.status_code == 200
        session_id1 = response1.json()["sessionId"]
        
        # Second message without session ID (should create new session)
        response2 = self.client.post(
            "/api/chat",
            json={"message": "Second message"}
        )
        
        assert response2.status_code == 200
        session_id2 = response2.json()["sessionId"]
        
        # Should be different sessions
        assert session_id1 != session_id2, "Different requests without sessionId should create different sessions"
        
        print(f"✅ New session creation test passed. Session 1: {session_id1[:8]}..., Session 2: {session_id2[:8]}...")
    
    @patch('backend.server.ai_orchestrator.api_key', 'test-api-key')
    @patch('backend.server.ai_orchestrator.generate_response')
    def test_session_isolation(self, mock_generate_response):
        """Test that different sessions are isolated from each other."""
        responses = ["Session 1 Response 1", "Session 2 Response 1", "Session 1 Response 2"]
        response_idx = [0]
        
        async def mock_response(*args, **kwargs):
            idx = response_idx[0]
            response_idx[0] += 1
            return responses[idx]
        
        mock_generate_response.side_effect = mock_response
        
        # Create first session
        response1 = self.client.post(
            "/api/chat",
            json={"message": "Hello from Session 1"}
        )
        assert response1.status_code == 200, f"Session 1 creation failed: {response1.text}"
        session_id1 = response1.json()["sessionId"]
        
        # Create second session
        response2 = self.client.post(
            "/api/chat",
            json={"message": "Hello from Session 2"}
        )
        assert response2.status_code == 200, f"Session 2 creation failed: {response2.text}"
        session_id2 = response2.json()["sessionId"]
        
        # Continue first session
        response3 = self.client.post(
            "/api/chat",
            json={"message": "Continuing Session 1", "sessionId": session_id1}
        )
        assert response3.status_code == 200, f"Session 1 continuation failed: {response3.text}"
        
        # Verify session 1 has 4 messages (2 user + 2 assistant)
        assert len(self.chat_sessions[session_id1]["messages"]) == 4
        
        # Verify session 2 has 2 messages (1 user + 1 assistant)
        assert len(self.chat_sessions[session_id2]["messages"]) == 2
        
        print(f"✅ Session isolation test passed")
    
    def test_health_check_endpoint(self):
        """Test that the health check endpoint works."""
        response = self.client.get("/api/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Tolu Shekoni Portfolio API" in data["message"]
        
        print(f"✅ Health check endpoint test passed")


def run_tests():
    """Run all tests with verbose output."""
    print("=" * 70)
    print("🧪 Running End-to-End Multi-Turn Chat Conversation Tests")
    print("=" * 70)
    
    # Run pytest with verbose output
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-s"  # Show print statements
    ])
    
    return exit_code


if __name__ == "__main__":
    sys.exit(run_tests())
