"""User-related API routes."""

from typing import Annotated

from ab_client.auth_client import OAuth2AuthorizeResponse, OAuth2TokenExposed, PKCEAuthorizeResponse
from fastapi import APIRouter, Depends

from ab_service.bff.dependencies import AuthClient, get_auth_client

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/login", response_model=OAuth2AuthorizeResponse | PKCEAuthorizeResponse)
async def login(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
):
    """Return the current user's identity context."""
    return await auth_client.get_login_url_login_get()


@router.get("/callback", response_model=OAuth2TokenExposed)
async def callback(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
):
    """Return the current user's identity context."""
    return await auth_client.callback_callback_get()
