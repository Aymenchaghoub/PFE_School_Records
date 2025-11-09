"""
Metrics and Monitoring Endpoints
Provides system health and performance metrics
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.monitoring import get_metrics
import psutil
import os

router = APIRouter(prefix="/metrics", tags=["Monitoring"])


@router.get("", summary="Get system metrics")
async def get_system_metrics(db: Session = Depends(get_db)):
    """
    Get comprehensive system metrics including:
    - Application uptime
    - Request statistics
    - Database status
    - System resources (CPU, Memory)
    """
    # Get application metrics
    app_metrics = get_metrics()
    
    # Check database status
    db_status = "connected"
    db_error = None
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "disconnected"
        db_error = str(e)
    
    # Get system resources (if psutil is available)
    system_metrics = {}
    try:
        system_metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent,
        }
    except (ImportError, Exception):
        # psutil not available or error
        system_metrics = {
            "cpu_percent": None,
            "memory_percent": None,
            "disk_percent": None,
        }
    
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "application": app_metrics,
        "database": {
            "status": db_status,
            "error": db_error,
        },
        "system": system_metrics,
    }


@router.get("/health", summary="Simple health check")
async def health_check(db: Session = Depends(get_db)):
    """
    Simple health check endpoint for load balancers and monitoring tools
    Returns 200 OK if the application and database are operational
    """
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }
