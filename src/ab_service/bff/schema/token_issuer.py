from __future__ import annotations

from typing import Annotated

from ab_client_token_issuer_store.models.o_auth_2_token_issuer import OAuth2TokenIssuer
from ab_client_token_issuer_store.models.pkceo_auth_2_token_issuer import PKCEOAuth2TokenIssuer
from ab_core.dependency import pydanticize_type
from pydantic import Field, BaseModel


TokenIssuer = Annotated[
    pydanticize_type(OAuth2TokenIssuer) | pydanticize_type(PKCEOAuth2TokenIssuer),
    Field(discriminator="type_"),
]


class CreateTokenIssuerRequest(BaseModel):
    name: str
    token_issuer: TokenIssuer
