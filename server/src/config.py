from typing import Any

from pydantic import PostgresDsn, RedisDsn, model_validator, field_validator
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn

    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: str = "http://localhost:5173"
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: str = "*"

    APP_VERSION: str = "1"

    @field_validator("CORS_ORIGINS")
    def parse_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",")]
        return v
        
    @field_validator("CORS_HEADERS")
    def parse_cors_headers(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [header.strip() for header in v.split(",")]
        return v

    @model_validator(mode="after")
    def validate_sentry_non_local(self) -> "Config":
        if self.ENVIRONMENT.is_deployed and not self.SENTRY_DSN:
            raise ValueError("Sentry is not set")

        return self


settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
