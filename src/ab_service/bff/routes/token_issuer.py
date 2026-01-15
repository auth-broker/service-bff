"""User-related API routes."""

from typing import Annotated

from ab_client.token_issuer_store import (
    CreateTokenIssuerRequest as TokenIssuerStoreCreateTokenIssuerRequest,
)
from ab_client.token_issuer_store import (
    ManagedTokenIssuer,
)
from ab_core.identity_context.dependency import IdentityContext, get_identity_context
from fastapi import APIRouter, Depends

from ab_service.bff.dependencies import TokenIssuerStoreClient, get_token_issuer_store_client
from ab_service.bff.schema.token_issuer import CreateTokenIssuerRequest

router = APIRouter(prefix="/token_issuer", tags=["Token Issuer"])


@router.get("/{token_issuer_id}", response_model=ManagedTokenIssuer)
async def get_token_issuer(
    token_issuer_id: str,
    _identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(get_token_issuer_store_client)],
):
    """Lookup a token issuer by its ID."""
    return await token_issuer_store_client.get_token_issuer__id__get(
        id=token_issuer_id,
        # TODO: lookup should include the user id, ensuring
        #       users can only access their own token issuers
    )


@router.get("", response_model=ManagedTokenIssuer)
async def create_token_issuer(
    request: CreateTokenIssuerRequest,
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(get_token_issuer_store_client)],
):
    """Create a new token issuer."""
    return await token_issuer_store_client.create_token_issuer_post(
        data=TokenIssuerStoreCreateTokenIssuerRequest(
            name=request.name,
            token_issuer=request.token_issuer,
            created_by=identity_context.user.id,
        ),
    )
