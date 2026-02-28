"""User-related API routes."""

import ipaddress
from typing import Annotated
from urllib.parse import urlparse, urljoin

from ab_client.auth_client import LoginRequest, OAuth2TokenExposed
from ab_core.identity_context.dependency import IdentityContext, get_identity_context
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse

from ab_service.bff.dependencies import AuthClient, get_auth_client

router = APIRouter(prefix="/identity-context", tags=["Identity Context"])


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/login")
async def login(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
    request: Request,
    return_to: str | None = None,
):
    """Return the current user's identity context."""
    if not return_to:
        return_to = urljoin(str(request.base_url), "/")

    parsed_url = urlparse(return_to)
    hostname = parsed_url.hostname
    if not hostname:
        raise ValueError("Invalid return_to URL: hostname could not be determined")

    login_payload = await auth_client.get_login_url_login_post(
        data=LoginRequest(
            app_context={
                # after the token exchange, to a final return back to the original
                # requested page.
                "return_to": return_to,
            }
        )
    )
    return RedirectResponse(url=login_payload.url, status_code=status.HTTP_302_FOUND)


@router.get("/callback", response_model=OAuth2TokenExposed)
async def callback(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
    request: Request,
):
    """Return the current user's identity context."""
    # exchange the auth code for tokens
    token = await auth_client.callback_callback_get(
        redirect_url=str(request.url),
    )

    # determine return_to url for redirect after login and cookie domain for setting cookies
    app_context = token.app_context or {}
    return_to = app_context.get("return_to", "/")

    # determine cookie domain (based off where the user should be redirected back to after login, which is typically the FE app)
    parsed_url = urlparse(return_to)
    hostname = parsed_url.hostname
    cookie_domain = None
    if hostname is not None:
        if hostname != "localhost":
            cookie_domain = f".{hostname}"
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            cookie_domain = f".{hostname}"

    # prepare redirect response to frontend with cookies set
    redirect = RedirectResponse(
        url=return_to,
        status_code=status.HTTP_302_FOUND,
    )

    # set frontend cookies with api tokens
    cookie_kwargs = dict(
        httponly=True,
        domain=cookie_domain,
        secure=True,
        samesite="lax",
        path="/",
    )
    redirect.set_cookie("access_token", token.access_token, **cookie_kwargs)
    if token.refresh_token is not None:
        redirect.set_cookie("refresh_token", token.refresh_token, **cookie_kwargs)
    if token.id_token is not None:
        redirect.set_cookie("id_token", token.id_token, **cookie_kwargs)

    return redirect


@router.get("/me", response_model=IdentityContext)
async def me(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
):
    """Return the current user's identity context."""
    return identity_context
