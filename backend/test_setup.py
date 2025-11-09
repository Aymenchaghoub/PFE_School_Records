"""
Test script to verify backend setup and dependencies.
Run: python test_setup.py
"""
import sys

def test_imports():
    """Test all critical imports."""
    print("Testing imports...")
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI: {e}")
        return False
    
    try:
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__}")
        if pydantic.__version__.startswith("2."):
            print("⚠️  Warning: Pydantic v2 detected. Should be v1.10.13 for Python 3.13")
    except ImportError as e:
        print(f"❌ Pydantic: {e}")
        return False
    
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"❌ SQLAlchemy: {e}")
        return False
    
    try:
        import pymysql
        print(f"✅ PyMySQL {pymysql.__version__}")
    except ImportError as e:
        print(f"❌ PyMySQL: {e}")
        return False
    
    try:
        from jose import jwt
        print("✅ python-jose")
    except ImportError as e:
        print(f"❌ python-jose: {e}")
        return False
    
    try:
        from passlib.context import CryptContext
        print("✅ passlib")
    except ImportError as e:
        print(f"❌ passlib: {e}")
        return False
    
    return True

def test_app_imports():
    """Test app module imports."""
    print("\nTesting app imports...")
    try:
        from app.core.config import settings
        print("✅ Config loaded")
        print(f"   API prefix: {settings.api_v1_prefix}")
    except Exception as e:
        print(f"❌ Config: {e}")
        return False
    
    try:
        from app.core.database import Base, engine, SessionLocal
        print("✅ Database module")
    except Exception as e:
        print(f"❌ Database: {e}")
        return False
    
    try:
        from app.models import User, Class, Subject, Grade, Absence, Event
        print("✅ All models imported")
    except Exception as e:
        print(f"❌ Models: {e}")
        return False
    
    try:
        from app.routers import auth, users, classes
        print("✅ Routers imported")
    except Exception as e:
        print(f"❌ Routers: {e}")
        return False
    
    try:
        from app.main import app
        print("✅ FastAPI app created")
    except Exception as e:
        print(f"❌ App: {e}")
        return False
    
    return True

def test_database_connection():
    """Test database connection."""
    print("\nTesting database connection...")
    try:
        from app.core.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("   This is OK if database is not configured yet.")
        print("   Set DATABASE_URL in .env file to test connection.")
        return False

def main():
    print("=" * 50)
    print("Backend Setup Verification")
    print("=" * 50)
    print(f"Python version: {sys.version}\n")
    
    all_ok = True
    
    if not test_imports():
        all_ok = False
    
    if not test_app_imports():
        all_ok = False
    
    db_connected = test_database_connection()
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ All imports successful!")
        if db_connected:
            print("✅ Database connected!")
        else:
            print("⚠️  Database not connected (configure .env file)")
        print("\nNext steps:")
        print("1. Create .env file with DATABASE_URL")
        print("2. Run: python -m app.seed_data")
        print("3. Run: uvicorn app.main:app --reload")
    else:
        print("❌ Some imports failed. Check requirements.txt")
    print("=" * 50)

if __name__ == "__main__":
    main()

