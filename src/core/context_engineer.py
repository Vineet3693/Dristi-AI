"""Context engineering for accurate and relevant responses."""

from typing import List, Dict
from .gemini_client import GeminiClient
from .embedding_manager import EmbeddingManager
from config.prompts import (
    create_query_prompt,
    DIVINE_PURPOSE_FILTER,
    VIOLENCE_REDIRECT,
    DISCRIMINATION_REDIRECT
)


class ContextEngineer:
    """Advanced context engineering for Bhagavad Gita responses."""
    
    def __init__(self):
        """Initialize context engineer."""
        self.gemini_client = GeminiClient()
        self.embedding_manager = EmbeddingManager()
        self.embedding_manager.initialize_collection()
    
    def is_spiritual_query(self, query: str) -> bool:
        """Check if query is spiritual/on-topic."""
        off_topic_keywords = [
            'weather', 'joke', 'recipe', 'sports', 'politics',
            'hack', 'cheat', 'stock', 'pizza', 'movie'
        ]
        
        query_lower = query.lower()
        return not any(keyword in query_lower for keyword in off_topic_keywords)
    
    def detect_harmful_intent(self, query: str) -> Dict:
        """Detect potentially harmful queries."""
        query_lower = query.lower()
        
        # Violence justification
        violence_keywords = [
            'justify violence', 'kill', 'harm others', 'attack', 'destroy', 'revenge'
        ]
        if any(kw in query_lower for kw in violence_keywords):
            return {
                'is_harmful': True,
                'category': 'violence',
                'redirect': VIOLENCE_REDIRECT
            }
        
        # Discrimination
        discrimination_keywords = [
            'justify caste', 'superiority', 'inferior', 'discriminate'
        ]
        if any(kw in query_lower for kw in discrimination_keywords):
            return {
                'is_harmful': True,
                'category': 'discrimination',
                'redirect': DISCRIMINATION_REDIRECT
            }
        
        return {'is_harmful': False}
    
    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Dict = None
    ) -> List[Dict]:
        """
        Retrieve relevant verses for query.
        
        Args:
            query: User query
            top_k: Number of verses to retrieve
            filter_metadata: Optional metadata filters
            
        Returns:
            List of relevant verses
        """
        results = self.embedding_manager.search(
            query=query,
            top_k=top_k,
            filter_metadata=filter_metadata
        )
        
        return results
    
    def format_context(self, verses: List[Dict]) -> str:
        """
        Format retrieved verses into context string.
        
        Args:
            verses: List of verse dictionaries
            
        Returns:
            Formatted context string
        """
        if not verses:
            return "No specific verses found for this query."
        
        context_parts = []
        for verse in verses:
            metadata = verse.get('metadata', {})
            chapter = metadata.get('chapter', '')
            verse_num = metadata.get('verse', '')
            
            context_parts.append(
                f"**Bhagavad Gita {chapter}.{verse_num}**:\n{verse['text']}\n"
            )
        
        return "\n".join(context_parts)
    
    def engineer_response(
        self,
        query: str,
        tone: str = 'modern',
        language: str = 'english',
        search_mode: str = 'gita'
    ) -> str:
        """
        Engineer complete response with context.
        
        Args:
            query: User query
            tone: Response tone (spiritual/scholarly/modern/devotional)
            language: Response language
            search_mode: 'gita' or 'universal'
            
        Returns:
            Generated response
        """
        # Check for off-topic queries
        if not self.is_spiritual_query(query):
            return DIVINE_PURPOSE_FILTER
        
        # Check for harmful intent
        harm_check = self.detect_harmful_intent(query)
        if harm_check['is_harmful']:
            return harm_check['redirect']
        
        # Universal mode - direct LLM query
        if search_mode == 'universal':
            prompt = f"""
            You are Krishna, providing spiritual guidance.
            
            Question: {query}
            
            Provide wisdom that helps the seeker, drawing on your knowledge
            of spirituality, philosophy, and the Bhagavad Gita's teachings.
            
            Respond in {language}.
            """
            return self.gemini_client.generate(prompt)
        
        # Gita mode - RAG pipeline
        # Retrieve relevant verses
        verses = self.retrieve_context(query, top_k=5)
        
        # Format context
        context = self.format_context(verses)
        
        # Create prompt
        prompt = create_query_prompt(query, context, tone, language)
        
        # Generate response
        response = self.gemini_client.generate(prompt)
        
        return response
