"""User-related API routes."""

from typing import Annotated
from urllib.parse import urljoin
from ab_client.auth_client import LoginRequest, OAuth2TokenExposed
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse

from ab_service.bff.dependencies import AppSettings, AuthClient, get_app_settings, get_auth_client

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
    app_settings: Annotated[AppSettings, Depends(get_app_settings)],
    response: Response,
    request: Request,
):
    """Return the current user's identity context."""
    token = await auth_client.callback_callback_get(
        redirect_url=str(request.url),
    )

    app_context = token.app_context or {}
    return_to_path = app_context.get("return_to", "/")

    return_to = urljoin(app_settings.FE_BASE_URL, return_to_path)

    redirect = RedirectResponse(
        url=return_to,
        status_code=status.HTTP_302_FOUND,
    )

    cookie_kwargs = dict(
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    if app_settings.FE_COOKIE_DOMAIN is not None:
        cookie_kwargs["domain"] = app_settings.FE_COOKIE_DOMAIN

    # set frontend cookies with api tokens
    redirect.set_cookie("access_token", token.access_token, **cookie_kwargs)
    if token.refresh_token is not None:
        redirect.set_cookie("refresh_token", token.refresh_token, **cookie_kwargs)
    if token.id_token is not None:
        redirect.set_cookie("id_token", token.id_token, **cookie_kwargs)

    return redirect