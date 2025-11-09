# ✅ Final Setup Checklist

## Pre-Installation

- [ ] Python 3.13 installed and verified
- [ ] MySQL server running (local) OR PlanetScale account ready
- [ ] Virtual environment created (optional but recommended)

## Installation Steps

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Verify**: Run `python test_setup.py`
- Should show all ✅ checkmarks
- Pydantic version should be 1.10.13 (not 2.x)

### 2. Create .env File
```bash
# Copy example
# Create .env in backend/ directory with:
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/school_records
SECRET_KEY=your-secret-key-min-32-chars
```

### 3. Create Database
```bash
mysql -u root -p
CREATE DATABASE school_records;
```

### 4. Seed Database
```bash
python -m app.seed_data
```

**Expected output:**
```
✅ Database connected
✅ Database tables created/verified
✅ Admin user created: admin@school.com / admin123
✅ Teacher user created: teacher@school.com / teacher123
✅ Class created: Class 10A
✅ Created 4 subjects
✅ Student user created: student@school.com / student123
🎉 Seed data created successfully!
```

### 5. Start Server
```bash
uvicorn app.main:app --reload
```

**Expected output:**
```
✅ Database connected
✅ Database tables created/verified
INFO:     Uvicorn running on http://127.0.0.1:8000
🚀 School Records Management System API
📡 API Documentation: http://localhost:8000/docs
```

## Verification Tests

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```
**Expected:** `{"status": "healthy", "database": "connected"}`

### Test 2: API Docs
Open: http://localhost:8000/docs
**Expected:** FastAPI Swagger UI loads

### Test 3: Login Endpoint
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@school.com","password":"admin123"}'
```
**Expected:** JSON with access_token, refresh_token, and user object

### Test 4: Protected Endpoint
```bash
# Get token from login response, then:
curl http://localhost:8000/api/users \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
**Expected:** List of users

## Common Issues & Solutions

### Issue: "No module named 'app'"
**Solution:** Run from `backend/` directory, not root

### Issue: "Database connection failed"
**Solution:** 
- Check MySQL is running
- Verify DATABASE_URL in .env
- Ensure database exists

### Issue: "Pydantic 2.x installed"
**Solution:**
```bash
pip uninstall pydantic pydantic-core -y
pip install pydantic==1.10.13
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
uvicorn app.main:app --reload --port 8001
```

## Production Deployment (Render)

### Checklist:
- [ ] Procfile exists: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Root Directory set to: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Environment variables configured:
  - [ ] DATABASE_URL
  - [ ] SECRET_KEY
  - [ ] JWT_EXPIRE_MINUTES
  - [ ] JWT_REFRESH_EXPIRE_DAYS
- [ ] CORS_ORIGINS set (comma-separated)

## Success Criteria

✅ All dependencies install without Rust  
✅ Server starts without errors  
✅ Database connects successfully  
✅ Tables created automatically  
✅ Seed data script runs successfully  
✅ `/health` returns healthy status  
✅ `/docs` loads correctly  
✅ `/api/auth/login` works with demo credentials  
✅ Protected endpoints work with JWT token  

## Files Status

- ✅ `requirements.txt` - Python 3.13 compatible
- ✅ `app/main.py` - FastAPI app with startup logging
- ✅ `app/core/database.py` - SQLAlchemy 2.0 compatible
- ✅ `app/core/config.py` - Pydantic v1 BaseSettings
- ✅ `app/seed_data.py` - Demo data seeding
- ✅ `Procfile` - Render deployment ready
- ✅ All schemas use `orm_mode = True`
- ✅ All routers use `from_orm()` instead of `model_validate()`

---

**Status**: ✅ Ready for Python 3.13 on Windows (no Rust required)

