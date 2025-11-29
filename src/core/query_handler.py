"""Query handler orchestrating the complete RAG pipeline."""

from typing import Dict, Generator
from .context_engineer import ContextEngineer
from .gemini_client import GeminiClient


class QueryHandler:
    """Handle queries through the complete RAG pipeline."""
    
    def __init__(self):
        """Initialize query handler."""
        self.context_engineer = ContextEngineer()
        self.gemini_client = GeminiClient()
    
    def process_query(
        self,
        query: str,
        tone: str = 'modern',
        language: str = 'english',
        search_mode: str = 'gita',
        stream: bool = False
    ):
        """
        Process query through RAG pipeline.
        
        Args:
            query: User query
            tone: Response tone
            language: Response language
            search_mode: 'gita' or 'universal'
            stream: Whether to stream response
            
        Returns:
            Response string or generator if streaming
        """
        if stream:
            return self._process_query_stream(query, tone, language, search_mode)
        else:
            return self.context_engineer.engineer_response(
                query=query,
                tone=tone,
                language=language,
                search_mode=search_mode
            )
    
    def _process_query_stream(
        self,
        query: str,
        tone: str,
        language: str,
        search_mode: str
    ) -> Generator[str, None, None]:
        """Process query with streaming response."""
        # For now, return non-streaming response
        # Streaming can be enhanced later
        response = self.context_engineer.engineer_response(
            query=query,
            tone=tone,
            language=language,
            search_mode=search_mode
        )
        yield response
