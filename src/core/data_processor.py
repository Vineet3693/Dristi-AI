"""CSV data processor for Bhagavad Gita."""

import pandas as pd
from typing import List, Dict
from pathlib import Path
from config.settings import DATA_DIR


class DataProcessor:
    """Process Bhagavad Gita CSV data."""
    
    def __init__(self, csv_path: str = None):
        """
        Initialize data processor.
        
        Args:
            csv_path: Path to CSV file (defaults to data/bhagavad_gita.csv)
        """
        if csv_path is None:
            csv_path = DATA_DIR / 'bhagavad_gita.csv'
        
        self.csv_path = Path(csv_path)
        self.df = None
    
    def load_csv(self) -> pd.DataFrame:
        """
        Load Bhagavad Gita CSV file.
        
        Returns:
            DataFrame with standardized columns
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        # Load CSV
        df = pd.read_csv(self.csv_path, encoding='utf-8')
        
        # Extract chapter and verse from verse_number (e.g., "Chapter 1, Verse 1")
        if 'verse_number' in df.columns:
            # Parse "Chapter X, Verse Y" format
            df[['chapter', 'verse']] = df['verse_number'].str.extract(r'Chapter (\d+), Verse (\d+)')
            df['chapter'] = df['chapter'].astype(int)
            df['verse'] = df['verse'].astype(int)
        
        # Map text columns
        column_mapping = {
            'verse_in_sanskrit': 'sanskrit',
            'verse_in_hindi': 'hindi_verse',
            'verse_in_english': 'english_verse',
            'translation_in_hindi': 'hindi',
            'translation_in_english': 'english'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Combine verse and translation for better context
        if 'hindi_verse' in df.columns and 'hindi' in df.columns:
            df['hindi'] = df['hindi_verse'].fillna('') + ' ' + df['hindi'].fillna('')
        if 'english_verse' in df.columns and 'english' in df.columns:
            df['english'] = df['english_verse'].fillna('') + ' ' + df['english'].fillna('')
        
        # Select only required columns
        required_cols = ['chapter', 'verse', 'sanskrit', 'hindi', 'english']
        df = df[required_cols]
        
        self.df = df
        print(f"Loaded {len(df)} verses from {self.csv_path}")
        return df
    
    def get_verse(self, chapter: int, verse: int) -> Dict:
        """
        Get specific verse.
        
        Args:
            chapter: Chapter number
            verse: Verse number
            
        Returns:
            Dictionary with verse data
        """
        if self.df is None:
            self.load_csv()
        
        result = self.df[
            (self.df['chapter'] == chapter) & 
            (self.df['verse'] == verse)
        ]
        
        if len(result) > 0:
            return result.iloc[0].to_dict()
        return {}
    
    def get_chapter_verses(self, chapter: int) -> List[Dict]:
        """
        Get all verses from a chapter.
        
        Args:
            chapter: Chapter number
            
        Returns:
            List of verse dictionaries
        """
        if self.df is None:
            self.load_csv()
        
        result = self.df[self.df['chapter'] == chapter]
        return result.to_dict('records')
    
    def process_for_embeddings(self) -> List[Dict]:
        """
        Process data for embedding creation.
        
        Returns:
            List of dictionaries with verse data and metadata
        """
        if self.df is None:
            self.load_csv()
        
        processed = []
        
        for _, row in self.df.iterrows():
            # Create combined text for embedding (all languages)
            combined_text = f"""
            Chapter {row['chapter']}, Verse {row['verse']}
            
            Sanskrit: {row.get('sanskrit', '')}
            Hindi: {row.get('hindi', '')}
            English: {row.get('english', '')}
            """
            
            verse_data = {
                'id': f"{row['chapter']}.{row['verse']}",
                'chapter': int(row['chapter']),
                'verse': int(row['verse']),
                'text': combined_text.strip(),
                'sanskrit': row.get('sanskrit', ''),
                'hindi': row.get('hindi', ''),
                'english': row.get('english', ''),
                'metadata': {
                    'chapter': int(row['chapter']),
                    'verse': int(row['verse']),
                    'verse_id': f"{row['chapter']}.{row['verse']}"
                }
            }
            
            processed.append(verse_data)
        
        return processed
    
    def get_total_verses(self) -> int:
        """Get total number of verses."""
        if self.df is None:
            self.load_csv()
        return len(self.df)
    
    def get_chapter_count(self) -> int:
        """Get total number of chapters."""
        if self.df is None:
            self.load_csv()
        return self.df['chapter'].nunique()
