from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List
import os
import sys


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    All sensitive values MUST be provided via environment variables.
    No defaults are provided for security-critical settings.
    """
    
    # Database - REQUIRED
    database_url: str = Field(
        ...,
        description="Database connection URL (e.g., mysql+pymysql://user:pass@host/db)"
    )
    
    # Security - REQUIRED
    secret_key: str = Field(
        ...,
        min_length=32,
        description="Secret key for JWT signing (min 32 characters)"
    )
    jwt_expire_minutes: int = Field(default=60, ge=1, le=1440)
    jwt_refresh_expire_days: int = Field(default=7, ge=1, le=30)
    algorithm: str = Field(default="HS256")
    
    # CORS - REQUIRED (no wildcard default)
    cors_origins: List[str] = Field(
        ...,
        description="Comma-separated list of allowed CORS origins"
    )
    
    # API Configuration
    api_v1_prefix: str = Field(default="/api")
    
    # Environment
    environment: str = Field(default="development")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string to list."""
        if isinstance(v, str):
            origins = [origin.strip() for origin in v.split(',') if origin.strip()]
        elif isinstance(v, list):
            # Already parsed as list by pydantic-settings
            origins = [str(origin).strip() for origin in v if origin]
        else:
            origins = [str(v)]
        
        # Warn if wildcard in production
        if '*' in origins and os.getenv('ENVIRONMENT', 'development') == 'production':
            print("⚠️  WARNING: CORS wildcard '*' detected in production environment!")
            print("   This allows requests from ANY origin and is a security risk.")
        return origins
    
    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, v):
        """Ensure secret key is not a default/example value."""
        insecure_patterns = ['change', 'secret', 'example', 'test', 'demo', 'your-']
        if any(pattern in v.lower() for pattern in insecure_patterns):
            if os.getenv('ENVIRONMENT', 'development') == 'production':
                raise ValueError(
                    "SECRET_KEY appears to be a default/example value! "
                    "Generate a secure random key for production."
                )
            print("⚠️  WARNING: SECRET_KEY appears to be an example value.")
        return v


# Initialize settings
try:
    settings = Settings()
    print("✅ Configuration loaded successfully")
except Exception as e:
    print(f"❌ Configuration Error: {e}")
    print("\n💡 Make sure you have a .env file with all required variables.")
    print("   Copy .env.example to .env and fill in the values.\n")
    sys.exit(1)
