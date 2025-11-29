"""Voice input and output using Web Speech API."""

import streamlit as st
from gtts import gTTS
import tempfile
from pathlib import Path


class VoiceHandler:
    """Handle voice input and output."""
    
    def __init__(self):
        """Initialize voice handler."""
        self.temp_dir = Path(tempfile.gettempdir()) / "drishti_audio"
        self.temp_dir.mkdir(exist_ok=True)
    
    def render_voice_input(self) -> str:
        """Render voice input component."""
        st.markdown("### 🎤 Voice Input")
        
        # Note: Web Speech API requires JavaScript
        # For now, we'll use a placeholder
        st.info("Voice input coming soon! Use the text input for now.")
        
        return ""
    
    def text_to_speech(self, text: str, language: str = 'en') -> str:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert
            language: Language code (en, hi, sa)
            
        Returns:
            Path to audio file
        """
        # Map language codes
        lang_map = {
            'english': 'en',
            'hindi': 'hi',
            'sanskrit': 'hi'  # Use Hindi for Sanskrit
        }
        
        lang_code = lang_map.get(language, 'en')
        
        # Generate speech
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Save to temp file
        audio_file = self.temp_dir / f"response_{hash(text)}.mp3"
        tts.save(str(audio_file))
        
        return str(audio_file)
    
    def render_audio_player(self, text: str, language: str = 'en'):
        """Render audio player for text."""
        try:
            audio_file = self.text_to_speech(text, language)
            
            with open(audio_file, 'rb') as f:
                audio_bytes = f.read()
            
            st.audio(audio_bytes, format='audio/mp3')
        
        except Exception as e:
            st.error(f"Audio generation failed: {e}")
