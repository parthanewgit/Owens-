# Quick Start guide
# Windows PowerShell Script to start development

param(
    [string]$Component = "both"
)

function Setup-Environment {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "Recruitment AI System - Setup" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Create virtual environment if not exists
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        python -m venv .venv
    }
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
    
    # Install dependencies
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt | Out-Null
    
    # Create .env if not exists
    if (-not (Test-Path ".env")) {
        Write-Host "Creating .env file from template..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "IMPORTANT: Edit .env file and add your OpenAI API Key" -ForegroundColor Red
    }
}

function Start-Backend {
    Write-Host ""
    Write-Host "Starting FastAPI Backend..." -ForegroundColor Green
    Write-Host "Backend available at: http://localhost:8000" -ForegroundColor Green
    Write-Host "API Docs at: http://localhost:8000/docs" -ForegroundColor Green
    Write-Host ""
    
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

function Start-Frontend {
    Write-Host ""
    Write-Host "Starting Streamlit Frontend..." -ForegroundColor Green
    Write-Host "Frontend available at: http://localhost:8501" -ForegroundColor Green
    
    # Get current machine IP
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp" -or $_.PrefixOrigin -eq "Manual"} | Select-Object -First 1).IPAddress
    if ($ipAddress) {
        Write-Host "External IP: http://$($ipAddress):8501" -ForegroundColor Green
    }
    Write-Host ""
    
    streamlit run frontend/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
}

function Main {
    Setup-Environment
    
    if ($Component -eq "backend") {
        Start-Backend
    } elseif ($Component -eq "frontend") {
        Start-Frontend
    } else {
        # Start both
        Write-Host ""
        Write-Host "Starting Backend..." -ForegroundColor Green
        
        $backendProcess = Start-Process -PassThru -NoNewWindow `
            -FileName "python" `
            -ArgumentList "-m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
        
        Start-Sleep -Seconds 3
        
        Write-Host "Starting Frontend..." -ForegroundColor Green
        Start-Frontend
        
        # Cleanup
        $backendProcess | Stop-Process -Force
    }
}

if ($MyInvocation.InvocationName -eq ".") {
    Main
}
