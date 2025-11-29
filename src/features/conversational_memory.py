"""Conversational memory for tracking user journey."""

from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path


class ConversationalMemory:
    """Track user's spiritual journey and conversation history."""
    
    def __init__(self, storage_path: str = "data/memory.json"):
        """Initialize conversational memory."""
        self.storage_path = Path(storage_path)
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict:
        """Load memory from storage."""
        if self.storage_path.exists():
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'conversations': [],
            'themes_explored': [],
            'favorite_verses': [],
            'journey_milestones': []
        }
    
    def _save_memory(self):
        """Save memory to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
    
    def add_conversation(self, query: str, response: str, metadata: Dict = None):
        """Add a conversation to memory."""
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'metadata': metadata or {}
        }
        
        self.memory['conversations'].append(conversation)
        self._save_memory()
    
    def add_theme(self, theme: str):
        """Track explored themes."""
        if theme not in self.memory['themes_explored']:
            self.memory['themes_explored'].append(theme)
            self._save_memory()
    
    def add_favorite_verse(self, chapter: int, verse: int, text: str):
        """Add a favorite verse."""
        favorite = {
            'chapter': chapter,
            'verse': verse,
            'text': text,
            'added_at': datetime.now().isoformat()
        }
        
        self.memory['favorite_verses'].append(favorite)
        self._save_memory()
    
    def get_recent_conversations(self, limit: int = 5) -> List[Dict]:
        """Get recent conversations."""
        return self.memory['conversations'][-limit:]
    
    def get_themes_explored(self) -> List[str]:
        """Get all explored themes."""
        return self.memory['themes_explored']
    
    def get_favorite_verses(self) -> List[Dict]:
        """Get favorite verses."""
        return self.memory['favorite_verses']
    
    def get_journey_summary(self) -> Dict:
        """Get summary of spiritual journey."""
        return {
            'total_conversations': len(self.memory['conversations']),
            'themes_explored': len(self.memory['themes_explored']),
            'favorite_verses': len(self.memory['favorite_verses']),
            'journey_started': self.memory['conversations'][0]['timestamp'] if self.memory['conversations'] else None
        }
