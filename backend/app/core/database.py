from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    echo=False  # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables. Imports all models first."""
    # Import all models to register them with Base.metadata
    from app.models import User, Class, Subject, Grade, Absence, Event
    try:
        from app.models.refresh_token import RefreshToken
    except ImportError:
        logger.warning("RefreshToken model not found, skipping...")
    
    try:
        # Test connection (SQLAlchemy 2.0 syntax)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("✅ Database connection successful")
        print("✅ Database connected")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        print(f"❌ Database connection failed: {e}")
        raise
    
    # Create all tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created/verified")
        print("✅ Database tables created/verified")
    except Exception as e:
        logger.error(f"❌ Database table creation failed: {e}")
        print(f"❌ Database table creation failed: {e}")
        raise
