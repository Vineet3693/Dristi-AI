@echo off
REM Drishti AI - Quick Start Script for Windows
REM This script activates the virtual environment and runs the app

echo ========================================
echo    Drishti AI - Divine Wisdom
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create a virtual environment first:
    echo    python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if dependencies are installed
echo.
echo Checking dependencies...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo.
    echo Dependencies not installed. Installing now...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file with your Gemini API key.
    echo.
    pause
)

REM Check if CSV exists
if not exist "data\bhagavad_gita.csv" (
    echo.
    echo WARNING: Bhagavad Gita CSV not found!
    echo Please add your CSV file to: data\bhagavad_gita.csv
    echo.
    pause
)

REM Run the app
echo.
echo ========================================
echo    Launching Drishti AI...
echo ========================================
echo.
streamlit run app.py

pause
