# Drishti AI - Divine Wisdom from Bhagavad Gita

A sophisticated RAG (Retrieval Augmented Generation) system providing spiritual guidance through Krishna's teachings from the Bhagavad Gita.

## 🕉️ Features

- **Semantic Search**: Understands meaning, not just keywords
- **Dual Search Modes**: Bhagavad Gita mode (RAG) or Universal mode (direct LLM)
- **Multi-Language Support**: Hindi, English, Sanskrit
- **Response Tone Selection**: Spiritual, Scholarly, Modern, or Devotional
- **Citation Transparency**: Every verse cited with source
- **Ethical Guardrails**: Prevents misuse and harmful interpretations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Add Your Data

Place your Bhagavad Gita CSV file at:

```
data/bhagavad_gita.csv
```

Expected CSV format:
```csv
chapter,verse,sanskrit,hindi,english
1,1,"धृतराष्ट्र उवाच...","धृतराष्ट्र बोले...","Dhritarashtra said..."
```

### 4. Create Embeddings (One-Time Setup)

```bash
python -c "from src.core.embedding_manager import EmbeddingManager; em = EmbeddingManager(); em.create_embeddings()"
```

This will process all verses and create persistent embeddings in ChromaDB.

### 5. Run the Application

```bash
streamlit run app.py
```

## 📖 Usage

1. **Choose Search Mode**: Bhagavad Gita (RAG) or Universal (direct LLM)
2. **Select Response Tone**: How Krishna should respond
3. **Pick Language**: Hindi, English, or Sanskrit
4. **Ask Questions**: Type your spiritual questions
5. **Receive Wisdom**: Get responses with verse citations

## 🏗️ Project Structure

```
drishti-ai/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Dependencies
├── config/
│   ├── settings.py          # Configuration
│   ├── prompts.py           # Prompt templates
│   └── features.yaml        # Feature flags
├── src/
│   └── core/
│       ├── data_processor.py      # CSV processing
│       ├── embedding_manager.py   # ChromaDB operations
│       ├── gemini_client.py       # Gemini API
│       ├── context_engineer.py    # Context engineering
│       └── query_handler.py       # RAG pipeline
├── data/
│   └── bhagavad_gita.csv   # Your data file
└── chromadb_storage/        # Persistent embeddings
```

## 🔑 Getting API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 💡 Tips

- **First Time**: Creating embeddings takes 5-10 minutes for 700 verses
- **Embeddings**: Created once, stored persistently in `chromadb_storage/`
- **CSV Format**: Ensure your CSV has columns: chapter, verse, sanskrit, hindi, english
- **API Limits**: Free tier has generous limits for personal use

## 🙏 About

**Creator**: Vineet Yadav  
**Vision**: To master life on the principles of Krishna, the Kalki (The Soul Protectors)  
**Contact**: 
- Telegram: @Vine3699
- Email: Vineet.ggu@gmail.com

---

सत्यमेव जयते  
ॐ नमो भगवते वासुदेवाय
