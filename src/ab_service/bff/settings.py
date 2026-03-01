from packaging.markers import Environment
from pydantic import Field
from pydantic_settings import BaseSettings

from .models import Environment


class AppSettings(BaseSettings):
    """BFF Settings"""

    APP_ENV: Environment = Field(
        default=Environment.PRODUCTION,
        description="The application environment. Used for conditional logic and debugging. Set to 'development' for local dev.",
    )
    ALLOWED_ORIGINS: list[str] = Field(
        default_factory=list,
        description="List of allowed origins for CORS. Should be set to the FE app URL in production (e.g. 'http://localhost:9998' for local dev).",
    )
    TRUSTED_PROXY_HOSTS: list[str] = Field(
        default_factory=list,
        description="List of trusted proxy hosts for ProxyHeadersMiddleware. Should be list of domains that may be forwarding requests to the BFF (e.g. API Gateway).",
    )
