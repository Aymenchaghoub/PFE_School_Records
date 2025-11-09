from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.database import init_db
from app.core.monitoring import MonitoringMiddleware, initialize_sentry
from app.routers import auth, users, classes, subjects, grades, absences, events, reports, statistics, metrics
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database (imports all models and creates tables)
try:
    init_db()
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="School Records Management System API",
    description="API for managing student academic records",
    version="1.0.0"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Monitoring middleware (add before CORS)
app.add_middleware(MonitoringMiddleware, enable_logging=True)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.api_v1_prefix}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.api_v1_prefix}/users", tags=["Users"])
app.include_router(classes.router, prefix=f"{settings.api_v1_prefix}/classes", tags=["Classes"])
app.include_router(subjects.router, prefix=f"{settings.api_v1_prefix}/subjects", tags=["Subjects"])
app.include_router(grades.router, prefix=f"{settings.api_v1_prefix}/grades", tags=["Grades"])
app.include_router(absences.router, prefix=f"{settings.api_v1_prefix}/absences", tags=["Absences"])
app.include_router(events.router, prefix=f"{settings.api_v1_prefix}/events", tags=["Events"])
app.include_router(reports.router, prefix=f"{settings.api_v1_prefix}/reports", tags=["Reports"])
app.include_router(statistics.router, prefix=f"{settings.api_v1_prefix}/statistics", tags=["Statistics"])
app.include_router(metrics.router, tags=["Monitoring"])


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info("🚀 School Records Management System API starting...")
    logger.info(f"📡 API prefix: {settings.api_v1_prefix}")
    logger.info(f"🌐 CORS origins: {settings.cors_origins}")
    
    # Initialize optional Sentry integration
    initialize_sentry()
    
    print("\n" + "="*50)
    print("🚀 School Records Management System API")
    print("="*50)
    print(f"📡 API Documentation: http://localhost:8000/docs")
    print(f"🔍 Health Check: http://localhost:8000/health")
    print(f"📊 Metrics: http://localhost:8000/metrics")
    print("="*50 + "\n")


@app.get("/")
def root():
    return {
        "message": "School Records Management System API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    try:
        from app.core.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
