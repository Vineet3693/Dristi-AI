#!/bin/bash
# Drishti AI - Quick Start Script for Linux/Mac

echo "========================================"
echo "   Drishti AI - Divine Wisdom"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please create a virtual environment first:"
    echo "   python -m venv .venv"
    echo ""
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
echo ""
echo "Checking dependencies..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "Dependencies not installed. Installing now..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install dependencies!"
        exit 1
    fi
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please create .env file with your Gemini API key."
    echo ""
fi

# Check if CSV exists
if [ ! -f "data/bhagavad_gita.csv" ]; then
    echo ""
    echo "WARNING: Bhagavad Gita CSV not found!"
    echo "Please add your CSV file to: data/bhagavad_gita.csv"
    echo ""
fi

# Run the app
echo ""
echo "========================================"
echo "   Launching Drishti AI..."
echo "========================================"
echo ""
streamlit run app.py
