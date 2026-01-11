"""User-related API routes."""

from typing import Annotated

from ab_core.identity_context.dependency import IdentityContext, get_identity_context
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/token_issuer", tags=["Token Issuer"])


@router.get("", response_model=IdentityContext)
async def get_token_issuer(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(gettoken_issuer_store_client)],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def get_token_issuers(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(gettoken_issuer_store_client)],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def create_token_issuer(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(gettoken_issuer_store_client)],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def update_token_issuer(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(gettoken_issuer_store_client)],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def delete_token_issuer(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(gettoken_issuer_store_client)],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=IdentityContext)
async def refresh_token_issuer(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(gettoken_issuer_store_client)],
):
    """Return the current user's identity context."""
    ...
