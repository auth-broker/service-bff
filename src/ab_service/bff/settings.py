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
    TRUSTED_PROXY_IPS: list[str] = Field(
        default_factory=list,
        description="List of trusted proxy IPs for ProxyHeadersMiddleware. Should be set to the IPs of proxies that may be forwarding requests to the BFF (e.g. API Gateway).",
    )
    ALLOWED_HOSTS: list[str] = Field(
        default_factory=list,
        description="List of allowed hosts for TrustedHostMiddleware. Should be set to the BE app hostname in production.",
    )
    ALLOWED_ORIGINS: list[str] = Field(
        default_factory=list,
        description="List of allowed originals for CORSMiddleware. Should be set to the FE app URL in production.",
    )