"""Base UI components for Drishti AI."""

import streamlit as st
from pathlib import Path


def load_css():
    """Load custom CSS styles."""
    css_file = Path(__file__).parent.parent.parent / "assets" / "styles.css"
    
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_header():
    """Render the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>🕉️ Drishti AI</h1>
        <h3>Divine Wisdom from the Bhagavad Gita</h3>
    </div>
    """, unsafe_allow_html=True)


def render_background_selector():
    """Render background image selector."""
    backgrounds = {
        "Cosmic Krishna": "cosmic_krishna.jpg",
        "Divine Chariot": "divine_chariot.jpg",
        "Sacred Lotus": "sacred_lotus.jpg",
        "Celestial Glow": "celestial_glow.jpg",
        "Spiritual Aura": "spiritual_aura.jpg",
        "Golden Temple": "golden_temple.jpg"
    }
    
    with st.sidebar:
        st.subheader("🎨 Background Theme")
        selected_bg = st.selectbox(
            "Choose background:",
            options=list(backgrounds.keys()),
            key='background_selector'
        )
        
        if selected_bg:
            bg_path = backgrounds[selected_bg]
            st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url('assets/backgrounds/{bg_path}');
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }}
            </style>
            """, unsafe_allow_html=True)


def render_flame_effect():
    """Render golden flame animation."""
    st.markdown("""
    <div class="flame-container">
        <div class="flame"></div>
    </div>
    """, unsafe_allow_html=True)


def render_loading_spinner(message: str = "🕉️ Krishna is contemplating..."):
    """Render custom loading spinner."""
    return st.spinner(message)


def render_verse_citation(chapter: int, verse: int, text: str):
    """
    Render a verse citation with expandable full text.
    
    Args:
        chapter: Chapter number
        verse: Verse number
        text: Verse text
    """
    with st.expander(f"📖 Bhagavad Gita {chapter}.{verse}"):
        st.markdown(f"**Sanskrit/Translation:**\n\n{text}")


def render_stats_card(title: str, value: str, icon: str = "📊"):
    """
    Render a stats card.
    
    Args:
        title: Card title
        value: Card value
        icon: Icon emoji
    """
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-icon">{icon}</div>
        <div class="stats-content">
            <div class="stats-title">{title}</div>
            <div class="stats-value">{value}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
