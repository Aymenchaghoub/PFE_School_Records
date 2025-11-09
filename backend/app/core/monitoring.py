"""
Monitoring and Observability Module
Provides metrics, logging, and optional Sentry integration
"""
import time
import logging
from datetime import datetime
from typing import Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import os

# Initialize logger
logger = logging.getLogger(__name__)

# Metrics storage (in-memory for simplicity, use Redis/Prometheus in production)
class MetricsStore:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.request_duration_sum = 0.0
        self.error_count = 0
        self.endpoint_counts = {}
        
    def record_request(self, endpoint: str, duration: float, status_code: int):
        """Record a request for metrics"""
        self.request_count += 1
        self.request_duration_sum += duration
        
        if status_code >= 400:
            self.error_count += 1
            
        if endpoint not in self.endpoint_counts:
            self.endpoint_counts[endpoint] = 0
        self.endpoint_counts[endpoint] += 1
    
    def get_uptime(self) -> float:
        """Get uptime in seconds"""
        return time.time() - self.start_time
    
    def get_average_duration(self) -> float:
        """Get average request duration"""
        if self.request_count == 0:
            return 0.0
        return self.request_duration_sum / self.request_count
    
    def get_metrics(self) -> dict:
        """Get all metrics"""
        uptime = self.get_uptime()
        return {
            "uptime_seconds": round(uptime, 2),
            "uptime_formatted": self._format_uptime(uptime),
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate": round(self.error_count / max(self.request_count, 1) * 100, 2),
            "average_response_time_ms": round(self.get_average_duration() * 1000, 2),
            "requests_per_minute": round(self.request_count / max(uptime / 60, 1), 2),
            "endpoint_counts": dict(sorted(
                self.endpoint_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]),  # Top 10 endpoints
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    @staticmethod
    def _format_uptime(seconds: float) -> str:
        """Format uptime as human-readable string"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        
        return " ".join(parts)


# Global metrics store
metrics_store = MetricsStore()


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging and metrics collection"""
    
    def __init__(self, app: ASGIApp, enable_logging: bool = True):
        super().__init__(app)
        self.enable_logging = enable_logging
    
    async def dispatch(self, request: Request, call_next):
        # Skip monitoring for health/metrics endpoints to avoid noise
        if request.url.path in ["/health", "/metrics"]:
            return await call_next(request)
        
        # Record start time
        start_time = time.time()
        
        # Log request
        if self.enable_logging:
            logger.info(f"→ {request.method} {request.url.path}")
        
        # Process request
        try:
            response: Response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Record metrics
            metrics_store.record_request(
                endpoint=request.url.path,
                duration=duration,
                status_code=response.status_code
            )
            
            # Log response
            if self.enable_logging:
                logger.info(
                    f"← {request.method} {request.url.path} "
                    f"→ {response.status_code} ({duration*1000:.2f}ms)"
                )
            
            # Add custom headers
            response.headers["X-Response-Time"] = f"{duration*1000:.2f}ms"
            response.headers["X-Request-ID"] = str(id(request))
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"✗ {request.method} {request.url.path} → Error: {str(e)}")
            metrics_store.record_request(request.url.path, duration, 500)
            raise


# Optional Sentry integration
sentry_sdk: Optional[object] = None

def initialize_sentry(dsn: Optional[str] = None):
    """Initialize Sentry for error tracking"""
    global sentry_sdk
    
    if not dsn:
        dsn = os.getenv("SENTRY_DSN")
    
    if not dsn or os.getenv("ENABLE_SENTRY", "false").lower() != "true":
        logger.info("Sentry integration disabled")
        return
    
    try:
        import sentry_sdk as sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        
        sdk.init(
            dsn=dsn,
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=0.1,  # 10% of transactions
            environment=os.getenv("ENVIRONMENT", "development"),
        )
        
        sentry_sdk = sdk
        logger.info("✅ Sentry integration initialized")
        
    except ImportError:
        logger.warning("⚠️  Sentry SDK not installed. Install with: pip install sentry-sdk")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Sentry: {e}")


def get_metrics() -> dict:
    """Get current metrics"""
    return metrics_store.get_metrics()
