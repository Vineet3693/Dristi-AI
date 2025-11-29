"""Application settings and configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# API Keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

# Paths
DATA_DIR = PROJECT_ROOT / 'data'
ASSETS_DIR = PROJECT_ROOT / 'assets'
CONFIG_DIR = PROJECT_ROOT / 'config'
CHROMADB_PATH = os.getenv('CHROMADB_PATH', str(PROJECT_ROOT / 'chromadb_storage'))

# ChromaDB Settings
CHROMADB_COLLECTION_NAME = 'bhagavad_gita'

# Gemini Models - Using latest stable 2.0 Flash
GEMINI_MODEL = 'gemini-2.5-pro'  # Latest stable version with good rate limits
GEMINI_EMBEDDING_MODEL = 'models/text-embedding-004'  # Embedding model keeps 'models/' prefix

# Generation Settings
GENERATION_CONFIG = {
    'temperature': 0.7,
    'top_p': 0.95,
    'top_k': 40,
    'max_output_tokens': 2048,
}

# RAG Settings
TOP_K_RESULTS = 10
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# UI Settings
APP_TITLE = "Drishti AI - Divine Wisdom from Bhagavad Gita"
APP_ICON = "🕉️"

# Supported Languages
LANGUAGES = {
    'hindi': 'हिंदी',
    'english': 'English',
    'sanskrit': 'संस्कृत'
}

# Response Tones
RESPONSE_TONES = {
    'spiritual': '🕉️ Spiritual & Poetic',
    'scholarly': '🧠 Scholarly',
    'modern': '💬 Modern & Relatable',
    'devotional': '🙏 Devotional'
}

# Search Modes
SEARCH_MODES = {
    'gita': 'Bhagavad Gita Mode',
    'universal': 'Universal Mode'
}
