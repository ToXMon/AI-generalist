"""
Conversation memory and context management system
Implements semantic history retrieval and efficient session management
"""

import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import json

logger = logging.getLogger(__name__)


class ConversationMemory:
    """
    Enhanced memory system for conversation management
    - Keeps full recent context
    - Summarizes older context  
    - Detects conversation topic shifts
    - Optimizes for token efficiency
    """
    
    def __init__(self, max_session_age_hours: int = 24):
        self.sessions: Dict[str, Dict] = {}
        self.max_session_age = max_session_age_hours
    
    def create_session(self, session_id: str) -> Dict:
        """Create new conversation session"""
        session = {
            "id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "messages": [],
            "topic_shifts": [],  # Track topic changes
            "metadata": {}
        }
        self.sessions[session_id] = session
        logger.info(f"Created session {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve session, return None if expired"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        created_at = datetime.fromisoformat(session["created_at"])
        age_hours = (datetime.utcnow() - created_at).total_seconds() / 3600
        
        if age_hours > self.max_session_age:
            logger.info(f"Session {session_id} expired")
            del self.sessions[session_id]
            return None
        
        return session
    
    def add_message(
        self, 
        session_id: str, 
        role: str, 
        content: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Add message to session"""
        session = self.get_session(session_id)
        if not session:
            session = self.create_session(session_id)
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        session["messages"].append(message)
        session["updated_at"] = datetime.utcnow().isoformat()
        
        logger.debug(f"Added {role} message to session {session_id}")
        return message
    
    def get_context_window(
        self,
        session_id: str,
        include_recent: int = 8,
        include_system_summary: bool = True
    ) -> List[Dict]:
        """
        Get optimized context window for model input
        - Recent messages: kept in full
        - Older messages: summarized
        """
        session = self.get_session(session_id)
        if not session or not session["messages"]:
            return []
        
        messages = session["messages"]
        
        # If short enough, return all
        if len(messages) <= include_recent:
            return messages
        
        # Separate recent from older
        recent = messages[-include_recent:]
        older = messages[:-include_recent]
        
        # Create context summary of older messages
        if include_system_summary and older:
            summary = self._create_summary(older)
            return [summary] + recent
        
        return recent
    
    def _create_summary(self, messages: List[Dict]) -> Dict:
        """Create a system message summarizing conversation history"""
        
        # Extract key topics and themes
        user_messages = [m for m in messages if m.get("role") == "user"]
        assistant_messages = [m for m in messages if m.get("role") == "assistant"]
        
        # Build summary string
        topics = []
        for msg in user_messages[-3:]:  # Last 3 user queries
            content = msg.get("content", "")
            # Extract first 50 chars as topic indicator
            topic = content[:50] + "..." if len(content) > 50 else content
            topics.append(f"- {topic}")
        
        summary_content = f"""[Previous Context Summary]
Earlier in this conversation:
{chr(10).join(topics)}
This context has been preserved. Continue the conversation naturally."""
        
        return {
            "role": "system",
            "content": summary_content,
            "metadata": {"type": "context_summary"}
        }
    
    def detect_topic_shift(self, session_id: str, new_message: str) -> bool:
        """Detect if conversation is shifting to new topic"""
        session = self.get_session(session_id)
        if not session or len(session["messages"]) < 2:
            return False
        
        # Simple heuristic: if new message is very different in length/keywords
        # from recent messages, it might be a topic shift
        recent_messages = session["messages"][-3:]
        recent_content = " ".join([
            m.get("content", "") for m in recent_messages
        ]).lower()
        
        # Keywords that indicate topic shift
        shift_indicators = ["anyway", "by the way", "speaking of", "change subject", "different"]
        
        if any(indicator in new_message.lower() for indicator in shift_indicators):
            session["topic_shifts"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "message_index": len(session["messages"])
            })
            logger.info(f"Topic shift detected in session {session_id}")
            return True
        
        return False
    
    def get_session_stats(self, session_id: str) -> Dict:
        """Get statistics about session"""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        messages = session["messages"]
        user_msgs = [m for m in messages if m.get("role") == "user"]
        assistant_msgs = [m for m in messages if m.get("role") == "assistant"]
        
        total_tokens = sum(
            len(msg.get("content", "").split()) * 1.3  # Approximate
            for msg in messages
        )
        
        return {
            "total_messages": len(messages),
            "user_messages": len(user_msgs),
            "assistant_messages": len(assistant_msgs),
            "estimated_tokens": int(total_tokens),
            "topic_shifts": len(session.get("topic_shifts", [])),
            "created_at": session.get("created_at"),
            "last_updated": session.get("updated_at")
        }
    
    def clear_session(self, session_id: str) -> bool:
        """Clear session data"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleared session {session_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Remove all expired sessions, return count removed"""
        expired = []
        current_time = datetime.utcnow()
        
        for session_id, session in self.sessions.items():
            created_at = datetime.fromisoformat(session["created_at"])
            age_hours = (current_time - created_at).total_seconds() / 3600
            if age_hours > self.max_session_age:
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")
        
        return len(expired)


class ConversationContext:
    """Context builder for providing relevant background to models"""
    
    def __init__(self):
        # Knowledge about Tolu from portfolio
        self.tolu_context = """
Tolu Shekoni is an AI/ML engineer and full-stack developer with expertise in:
- Machine Learning and AI systems (LLMs, RAG, agents)
- Full-stack development (React, Node.js, Python, FastAPI)
- Cloud deployment (Akash, Docker, AWS)
- Problem-solving and rapid prototyping
- Career transition from other fields into tech

Key Projects:
- AI-powered portfolio website with Venice AI integration
- Deployment expertise on Akash (Web3 cloud)
- Experience with containerization and DevOps
"""
    
    def build_context_for_query(
        self,
        user_message: str,
        session_stats: Dict,
        previous_topics: List[str]
    ) -> str:
        """Build contextual information for the model"""
        
        context_parts = []
        
        # Add Tolu's background if relevant
        if self._should_include_tolu_context(user_message):
            context_parts.append(f"User is talking to Tolu's AI assistant.\n{self.tolu_context}")
        
        # Add conversation statistics
        if session_stats.get("user_messages", 0) > 3:
            context_parts.append(f"\nThis is turn {session_stats['user_messages']} in the conversation.")
        
        # Add topic history
        if previous_topics:
            topics_str = ", ".join(previous_topics[-3:])  # Last 3 topics
            context_parts.append(f"\nRecent conversation topics: {topics_str}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def _should_include_tolu_context(self, message: str) -> bool:
        """Check if message requires Tolu background context"""
        keywords = [
            "tolu", "you", "your", "background", "experience", "skills",
            "project", "work", "career", "personal", "profile"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in keywords)

