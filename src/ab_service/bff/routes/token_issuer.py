"""User-related API routes."""

from typing import Annotated

from ab_client_token_issuer_store.api.token_issuer import (
    create_token_issuer_post,
)
from ab_client_token_issuer_store.models.create_token_issuer_request import CreateTokenIssuerRequest
from ab_core.identity_context.dependency import IdentityContext, get_identity_context
from fastapi import APIRouter, Depends

from ab_service.bff.schema.token_issuer import CreateTokenIssuerRequest

router = APIRouter(prefix="/token_issuer", tags=["Token Issuer"])


@router.get("/{token_issuer_id}", response_model=IdentityContext)
async def get_token_issuer(
    token_issuer_id: Annotated[UUID, Path(description="Token issuer id")],
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(gettoken_issuer_store_client)],
):
    """Return the current user's identity context."""
    ...


@router.get("", response_model=...)
async def create_token_issuer(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
    token_issuer_store_client: Annotated[TokenIssuerStoreClient, Depends(gettoken_issuer_store_client)],
):
    """Return the current user's identity context."""
    # TODO: we need to update the token issuer store service schemas to be more user friendly.
    #       currently they are coupled to the token issuer schemas which is not nice. Once that is done
    #       we can re-use the CreateTokenIssuerRequest from token issuer store here.
    response = await create_token_issuer_post.asyncio(
        client=token_issuer_store_client,
        create_token_issuer_request=CreateTokenIssuerRequest(
            name=...,
            token_issuer=...,
            created_by=identity_context.user.id,
        ),
    )
    return token_issuer.to_dict()
