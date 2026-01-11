"""User-related API routes."""

from typing import Annotated

from ab_core.database.session_context import db_session_async
from ab_core.identity_context.dependency import IdentityContext, get_identity_context
from fastapi import APIRouter
from fastapi import Depends as FDepends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/token_issuer", tags=["Token Issuer"])


@router.get("", response_model=IdentityContext)
async def get_token_issuer(
    _db_session: Annotated[AsyncSession, FDepends(db_session_async)],
    identity_context: Annotated[IdentityContext, FDepends(get_identity_context)],
    _token_issuer_store_client: Annotated[
        TokenIssuerStoreClient,
        Depends(
            ObjectLoaderEnvironment[pydanticize_type(TokenIssuerStoreClient)](env_prefix="TOKEN_ISSUER_STORE_SERVICE"),
            persist=True,
        ),
    ],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def get_token_issuers(
    _db_session: Annotated[AsyncSession, FDepends(db_session_async)],
    identity_context: Annotated[IdentityContext, FDepends(get_identity_context)],
    _token_issuer_store_client: Annotated[
        TokenIssuerStoreClient,
        Depends(
            ObjectLoaderEnvironment[pydanticize_type(TokenIssuerStoreClient)](env_prefix="TOKEN_ISSUER_STORE_SERVICE"),
            persist=True,
        ),
    ],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def create_token_issuer(
    _db_session: Annotated[AsyncSession, FDepends(db_session_async)],
    identity_context: Annotated[IdentityContext, FDepends(get_identity_context)],
    _token_issuer_store_client: Annotated[
        TokenIssuerStoreClient,
        Depends(
            ObjectLoaderEnvironment[pydanticize_type(TokenIssuerStoreClient)](env_prefix="TOKEN_ISSUER_STORE_SERVICE"),
            persist=True,
        ),
    ],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def update_token_issuer(
    _db_session: Annotated[AsyncSession, FDepends(db_session_async)],
    identity_context: Annotated[IdentityContext, FDepends(get_identity_context)],
    _token_issuer_store_client: Annotated[
        TokenIssuerStoreClient,
        Depends(
            ObjectLoaderEnvironment[pydanticize_type(TokenIssuerStoreClient)](env_prefix="TOKEN_ISSUER_STORE_SERVICE"),
            persist=True,
        ),
    ],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def delete_token_issuer(
    _db_session: Annotated[AsyncSession, FDepends(db_session_async)],
    identity_context: Annotated[IdentityContext, FDepends(get_identity_context)],
    _token_issuer_store_client: Annotated[
        TokenIssuerStoreClient,
        Depends(
            ObjectLoaderEnvironment[pydanticize_type(TokenIssuerStoreClient)](env_prefix="TOKEN_ISSUER_STORE_SERVICE"),
            persist=True,
        ),
    ],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def refresh_token_issuer(
    _db_session: Annotated[AsyncSession, FDepends(db_session_async)],
    identity_context: Annotated[IdentityContext, FDepends(get_identity_context)],
    _token_issuer_store_client: Annotated[
        TokenIssuerStoreClient,
        Depends(
            ObjectLoaderEnvironment[pydanticize_type(TokenIssuerStoreClient)](env_prefix="TOKEN_ISSUER_STORE_SERVICE"),
            persist=True,
        ),
    ],
):
    """Return the current user's identity context."""
    ...
