"""Chapter navigator for browsing Bhagavad Gita."""

import streamlit as st
from typing import Dict, List
from src.core.data_processor import DataProcessor


class ChapterNavigator:
    """Navigate through Bhagavad Gita chapters and themes."""
    
    # Chapter information
    CHAPTERS = {
        1: {"name": "Arjuna Vishada Yoga", "icon": "😔", "summary": "Arjuna's Dilemma"},
        2: {"name": "Sankhya Yoga", "icon": "🧘", "summary": "Transcendental Knowledge"},
        3: {"name": "Karma Yoga", "icon": "⚡", "summary": "Path of Action"},
        4: {"name": "Jnana Karma Sanyasa Yoga", "icon": "📚", "summary": "Knowledge and Renunciation"},
        5: {"name": "Karma Sanyasa Yoga", "icon": "🕉️", "summary": "Renunciation of Action"},
        6: {"name": "Dhyana Yoga", "icon": "🧘‍♂️", "summary": "Meditation"},
        7: {"name": "Jnana Vijnana Yoga", "icon": "💡", "summary": "Knowledge and Wisdom"},
        8: {"name": "Aksara Brahma Yoga", "icon": "🌌", "summary": "Imperishable Brahman"},
        9: {"name": "Raja Vidya Yoga", "icon": "👑", "summary": "Royal Knowledge"},
        10: {"name": "Vibhuti Yoga", "icon": "✨", "summary": "Divine Glories"},
        11: {"name": "Vishvarupa Darshana Yoga", "icon": "🌟", "summary": "Universal Form"},
        12: {"name": "Bhakti Yoga", "icon": "❤️", "summary": "Path of Devotion"},
        13: {"name": "Kshetra Kshetrajna Vibhaga Yoga", "icon": "🌱", "summary": "Field and Knower"},
        14: {"name": "Gunatraya Vibhaga Yoga", "icon": "⚖️", "summary": "Three Gunas"},
        15: {"name": "Purushottama Yoga", "icon": "🔱", "summary": "Supreme Person"},
        16: {"name": "Daivasura Sampad Vibhaga Yoga", "icon": "⚔️", "summary": "Divine and Demonic"},
        17: {"name": "Shraddhatraya Vibhaga Yoga", "icon": "🙏", "summary": "Three Types of Faith"},
        18: {"name": "Moksha Sanyasa Yoga", "icon": "🕊️", "summary": "Liberation and Renunciation"}
    }
    
    # Theme categories
    THEMES = {
        "Karma Yoga": {"icon": "⚡", "chapters": [2, 3, 5, 18]},
        "Dharma": {"icon": "⚖️", "chapters": [1, 2, 16]},
        "Bhakti": {"icon": "❤️", "chapters": [7, 9, 12, 18]},
        "Jnana": {"icon": "💡", "chapters": [2, 4, 7, 13, 15]},
        "Detachment": {"icon": "🍃", "chapters": [2, 5, 6, 12]},
        "Self-Realization": {"icon": "🧘", "chapters": [6, 13, 15]},
        "Meditation": {"icon": "🧘‍♂️", "chapters": [6, 8, 12]},
        "Universal Form": {"icon": "🌟", "chapters": [11]}
    }
    
    def __init__(self, data_processor: DataProcessor = None):
        """Initialize chapter navigator."""
        self.data_processor = data_processor
    
    def render_chapter_grid(self):
        """Render chapter grid view."""
        st.subheader("📖 Browse by Chapter")
        
        # Create grid (3 columns)
        cols = st.columns(3)
        
        for i, (chapter_num, info) in enumerate(self.CHAPTERS.items()):
            with cols[i % 3]:
                if st.button(
                    f"{info['icon']} Chapter {chapter_num}\n{info['name']}\n*{info['summary']}*",
                    key=f"chapter_{chapter_num}",
                    use_container_width=True
                ):
                    st.session_state.selected_chapter = chapter_num
                    st.session_state.view_mode = 'chapter_detail'
    
    def render_theme_view(self):
        """Render theme-based view."""
        st.subheader("🎨 Browse by Theme")
        
        # Theme selector
        selected_theme = st.selectbox(
            "Choose a theme:",
            options=list(self.THEMES.keys()),
            format_func=lambda x: f"{self.THEMES[x]['icon']} {x}"
        )
        
        if selected_theme:
            theme_info = self.THEMES[selected_theme]
            st.markdown(f"### {theme_info['icon']} {selected_theme}")
            
            # Show chapters for this theme
            st.markdown("**Relevant Chapters:**")
            for chapter_num in theme_info['chapters']:
                chapter_info = self.CHAPTERS[chapter_num]
                st.markdown(f"- {chapter_info['icon']} Chapter {chapter_num}: {chapter_info['name']}")
    
    def render_verse_browser(self, chapter: int):
        """Render verse browser for a chapter."""
        if not self.data_processor:
            st.warning("Data processor not initialized")
            return
        
        chapter_info = self.CHAPTERS.get(chapter)
        if not chapter_info:
            return
        
        st.markdown(f"## {chapter_info['icon']} Chapter {chapter}: {chapter_info['name']}")
        st.markdown(f"*{chapter_info['summary']}*")
        
        # Get verses for this chapter
        df = self.data_processor.load_csv()
        chapter_verses = df[df['chapter'] == chapter]
        
        if len(chapter_verses) == 0:
            st.info("No verses found for this chapter")
            return
        
        # Verse slider
        verse_num = st.slider(
            "Select Verse:",
            min_value=1,
            max_value=len(chapter_verses),
            value=1,
            key=f"verse_slider_{chapter}"
        )
        
        # Display verse
        verse_data = chapter_verses.iloc[verse_num - 1]
        
        st.markdown("---")
        
        # Sanskrit
        if 'sanskrit' in verse_data:
            st.markdown(f"**Sanskrit:**")
            st.markdown(f"*{verse_data['sanskrit']}*")
        
        # English
        if 'english' in verse_data:
            st.markdown(f"**English:**")
            st.markdown(verse_data['english'])
        
        # Hindi
        if 'hindi' in verse_data:
            st.markdown(f"**Hindi:**")
            st.markdown(verse_data['hindi'])
