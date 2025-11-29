"""In-memory embedding manager for Streamlit Cloud deployment."""

from typing import List, Dict, Optional
import numpy as np
from src.core.gemini_client import GeminiClient
from src.core.data_processor import DataProcessor


class InMemoryEmbeddingManager:
    """Manage embeddings in memory for Streamlit Cloud (read-only filesystem)."""
    
    def __init__(self):
        """Initialize in-memory embedding manager."""
        self.gemini_client = GeminiClient()
        self.embeddings_data = {
            'ids': [],
            'embeddings': [],
            'documents': [],
            'metadatas': []
        }
        self.initialized = False
    
    def initialize_collection(self):
        """Initialize collection (no-op for in-memory)."""
        self.initialized = True
        print(f"In-memory collection initialized")
        print(f"Current count: {len(self.embeddings_data['ids'])} verses")
    
    def create_embeddings(self, force_recreate: bool = False):
        """
        Create embeddings for all verses in memory.
        
        Args:
            force_recreate: If True, recreate all embeddings
        """
        if len(self.embeddings_data['ids']) > 0 and not force_recreate:
            print(f"Embeddings already exist ({len(self.embeddings_data['ids'])} verses)")
            return
        
        if force_recreate:
            self.embeddings_data = {
                'ids': [],
                'embeddings': [],
                'documents': [],
                'metadatas': []
            }
        
        # Load and process data
        processor = DataProcessor()
        verses_data = processor.process_for_embeddings()
        
        # Deduplicate by verse ID
        seen_ids = set()
        unique_verses = []
        for verse in verses_data:
            verse_id = verse['id']
            if verse_id not in seen_ids:
                seen_ids.add(verse_id)
                unique_verses.append(verse)
        
        print(f"Processing {len(unique_verses)} unique verses")
        
        # Create embeddings in batches
        batch_size = 10
        for i in range(0, len(unique_verses), batch_size):
            batch = unique_verses[i:i+batch_size]
            
            for verse in batch:
                # Create embedding
                embedding = self.gemini_client.create_embedding(verse['text'])
                
                # Store in memory
                self.embeddings_data['ids'].append(verse['id'])
                self.embeddings_data['embeddings'].append(embedding)
                self.embeddings_data['documents'].append(verse['text'])
                self.embeddings_data['metadatas'].append(verse['metadata'])
            
            print(f"Processed {min(i + batch_size, len(unique_verses))}/{len(unique_verses)} verses")
        
        print(f"✅ Created embeddings for {len(unique_verses)} verses in memory")
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar verses using cosine similarity.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of matching verses with metadata
        """
        if len(self.embeddings_data['ids']) == 0:
            return []
        
        # Create query embedding
        query_embedding = self.gemini_client.create_query_embedding(query)
        
        # Calculate cosine similarities
        similarities = []
        for i, emb in enumerate(self.embeddings_data['embeddings']):
            # Cosine similarity
            similarity = np.dot(query_embedding, emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(emb)
            )
            similarities.append((i, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top k results
        results = []
        for idx, similarity in similarities[:top_k]:
            results.append({
                'id': self.embeddings_data['ids'][idx],
                'text': self.embeddings_data['documents'][idx],
                'metadata': self.embeddings_data['metadatas'][idx],
                'distance': 1 - similarity  # Convert similarity to distance
            })
        
        return results
    
    def get_verse_by_id(self, verse_id: str) -> Optional[Dict]:
        """
        Get specific verse by ID.
        
        Args:
            verse_id: Verse ID (e.g., "2.47")
            
        Returns:
            Verse data or None
        """
        try:
            idx = self.embeddings_data['ids'].index(verse_id)
            return {
                'id': self.embeddings_data['ids'][idx],
                'text': self.embeddings_data['documents'][idx],
                'metadata': self.embeddings_data['metadatas'][idx]
            }
        except ValueError:
            return None
    
    def get_stats(self) -> Dict:
        """Get collection statistics."""
        return {
            'total_verses': len(self.embeddings_data['ids']),
            'collection_name': 'in_memory_bhagavad_gita',
            'storage_path': 'memory'
        }
