#!/bin/bash
# macOS/Linux Shell Script to set up and run the Recruitment AI System

set -e

echo ""
echo "============================================"
echo "Recruitment AI System - Setup & Run"
echo "============================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env file and add your OpenAI API Key"
    echo ""
fi

# Ask user what to run
echo ""
echo "Choose what to run:"
echo "1. Backend only (FastAPI on port 8000)"
echo "2. Frontend only (Streamlit on port 8501)"
echo "3. Both (Backend and Frontend)"
echo ""

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting FastAPI Backend..."
        echo "Backend will be available at: http://localhost:8000"
        echo "API Docs at: http://localhost:8000/docs"
        echo ""
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ;;
    2)
        echo ""
        echo "Starting Streamlit Frontend..."
        echo "Frontend will be available at: http://localhost:8501"
        
        # Get the machine's IP address
        IP_ADDRESS=$(hostname -I | awk '{print $1}')
        if [ ! -z "$IP_ADDRESS" ]; then
            echo "External IP: http://$IP_ADDRESS:8501"
        fi
        echo ""
        
        streamlit run frontend/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
        ;;
    3)
        echo ""
        echo "Starting both Backend and Frontend..."
        echo ""
        echo "Backend will be at: http://localhost:8000"
        echo "Frontend will be at: http://localhost:8501"
        echo ""
        
        # Start backend in background
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
        BACKEND_PID=$!
        
        sleep 3
        
        # Start frontend
        streamlit run frontend/streamlit_app.py
        
        # Kill backend when frontend exits
        kill $BACKEND_PID 2>/dev/null || true
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
