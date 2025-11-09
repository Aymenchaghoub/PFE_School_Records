# Python 3.13 Compatibility Guide

## Changes Made for Python 3.13 Compatibility

### Problem
Python 3.13 doesn't have prebuilt wheels for `pydantic-core` (used by Pydantic v2), which requires Rust compilation. This is not available on Windows without manual Rust installation.

### Solution
Downgraded to **Pydantic v1.10.13**, which uses pure Python (no Rust dependency).

## Updated Dependencies

### requirements.txt
- **Pydantic**: `2.5.0` → `1.10.13` (pure Python, no Rust)
- **FastAPI**: `0.104.1` → `0.100.1` (compatible with Pydantic v1)
- **pydantic-settings**: Removed (use `pydantic[dotenv]` instead)
- Added: `pydantic[dotenv]==1.10.13` for environment variable support

All other dependencies remain the same and are compatible with Python 3.13.

## Code Changes

### 1. Config (app/core/config.py)
- Changed: `from pydantic_settings import BaseSettings` → `from pydantic import BaseSettings`
- Changed: `list[str]` → `List[str]` (for Python 3.9+ compatibility, though 3.13 supports both)

### 2. All Schemas (app/schemas/*.py)
- Changed: `from_attributes = True` → `orm_mode = True` (Pydantic v1 syntax)
- This affects:
  - `user.py`
  - `class_model.py`
  - `subject.py`
  - `grade.py`
  - `absence.py`
  - `event.py`

### 3. Routers (app/routers/auth.py)
- Changed: `UserResponse.model_validate(user)` → `UserResponse.from_orm(user)` (Pydantic v1 syntax)

## Installation Instructions

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -c "import pydantic; print(pydantic.__version__)"
   # Should output: 1.10.13
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Test endpoints:**
   - Open: `http://localhost:8000/docs`
   - Test: `POST /api/auth/login` with demo credentials

## Verification Checklist

- [x] No Rust dependencies in requirements.txt
- [x] All schemas use `orm_mode = True`
- [x] All `model_validate()` calls replaced with `from_orm()`
- [x] Config uses `pydantic.BaseSettings`
- [x] FastAPI version compatible with Pydantic v1

## Differences: Pydantic v1 vs v2

| Feature | Pydantic v1 | Pydantic v2 |
|---------|-------------|-------------|
| ORM mode | `orm_mode = True` | `from_attributes = True` |
| Parse from ORM | `from_orm(obj)` | `model_validate(obj)` |
| Settings | `pydantic.BaseSettings` | `pydantic_settings.BaseSettings` |
| Performance | Slower (pure Python) | Faster (Rust core) |
| Python 3.13 | ✅ Works | ❌ Needs Rust |

## Testing

After installation, test that everything works:

```bash
# Test 1: Import works
python -c "from app.main import app; print('✅ App imports successfully')"

# Test 2: Server starts
uvicorn app.main:app --reload --port 8000

# Test 3: API responds
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

## Notes

- **Performance**: Pydantic v1 is slower than v2, but still fast enough for this application
- **Future**: Once Pydantic v2 releases Python 3.13 wheels, you can upgrade back
- **Compatibility**: All existing functionality remains the same
- **No breaking changes**: API endpoints and behavior unchanged

## Troubleshooting

### Issue: Import errors
**Solution**: Make sure you're in the `backend` directory and virtual environment is activated.

### Issue: "No module named 'pydantic_settings'"
**Solution**: This is expected - we're using `pydantic.BaseSettings` now, not `pydantic_settings`.

### Issue: "from_attributes" error
**Solution**: Make sure all schemas use `orm_mode = True` instead.

### Issue: "model_validate" error
**Solution**: Replace with `from_orm()` in all routers.

