"""Pydantic schemas for token issuer endpoints.

Defines request/response models used by the token issuer API.
"""

from ab_client.token_issuer_store import TokenIssuer
from pydantic import BaseModel


class CreateTokenIssuerRequest(BaseModel):
    """Request model for creating a token issuer.

    Attributes:
        name: str: Human-friendly name for the issuer.
        token_issuer: TokenIssuer: The issuer configuration object.

    """

    name: str
    token_issuer: TokenIssuer
