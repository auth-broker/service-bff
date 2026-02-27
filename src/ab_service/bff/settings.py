from urllib.parse import urlparse
import ipaddress
from pydantic import computed_field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings for the AB Service BFF."""

    FE_BASE_URL: str = "http://localhost:9998"  # Default base URL for the FE service

    @computed_field
    @property
    def FE_COOKIE_DOMAIN(self) -> str | None:
        """Compute the cookie domain for the FE service based on the FE_BASE_URL."""
        parsed_url = urlparse(self.FE_BASE_URL)
        if not parsed_url.hostname:
            return None

        hostname = parsed_url.hostname
        if hostname == "localhost":
            return None

        hostname = hostname.rstrip(".")

        # If it's an IP address, don't set Domain
        try:
            ipaddress.ip_address(hostname)
            return None
        except ValueError:
            pass

        return f".{hostname}"
