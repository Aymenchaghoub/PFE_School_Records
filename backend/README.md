# Backend API Documentation

## Project Structure

```
backend/
├── app/                    # Main application package
│   ├── core/              # Core modules (config, database, security)
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API endpoints
│   ├── schemas/           # Pydantic schemas
│   ├── main.py            # FastAPI application entry point
│   └── seed_data.py       # Database seeding script
├── requirements.txt       # Python dependencies
└── pyproject.toml         # Code quality tools config
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create `.env` file):
```env
DATABASE_URL=mysql+pymysql://root@localhost/pfc
SECRET_KEY=your-secret-key-change-in-production
JWT_EXPIRE_MINUTES=60
JWT_REFRESH_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:5173
```

3. Run the server:
```bash
# Development (with auto-reload)
uvicorn app.main:app --reload

# Production
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

4. (Optional) Seed initial data:
```bash
python -m app.seed_data
```

## API Endpoints

See main README.md for complete API documentation.

## Testing

```bash
pytest
```

