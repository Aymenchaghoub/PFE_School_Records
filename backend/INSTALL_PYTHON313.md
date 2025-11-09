# Quick Installation Guide for Python 3.13

## ✅ All Changes Complete

The backend has been fully updated to work with Python 3.13 on Windows **without requiring Rust**.

## Quick Start

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment (if not already done)
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies (no Rust needed!)
pip install -r requirements.txt

# 5. Verify Pydantic version
python -c "import pydantic; print('Pydantic version:', pydantic.__version__)"
# Should show: Pydantic version: 1.10.13

# 6. Run the server
uvicorn app.main:app --reload
```

## What Was Changed

### 1. Dependencies (requirements.txt)
- ✅ Pydantic: `2.5.0` → `1.10.13` (pure Python, no Rust)
- ✅ FastAPI: `0.104.1` → `0.100.1` (Pydantic v1 compatible)
- ✅ Removed: `pydantic-settings==2.1.0`
- ✅ Added: `pydantic[dotenv]==1.10.13`

### 2. Code Updates
- ✅ All schemas: `from_attributes = True` → `orm_mode = True`
- ✅ Auth router: `model_validate()` → `from_orm()`
- ✅ Config: `pydantic_settings.BaseSettings` → `pydantic.BaseSettings`

## Verification

After installation, test:

```bash
# Test 1: Check imports
python -c "from app.main import app; print('✅ App imports successfully')"

# Test 2: Start server
uvicorn app.main:app --reload

# Test 3: Open browser
# Navigate to: http://localhost:8000/docs
# Should see FastAPI Swagger UI

# Test 4: Test health endpoint
# In another terminal:
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

## Expected Output

When you run `uvicorn app.main:app --reload`, you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then open `http://localhost:8000/docs` to see the API documentation.

## Troubleshooting

### "No module named 'pydantic_settings'"
✅ **This is expected!** We're using `pydantic.BaseSettings` now, not `pydantic_settings`.

### "from_attributes is not a valid Config option"
✅ **Fixed!** All schemas now use `orm_mode = True` instead.

### "model_validate() is not a method"
✅ **Fixed!** All code now uses `from_orm()` instead.

### Installation takes a long time / asks for Rust
❌ **This should NOT happen.** If it does:
1. Make sure you're using `requirements.txt` with Pydantic v1
2. Check: `pip list | findstr pydantic` should show `1.10.13`
3. If you see `2.x`, uninstall and reinstall: `pip uninstall pydantic pydantic-core -y && pip install -r requirements.txt`

## Success Criteria

✅ All dependencies install without Rust  
✅ Server starts without errors  
✅ `/docs` endpoint loads  
✅ `/health` endpoint returns `{"status":"healthy"}`  
✅ `/api/auth/login` endpoint is visible in docs  

## Files Modified

- `requirements.txt` - Updated dependencies
- `app/core/config.py` - Changed BaseSettings import
- `app/schemas/*.py` - Changed to `orm_mode = True`
- `app/routers/auth.py` - Changed to `from_orm()`

## Next Steps

Once verified working:
1. Create `.env` file with your database URL
2. Run `python -m app.seed_data` to create demo users
3. Test login endpoint with demo credentials

---

**Status**: ✅ Ready for Python 3.13 on Windows (no Rust required)

