# 🚀 Backend Setup Guide - Python 3.13 Compatible

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Note**: All dependencies are prebuilt wheels - no Rust compilation needed!

### 2. Configure Environment

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/school_records
SECRET_KEY=your-secret-key-change-in-production-min-32-characters
JWT_EXPIRE_MINUTES=60
JWT_REFRESH_EXPIRE_DAYS=7
```

### 3. Start Database (MySQL)

**Local MySQL:**
```bash
# Create database
mysql -u root -p
CREATE DATABASE school_records;
```

**Or use PlanetScale connection string in .env**

### 4. Initialize Database

```bash
# This will create all tables
python -m app.seed_data
```

This creates:
- Admin: `admin@school.com` / `admin123`
- Teacher: `teacher@school.com` / `teacher123`
- Student: `student@school.com` / `student123`

### 5. Run Server

```bash
uvicorn app.main:app --reload
```

You should see:
```
✅ Database connected
✅ Database tables created/verified
🚀 School Records Management System API
📡 API Documentation: http://localhost:8000/docs
```

## Testing

### 1. Health Check
```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status": "healthy", "database": "connected"}
```

### 2. API Documentation
Open: http://localhost:8000/docs

### 3. Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@school.com","password":"admin123"}'
```

Expected:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Administrator",
    "email": "admin@school.com",
    "role": "admin"
  }
}
```

## Troubleshooting

### Database Connection Error
- Verify MySQL is running: `mysql -u root -p`
- Check DATABASE_URL in `.env`
- Ensure database exists: `CREATE DATABASE school_records;`

### Import Errors
- Make sure you're in the `backend/` directory
- Activate virtual environment: `venv\Scripts\activate` (Windows)

### Port Already in Use
- Change port: `uvicorn app.main:app --reload --port 8001`
- Or kill process: `netstat -ano | findstr :8000`

## Production Deployment (Render)

1. Set Root Directory: `backend`
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `JWT_EXPIRE_MINUTES`
   - `JWT_REFRESH_EXPIRE_DAYS`

## Dependencies

All dependencies are Python 3.13 compatible:
- ✅ FastAPI 0.100.1
- ✅ Pydantic 1.10.13 (pure Python, no Rust)
- ✅ SQLAlchemy 2.0.23
- ✅ Uvicorn 0.24.0
- ✅ All others have prebuilt wheels

No Rust compilation needed!

