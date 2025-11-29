"""
Setup script for Drishti AI - Creates embeddings from Bhagavad Gita CSV.

Run this script once to initialize the vector database:
    python setup.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.embedding_manager import EmbeddingManager
from src.core.data_processor import DataProcessor
from config.settings import DATA_DIR


def main():
    """Main setup function."""
    print("=" * 60)
    print("🕉️  Drishti AI - Setup & Initialization")
    print("=" * 60)
    print()
    
    # Check if CSV exists
    csv_path = DATA_DIR / "bhagavad_gita.csv"
    if not csv_path.exists():
        print("❌ ERROR: Bhagavad Gita CSV not found!")
        print(f"   Expected location: {csv_path}")
        print()
        print("Please add your CSV file with columns:")
        print("   - chapter")
        print("   - verse")
        print("   - sanskrit")
        print("   - hindi")
        print("   - english")
        print()
        return
    
    print(f"✅ Found CSV: {csv_path}")
    print()
    
    # Load data
    print("📖 Loading Bhagavad Gita data...")
    processor = DataProcessor(str(csv_path))
    df = processor.load_csv()
    print(f"   Loaded {len(df)} verses")
    print()
    
    # Create embeddings
    print("🔮 Creating embeddings with Gemini...")
    print("   This may take 5-10 minutes for 700 verses...")
    print()
    
    embedding_manager = EmbeddingManager()
    embedding_manager.create_embeddings(force_recreate=True)
    
    print()
    print("=" * 60)
    print("✨ Setup Complete!")
    print("=" * 60)
    print()
    print("You can now run the application:")
    print("   streamlit run app.py")
    print()
    print("सत्यमेव जयते")
    print("ॐ नमो भगवते वासुदेवाय")
    print()


if __name__ == "__main__":
    main()
