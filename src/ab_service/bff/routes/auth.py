"""User-related API routes."""

import ipaddress
import logging
from typing import Annotated
from urllib.parse import urljoin, urlparse

from ab_client.auth_client import LoginRequest, OAuth2TokenExposed, RefreshTokenRequest
from ab_core.identity_context.dependency import IdentityContext, get_identity_context
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse

from ab_service.bff.dependencies import AuthClient, get_auth_client

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/login")
async def login(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
    request: Request,
    return_to: str | None = None,
):
    """Return the current user's identity context."""
    # default return_to to the base URL of wherever the request came from (e.g. FE app)
    if not return_to:
        return_to = urljoin(str(request.base_url), "/")

    # valid return to URL must have a hostname (to determine cookie domain for later);
    parsed_url = urlparse(return_to)
    hostname = parsed_url.hostname
    if not hostname:
        raise ValueError("Invalid return_to URL: hostname could not be determined")

    # kickstart the oauth 2.0 login flow by getting the authorization URL to redirect the user to
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


@router.get("/refresh", response_model=OAuth2TokenExposed)
async def refresh(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
    request: Request,
    response: Response,
    refresh_token: Annotated[str | None, Cookie(alias="refresh_token")] = None,
    return_to: str | None = None,
):
    """Return the current user's identity context."""
    if not refresh_token:
        # Usually 400, but 401 will trigger the client to login again,
        # which is the desired behavior if they don't have a refresh token cookie
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
        )

    # default return_to to the base URL of wherever the request came from (e.g. FE app)
    if not return_to:
        return_to = urljoin(str(request.base_url), "/")

    # exchange the auth code for tokens
    try:
        token = await auth_client.refresh_token_refresh_post(
            data=RefreshTokenRequest(
                refresh_token=refresh_token,
            ),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed",
        ) from e

    return _handle_token(token, return_to)


@router.get("/callback", response_model=OAuth2TokenExposed)
async def callback(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
    request: Request,
):
    """Return the current user's identity context."""
    # exchange the auth code for tokens
    try:
        token = await auth_client.callback_callback_get(
            redirect_url=str(request.url),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login callback failed",
        ) from e

    # determine return_to url for redirect after login and cookie domain for setting cookies
    app_context = token.app_context or {}
    return_to = app_context.get("return_to", "/")

    return _handle_token(token, return_to)


@router.get("/me", response_model=IdentityContext)
async def me(
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
):
    """Return the current user's identity context."""
    return identity_context


def _get_cookie_domain(url: str) -> str | None:
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    cookie_domain = None
    if hostname and hostname != "localhost":
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            cookie_domain = f".{hostname}"
    return cookie_domain


def _handle_token(token: OAuth2TokenExposed, return_to: str) -> RedirectResponse:
    """Helper to prepare the redirect response with cookies set for the given token and return_to URL."""
    # determine cookie domain (based off where the user should be redirected back to after login, which is typically the FE app)
    cookie_domain = _get_cookie_domain(return_to)

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
    else:
        logger.warning("No refresh token returned from callback; user will be logged out when access token expires")
    if token.id_token is not None:
        redirect.set_cookie("id_token", token.id_token, **cookie_kwargs)
    else:
        logger.warning("No id token returned from callback; frontend will not have access to user claims")

    return redirect
