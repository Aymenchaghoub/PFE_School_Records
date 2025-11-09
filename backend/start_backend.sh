#!/bin/bash
# Backend start script for Linux/Mac
# Activates virtual environment, runs migrations, starts FastAPI with Gunicorn

set -e

echo "🚀 Starting School Records Management Backend..."
echo ""

# Check if we're in the backend directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    if [ -f ".env.example" ]; then
        cp ".env.example" ".env"
        echo "✅ Created .env file. Please update it with your configuration."
        echo "   Then run this script again."
        exit 0
    else
        echo "❌ Error: .env.example not found. Cannot proceed."
        exit 1
    fi
fi

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  No virtual environment found. Using system Python..."
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
if ! python -c "import fastapi, sqlalchemy, alembic" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run database migrations
echo "🗄️  Running database migrations..."
python -m alembic upgrade head || echo "⚠️  Migration failed or no migrations to apply"

echo ""
echo "============================================================"
echo "✅ Backend is starting..."
echo "============================================================"
echo "📡 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo "🔍 Health: http://localhost:8000/health"
echo "============================================================"
echo ""

# Start the server
# For development: Use uvicorn with auto-reload
# For production: Use gunicorn with uvicorn workers
if [ "$1" = "--production" ]; then
    echo "🚀 Starting in PRODUCTION mode with Gunicorn..."
    gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
else
    echo "🔧 Starting in DEVELOPMENT mode with Uvicorn..."
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi
