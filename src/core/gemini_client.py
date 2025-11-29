"""Gemini API client for embeddings and text generation."""

import google.generativeai as genai
from typing import List, Optional
import time
from config.settings import GOOGLE_API_KEY, GEMINI_MODEL, GEMINI_EMBEDDING_MODEL


class GeminiClient:
    """Client for interacting with Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client."""
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.embedding_model = GEMINI_EMBEDDING_MODEL
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return []
    
    def create_query_embedding(self, query: str) -> List[float]:
        """
        Create embedding for search query.
        
        Args:
            query: Search query
            
        Returns:
            List of floats representing the embedding
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error creating query embedding: {e}")
            return []
    
    def generate(
        self, 
        prompt: str, 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text response.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            generation_config = {
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 40,
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Return text - Gemini handles UTF-8 properly
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.7
    ):
        """
        Generate text response with streaming.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            
        Yields:
            Text chunks as they're generated
        """
        try:
            generation_config = {
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 40,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error: {str(e)}"
