"""Base UI components for Drishti AI."""

import streamlit as st
from pathlib import Path
import base64


def load_css():
    """Load custom CSS styles with background image."""
    css_file = Path(__file__).parent.parent.parent / "assets" / "styles.css"
    bg_image = Path(__file__).parent.parent.parent / "assets" / "backgrounds" / "drishti_ai_bg_4_1764420887041.png"
    
    # Load main CSS
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Add background image
    if bg_image.exists():
        with open(bg_image, "rb") as img_file:
            bg_base64 = base64.b64encode(img_file.read()).decode()
        
        bg_style = f"""
        <style>
        .stApp {{
            background: linear-gradient(
                135deg,
                rgba(13, 27, 42, 0.85) 0%,
                rgba(27, 38, 59, 0.82) 50%,
                rgba(65, 90, 119, 0.80) 100%
            ),
            url('data:image/png;base64,{bg_base64}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
        }}
        </style>
        """
        st.markdown(bg_style, unsafe_allow_html=True)


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
