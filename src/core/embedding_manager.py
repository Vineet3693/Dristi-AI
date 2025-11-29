"""ChromaDB embedding manager for persistent vector storage."""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from pathlib import Path
from config.settings import CHROMADB_PATH, CHROMADB_COLLECTION_NAME
from .gemini_client import GeminiClient
from .data_processor import DataProcessor


class EmbeddingManager:
    """Manage ChromaDB embeddings for Bhagavad Gita."""
    
    def __init__(self):
        """Initialize embedding manager."""
        try:
            # Try to use persistent client (works locally and reads from GitHub on cloud)
            self.client = chromadb.PersistentClient(path=CHROMADB_PATH)
        except Exception as e:
            print(f"Note: Using read-only mode - {e}")
            # Fallback: still try persistent client, it can read even if it can't write
            self.client = chromadb.PersistentClient(path=CHROMADB_PATH)
        
        self.gemini_client = GeminiClient()
        self.collection = None
    
    def initialize_collection(self):
        """Initialize or get existing collection."""
        try:
            self.collection = self.client.get_or_create_collection(
                name=CHROMADB_COLLECTION_NAME,
                metadata={"description": "Bhagavad Gita verses with embeddings"}
            )
            print(f"Collection '{CHROMADB_COLLECTION_NAME}' initialized")
            print(f"Current count: {self.collection.count()} verses")
        except Exception as e:
            print(f"Error initializing collection: {e}")
    
    def create_embeddings(self, force_recreate: bool = False):
        """
        Create embeddings for all verses.
        
        Args:
            force_recreate: If True, delete and recreate all embeddings
        """
        if self.collection is None:
            self.initialize_collection()
        
        # Check if embeddings already exist
        if self.collection.count() > 0 and not force_recreate:
            print(f"Embeddings already exist ({self.collection.count()} verses)")
            print("Use force_recreate=True to recreate")
            return
        
        # Delete existing if force recreate
        if force_recreate and self.collection.count() > 0:
            print("Deleting existing embeddings...")
            self.client.delete_collection(CHROMADB_COLLECTION_NAME)
            self.initialize_collection()
        
        # Load and process data
        processor = DataProcessor()
        verses_data = processor.process_for_embeddings()
        
        # Deduplicate by verse ID (keep first occurrence)
        seen_ids = set()
        unique_verses = []
        for verse in verses_data:
            verse_id = verse['id']
            if verse_id not in seen_ids:
                seen_ids.add(verse_id)
                unique_verses.append(verse)
        
        print(f"Processing {len(unique_verses)} unique verses (removed {len(verses_data) - len(unique_verses)} duplicates)")
        
        # Create embeddings in batches
        batch_size = 10
        for i in range(0, len(unique_verses), batch_size):
            batch = unique_verses[i:i+batch_size]
            
            ids = [v['id'] for v in batch]
            texts = [v['text'] for v in batch]
            metadatas = [v['metadata'] for v in batch]
            
            # Create embeddings
            embeddings = []
            for text in texts:
                embedding = self.gemini_client.create_embedding(text)
                embeddings.append(embedding)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            
            print(f"Processed {min(i + batch_size, len(unique_verses))}/{len(unique_verses)} verses")
        
        print(f"✅ Created embeddings for {len(unique_verses)} verses")
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar verses.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of matching verses with metadata
        """
        if self.collection is None:
            self.initialize_collection()
        
        # Create query embedding
        query_embedding = self.gemini_client.create_query_embedding(query)
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
        
        return formatted_results
    
    def get_verse_by_id(self, verse_id: str) -> Optional[Dict]:
        """
        Get specific verse by ID.
        
        Args:
            verse_id: Verse ID (e.g., "2.47")
            
        Returns:
            Verse data or None
        """
        if self.collection is None:
            self.initialize_collection()
        
        try:
            result = self.collection.get(
                ids=[verse_id],
                include=['documents', 'metadatas']
            )
            
            if result['ids']:
                return {
                    'id': result['ids'][0],
                    'text': result['documents'][0],
                    'metadata': result['metadatas'][0]
                }
        except Exception as e:
            print(f"Error getting verse: {e}")
        
        return None
    
    def get_stats(self) -> Dict:
        """Get collection statistics."""
        if self.collection is None:
            self.initialize_collection()
        
        return {
            'total_verses': self.collection.count(),
            'collection_name': CHROMADB_COLLECTION_NAME,
            'storage_path': CHROMADB_PATH
        }
