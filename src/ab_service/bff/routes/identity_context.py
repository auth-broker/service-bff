"""User-related API routes."""

from typing import Annotated

from ab_core.identity_context.dependency import IdentityContext, get_identity_context
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/identity-context", tags=["Identity Context"])


@router.get("", response_model=IdentityContext)
async def me(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
):
    """Return the current user's identity context."""
    return identity_context
