"""User-related API routes."""

from typing import Annotated

from ab_client.auth_client import AuthorizeResponse, OAuth2TokenExposed, LoginRequest
from fastapi import APIRouter, Depends, Response, Request

from ab_service.bff.dependencies import AuthClient, get_auth_client
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, status

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/login")
async def login(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
):
    """Return the current user's identity context."""
    login_payload = await auth_client.get_login_url_login_post(
        data=LoginRequest(
            app_context={
                # after the token exchange, to a final return back to the original
                # requested page.
                "return_to": "/"
            }
        )
    )
    return RedirectResponse(url=login_payload.url, status_code=status.HTTP_302_FOUND)


@router.get("/callback", response_model=OAuth2TokenExposed)
async def callback(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
    response: Response,
    request: Request,
):
    """Return the current user's identity context."""
    token = await auth_client.callback_callback_get(
        redirect_url=str(request.url),
    )

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    if token.refresh_token is not None:
        response.set_cookie(
            key="refresh_token",
            value=token.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
    if token.id_token is not None:
        response.set_cookie(
            key="id_token",
            value=token.id_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

    app_context= token.app_context or {}
    return RedirectResponse(
        url=app_context.get("return_to", "/"),
        status_code=status.HTTP_302_FOUND,
    )
