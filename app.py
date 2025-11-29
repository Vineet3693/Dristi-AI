"""
Drishti AI - Divine Wisdom from Bhagavad Gita

A sophisticated RAG system providing spiritual guidance through Krishna's teachings.
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.query_handler import QueryHandler
from src.core.inmemory_embedding_manager import InMemoryEmbeddingManager
from src.core.data_processor import DataProcessor
from src.ui.base_components import load_css, render_header
from src.features.feature_registry import FeatureRegistry
from src.features.export_handler import ExportHandler
from src.features.chapter_navigator import ChapterNavigator
from src.features.conversational_memory import ConversationalMemory
from src.features.voice_handler import VoiceHandler
from config.settings import APP_TITLE, APP_ICON, LANGUAGES, RESPONSE_TONES, SEARCH_MODES
import tempfile
from pathlib import Path
import os


# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()



def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'query_handler' not in st.session_state:
        st.session_state.query_handler = QueryHandler()
    
    if 'embedding_manager' not in st.session_state:
        # Use in-memory manager for Streamlit Cloud (read-only filesystem)
        st.session_state.embedding_manager = InMemoryEmbeddingManager()
        st.session_state.embedding_manager.initialize_collection()
    
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = DataProcessor()
    
    if 'feature_registry' not in st.session_state:
        st.session_state.feature_registry = FeatureRegistry()
    
    if 'export_handler' not in st.session_state:
        st.session_state.export_handler = ExportHandler()
    
    if 'chapter_navigator' not in st.session_state:
        st.session_state.chapter_navigator = ChapterNavigator(st.session_state.data_processor)
    
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationalMemory()
    
    if 'voice_handler' not in st.session_state:
        st.session_state.voice_handler = VoiceHandler()
    
    if 'tone' not in st.session_state:
        st.session_state.tone = 'modern'
    
    if 'language' not in st.session_state:
        st.session_state.language = 'english'
    
    if 'search_mode' not in st.session_state:
        st.session_state.search_mode = 'gita'
    
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 'chat'
    
    if 'enable_voice' not in st.session_state:
        st.session_state.enable_voice = False


def render_sidebar():
    """Render sidebar with controls."""
    with st.sidebar:
        st.title(f"{APP_ICON} Drishti AI")
        st.markdown("*Divine Wisdom from Bhagavad Gita*")
        
        st.markdown("---")
        
        # Search mode
        st.subheader("🔍 Search Mode")
        search_mode = st.radio(
            "Choose mode:",
            options=list(SEARCH_MODES.keys()),
            format_func=lambda x: SEARCH_MODES[x],
            key='search_mode_radio'
        )
        st.session_state.search_mode = search_mode
        
        st.markdown("---")
        
        # Response tone
        st.subheader("🎭 Response Tone")
        tone = st.selectbox(
            "Choose Krishna's tone:",
            options=list(RESPONSE_TONES.keys()),
            format_func=lambda x: RESPONSE_TONES[x],
            key='tone_select'
        )
        st.session_state.tone = tone
        
        st.markdown("---")
        
        # Language
        st.subheader("🗣️ Response Language")
        language = st.selectbox(
            "Choose language:",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            key='language_select'
        )
        st.session_state.language = language
        
        st.markdown("---")
        
        # Stats
        stats = st.session_state.embedding_manager.get_stats()
        st.subheader("📊 Statistics")
        st.metric("Total Verses", stats['total_verses'])
        st.metric("Questions Asked", len(st.session_state.messages) // 2)
        
        st.markdown("---")
        
        # Voice toggle
        if st.session_state.feature_registry.is_enabled('voice'):
            st.markdown("---")
            st.subheader("🎤 Voice")
            st.session_state.enable_voice = st.checkbox(
                "Enable Voice Output",
                value=st.session_state.enable_voice
            )
        
        # Journey stats
        if st.session_state.feature_registry.is_enabled('conversational_memory'):
            st.markdown("---")
            st.subheader("🌟 Your Journey")
            journey = st.session_state.memory.get_journey_summary()
            st.metric("Conversations", journey['total_conversations'])
            st.metric("Themes Explored", journey['themes_explored'])
            st.metric("Favorites", journey['favorite_verses'])
        
        # About
        with st.expander("ℹ️ About Drishti AI"):
            st.markdown("""
            **Creator**: Vineet Yadav
            
            **Vision**: To master life on the principles of Krishna, the Kalki (The Soul Protectors)
            
            **Contact**:
            - Telegram: @Vine3699
            - Email: Vineet.ggu@gmail.com
            
            ---
            
            सत्यमेव जयते  
            ॐ नमो भगवते वासुदेवाय
            """)


def render_chat():
    """Render chat interface."""
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Voice output for assistant messages
            if (message["role"] == "assistant" and 
                st.session_state.enable_voice and 
                st.session_state.feature_registry.is_enabled('voice')):
                st.session_state.voice_handler.render_audio_player(
                    message["content"],
                    st.session_state.language
                )
    
    # Chat input
    if prompt := st.chat_input("🎤 Ask Krishna for divine wisdom..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🕉️ Krishna is contemplating..."):
                response = st.session_state.query_handler.process_query(
                    query=prompt,
                    tone=st.session_state.tone,
                    language=st.session_state.language,
                    search_mode=st.session_state.search_mode
                )
                st.markdown(response)
                
                # Voice output
                if (st.session_state.enable_voice and 
                    st.session_state.feature_registry.is_enabled('voice')):
                    st.session_state.voice_handler.render_audio_player(
                        response,
                        st.session_state.language
                    )
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save to memory
        if st.session_state.feature_registry.is_enabled('conversational_memory'):
            st.session_state.memory.add_conversation(prompt, response)
    
    # Export button
    if st.session_state.messages and st.session_state.feature_registry.is_enabled('export'):
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export to PDF", use_container_width=True):
                # Combine all messages
                content = "\n\n".join([
                    f"**{m['role'].title()}:** {m['content']}" 
                    for m in st.session_state.messages
                ])
                
                # Export
                temp_file = Path(tempfile.gettempdir()) / "drishti_conversation.pdf"
                st.session_state.export_handler.export_to_pdf(content, str(temp_file))
                
                with open(temp_file, 'rb') as f:
                    st.download_button(
                        "⬇️ Download PDF",
                        f.read(),
                        file_name="drishti_conversation.pdf",
                        mime="application/pdf"
                    )
        
        with col2:
            if st.button("📝 Export to DOCX", use_container_width=True):
                # Combine all messages
                content = "\n\n".join([
                    f"**{m['role'].title()}:** {m['content']}" 
                    for m in st.session_state.messages
                ])
                
                # Export
                temp_file = Path(tempfile.gettempdir()) / "drishti_conversation.docx"
                st.session_state.export_handler.export_to_docx(content, str(temp_file))
                
                with open(temp_file, 'rb') as f:
                    st.download_button(
                        "⬇️ Download DOCX",
                        f.read(),
                        file_name="drishti_conversation.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )


def main():
    """Main application."""
    # Initialize
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main content - use custom header
    render_header()
    
    # Check if embeddings exist
    stats = st.session_state.embedding_manager.get_stats()
    if stats['total_verses'] == 0:
        st.info("🕉️ **First-time setup detected**")
        st.write("Drishti AI needs to create embeddings from the Bhagavad Gita.")
        st.write("This is a one-time process that will take 5-10 minutes.")
        
        if st.button("🚀 Create Embeddings Now", type="primary", use_container_width=True):
            with st.spinner("Creating embeddings from 640 verses... Please wait..."):
                try:
                    # Try to re-initialize first (in case chromadb files exist)
                    st.session_state.embedding_manager.initialize_collection()
                    stats_check = st.session_state.embedding_manager.get_stats()
                    
                    if stats_check['total_verses'] > 0:
                        st.success(f"✅ Successfully loaded {stats_check['total_verses']} verses from storage!")
                        st.balloons()
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        # Chromadb storage not found, create embeddings from CSV
                        st.info("📊 ChromaDB storage not found. Creating embeddings from CSV...")
                        
                        # Create embeddings
                        st.session_state.embedding_manager.create_embeddings(force_recreate=False)
                        
                        # Verify
                        stats_new = st.session_state.embedding_manager.get_stats()
                        if stats_new['total_verses'] > 0:
                            st.success(f"✅ Successfully created embeddings for {stats_new['total_verses']} verses!")
                            st.balloons()
                            import time
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Failed to create embeddings.")
                            st.info("💡 **Troubleshooting:**")
                            st.write("1. Ensure GOOGLE_API_KEY is set in Streamlit secrets")
                            st.write("2. Check that data/bhagavad_gita.csv exists")
                            st.write("3. Verify you have internet connection")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 **Troubleshooting:**")
                    st.write("1. Ensure GOOGLE_API_KEY is set in Streamlit secrets")
                    st.write("2. Check that data/bhagavad_gita.csv exists in the repository")
                    st.write("3. Verify the app has read access to files")
                    import traceback
                    with st.expander("🔍 Technical Details"):
                        st.code(traceback.format_exc())
        
        st.warning("""
        **Note:** This will use the Gemini API to create embeddings.  
        Make sure your GOOGLE_API_KEY is set in Streamlit Cloud secrets.
        """)
        return
    
    # Tabs for different features
    tabs = ["💬 Chat"]
    
    if st.session_state.feature_registry.is_enabled('chapter_navigator'):
        tabs.append("📖 Chapters")
    
    if st.session_state.feature_registry.is_enabled('conversational_memory'):
        tabs.append("🌟 Journey")
    
    tab_objects = st.tabs(tabs)
    
    # Chat tab
    with tab_objects[0]:
        render_chat()
    
    # Chapter navigator tab
    if st.session_state.feature_registry.is_enabled('chapter_navigator') and len(tab_objects) > 1:
        with tab_objects[1]:
            st.subheader("📖 Explore Bhagavad Gita")
            
            view_mode = st.radio(
                "Browse by:",
                ["Chapters", "Themes"],
                horizontal=True
            )
            
            if view_mode == "Chapters":
                st.session_state.chapter_navigator.render_chapter_grid()
                
                # Show chapter detail if selected
                if 'selected_chapter' in st.session_state:
                    st.session_state.chapter_navigator.render_verse_browser(
                        st.session_state.selected_chapter
                    )
            else:
                st.session_state.chapter_navigator.render_theme_view()
    
    # Journey tab
    if st.session_state.feature_registry.is_enabled('conversational_memory') and len(tab_objects) > 2:
        with tab_objects[-1]:
            st.subheader("🌟 Your Spiritual Journey")
            
            journey = st.session_state.memory.get_journey_summary()
            
            # Stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Conversations", journey['total_conversations'])
            with col2:
                st.metric("Themes Explored", journey['themes_explored'])
            with col3:
                st.metric("Favorite Verses", journey['favorite_verses'])
            
            # Recent conversations
            st.markdown("### Recent Conversations")
            recent = st.session_state.memory.get_recent_conversations(5)
            for conv in reversed(recent):
                with st.expander(f"Q: {conv['query'][:50]}..."):
                    st.markdown(f"**Query:** {conv['query']}")
                    st.markdown(f"**Response:** {conv['response'][:200]}...")
                    st.caption(f"Time: {conv['timestamp']}")
            
            # Favorite verses
            favorites = st.session_state.memory.get_favorite_verses()
            if favorites:
                st.markdown("### ⭐ Favorite Verses")
                for fav in favorites:
                    st.markdown(f"**{fav['chapter']}.{fav['verse']}** - {fav['text'][:100]}...")


if __name__ == "__main__":
    main()
