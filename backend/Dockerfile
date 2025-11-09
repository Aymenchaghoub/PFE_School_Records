# Backend Dockerfile for FastAPI + Python 3.13
# Optimized for Render deployment with fast cold starts

FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies (for PyMySQL, cryptography, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (Render will use $PORT env var)
EXPOSE 8000

# Healthcheck - queries the /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run Alembic migrations and start Uvicorn
# Use shell to handle environment variables properly
CMD sh -c "alembic upgrade head || echo '⚠️ Migration skipped' && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
