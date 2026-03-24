@echo off
REM Windows Batch Script to set up and run the Recruitment AI System

setlocal enabledelayedexpansion

echo.
echo ============================================
echo Recruitment AI System - Setup & Run
echo ============================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Check for .env file
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env file and add your OpenAI API Key
    echo.
    pause
)

REM Ask user what to run
echo.
echo Choose what to run:
echo 1. Backend only (FastAPI on port 8000)
echo 2. Frontend only (Streamlit on port 8501)
echo 3. Both (Backend and Frontend)
echo.

set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting FastAPI Backend...
    echo Backend will be available at: http://localhost:8000
    echo API Docs at: http://localhost:8000/docs
    echo.
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
) else if "%choice%"=="2" (
    echo.
    echo Starting Streamlit Frontend...
    echo Frontend will be available at: http://localhost:8501
    echo.
    streamlit run frontend/streamlit_app.py
) else if "%choice%"=="3" (
    echo.
    echo Starting both Backend and Frontend...
    echo.
    echo Backend will be at: http://localhost:8000
    echo Frontend will be at: http://localhost:8501
    echo.
    
    start "Recruitment AI - Backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    timeout /t 3 /nobreak
    start "Recruitment AI - Frontend" cmd /k "streamlit run frontend/streamlit_app.py"
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b 1
)

pause
