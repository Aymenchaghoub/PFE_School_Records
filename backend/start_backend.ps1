#!/usr/bin/env pwsh
# Backend start script for Windows (PowerShell)
# Activates virtual environment, runs migrations, starts FastAPI with Gunicorn

Write-Host "🚀 Starting School Records Management Backend..." -ForegroundColor Green
Write-Host ""

# Check if we're in the backend directory
if (!(Test-Path "app\main.py")) {
    Write-Host "❌ Error: Please run this script from the backend directory" -ForegroundColor Red
    exit 1
}

# Check for .env file
if (!(Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found. Copying from .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env file. Please update it with your configuration." -ForegroundColor Green
        Write-Host "   Then run this script again." -ForegroundColor Yellow
        exit 0
    } else {
        Write-Host "❌ Error: .env.example not found. Cannot proceed." -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Cyan
    & ".\venv\Scripts\Activate.ps1"
} elseif (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Cyan
    & ".\.venv\Scripts\Activate.ps1"
} else {
    Write-Host "⚠️  No virtual environment found. Using system Python..." -ForegroundColor Yellow
}

# Check if dependencies are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Cyan
python -c "import fastapi, sqlalchemy, alembic" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Run database migrations
Write-Host "🗄️  Running database migrations..." -ForegroundColor Cyan
python -m alembic upgrade head
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Migration failed or no migrations to apply" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "✅ Backend is starting..." -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "📡 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🔍 Health: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Green
Write-Host ""

# Start the server
# For development: Use uvicorn with auto-reload
# For production: Use gunicorn with uvicorn workers
param(
    [switch]$Production
)

if ($Production) {
    Write-Host "🚀 Starting in PRODUCTION mode with Gunicorn..." -ForegroundColor Magenta
    gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
} else {
    Write-Host "🔧 Starting in DEVELOPMENT mode with Uvicorn..." -ForegroundColor Cyan
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}
