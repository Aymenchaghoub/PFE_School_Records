"""
Test script to verify modern FastAPI + Pydantic v2 setup.
Run: python test_modern_setup.py
"""
import sys

def test_imports():
    """Test all critical imports."""
    print("Testing imports...")
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
        if not fastapi.__version__.startswith("0.11"):
            print(f"⚠️  Warning: Expected FastAPI >= 0.115.0, got {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI: {e}")
        return False
    
    try:
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__}")
        if not pydantic.__version__.startswith("2."):
            print(f"⚠️  Warning: Expected Pydantic >= 2.5.0, got {pydantic.__version__}")
    except ImportError as e:
        print(f"❌ Pydantic: {e}")
        return False
    
    try:
        import pydantic_settings
        print(f"✅ pydantic-settings {pydantic_settings.__version__}")
    except ImportError as e:
        print(f"❌ pydantic-settings: {e}")
        return False
    
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"❌ SQLAlchemy: {e}")
        return False
    
    return True

def test_app_imports():
    """Test app module imports."""
    print("\nTesting app imports...")
    try:
        from app.core.config import settings
        print("✅ Config loaded")
        print(f"   API prefix: {settings.api_v1_prefix}")
        # Test Pydantic v2 syntax
        if hasattr(settings, 'model_config'):
            print("✅ Using Pydantic v2 SettingsConfigDict")
        else:
            print("⚠️  Using old Config class")
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
        from app.schemas.user import UserResponse
        # Test Pydantic v2 syntax
        if hasattr(UserResponse, 'model_config'):
            print("✅ Schemas using Pydantic v2 ConfigDict")
        else:
            print("⚠️  Schemas using old Config class")
    except Exception as e:
        print(f"❌ Schemas: {e}")
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

def test_pydantic_v2_syntax():
    """Test Pydantic v2 specific syntax."""
    print("\nTesting Pydantic v2 syntax...")
    try:
        from app.schemas.user import UserResponse
        from app.models.user import User, UserRole
        from app.core.security import get_password_hash
        
        # Create a test user
        test_user = User(
            id=999,
            name="Test User",
            email="test@example.com",
            password=get_password_hash("test"),
            role=UserRole.ADMIN
        )
        
        # Test model_validate (Pydantic v2)
        response = UserResponse.model_validate(test_user)
        print("✅ model_validate() works (Pydantic v2)")
        
        if hasattr(response, 'id') and response.id == 999:
            print("✅ UserResponse validation successful")
        else:
            print("⚠️  UserResponse validation issue")
            return False
            
    except Exception as e:
        print(f"❌ Pydantic v2 syntax test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    print("=" * 50)
    print("Modern FastAPI + Pydantic v2 Setup Verification")
    print("=" * 50)
    print(f"Python version: {sys.version}\n")
    
    all_ok = True
    
    if not test_imports():
        all_ok = False
    
    if not test_app_imports():
        all_ok = False
    
    if not test_pydantic_v2_syntax():
        all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ All tests passed!")
        print("\nNext steps:")
        print("1. Create .env file with DATABASE_URL")
        print("2. Run: python -m app.seed_data")
        print("3. Run: uvicorn app.main:app --reload")
        print("4. Open: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Check errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()

