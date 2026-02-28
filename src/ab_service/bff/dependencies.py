"""Dependency providers for the BFF service.

This module exposes dependency-injected factories for the database and
remote service clients used by the BFF routes.
"""

from typing import Annotated

from ab_client.auth_client import AsyncClient as AuthClient
from ab_client.token_issuer import AsyncClient as TokenIssuerClient
from ab_client.token_issuer_store import AsyncClient as TokenIssuerStoreClient
from ab_client.token_store import AsyncClient as TokenStoreClient
from ab_client.token_validator import AsyncClient as TokenValidatorClient
from ab_client.user import AsyncClient as UserClient
from ab_core.database.databases import Database
from ab_core.dependency import Depends, inject, pydanticize_type
from ab_core.dependency.loaders.environment_object import ObjectLoaderEnvironment


@inject
async def get_database(
    _db: Annotated[
        Database,
        Depends(
            Database,
            persist=True,
        ),
    ],
):
    yield _db


@inject
async def get_auth_client(
    _auth_client: Annotated[
        AuthClient,
        Depends(
            ObjectLoaderEnvironment[pydanticize_type(AuthClient)](env_prefix="AUTH_SERVICE"),
            persist=True,
        ),
    ],
):
    yield _auth_client


@inject
async def get_token_validator_client(
    _token_validator_client: Annotated[
        TokenValidatorClient,
        Depends(
            ObjectLoaderEnvironment[TokenValidatorClient](env_prefix="TOKEN_VALIDATOR_SERVICE"),
            persist=True,
        ),
    ],
):
    yield _token_validator_client


@inject
async def get_user_client(
    _user_client: Annotated[
        UserClient,
        Depends(
            ObjectLoaderEnvironment[UserClient](env_prefix="USER_SERVICE"),
            persist=True,
        ),
    ],
):
    yield _user_client


@inject
async def get_token_issuer_client(
    _token_issuer_client: Annotated[
        TokenIssuerClient,
        Depends(
            ObjectLoaderEnvironment[TokenIssuerClient](env_prefix="TOKEN_ISSUER_SERVICE"),
            persist=True,
        ),
    ],
):
    yield _token_issuer_client


@inject
async def get_token_issuer_store_client(
    _token_issuer_store_client: Annotated[
        TokenIssuerStoreClient,
        Depends(
            ObjectLoaderEnvironment[TokenIssuerStoreClient](env_prefix="TOKEN_ISSUER_STORE_SERVICE"),
            persist=True,
        ),
    ],
):
    yield _token_issuer_store_client


@inject
async def get_token_store_client(
    _token_store_client: Annotated[
        TokenStoreClient,
        Depends(
            ObjectLoaderEnvironment[TokenStoreClient](env_prefix="TOKEN_STORE_SERVICE"),
            persist=True,
        ),
    ],
):
    yield _token_store_client


__all__ = [
    get_database,
    Database,
    get_auth_client,
    AuthClient,
    get_token_validator_client,
    TokenValidatorClient,
    get_user_client,
    UserClient,
    get_token_issuer_client,
    TokenIssuerClient,
    get_token_issuer_store_client,
    TokenIssuerStoreClient,
    get_token_store_client,
    TokenStoreClient,
]
