"""User-related API routes."""

import ipaddress
import logging
from typing import Annotated

from ab_client.auth_client import LoginRequest, OAuth2TokenExposed, RefreshTokenRequest
from ab_core.identity_context.dependency import IdentityContext, get_identity_context
from fastapi import APIRouter, Cookie, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from yarl import URL

from ab_service.bff.dependencies import AppSettings, AuthClient, get_app_settings, get_auth_client
from ab_service.bff.models import Environment

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
        return_to = URL(str(request.base_url)).with_path("/").human_repr()

    # valid return to URL must have a hostname (to determine cookie domain for later);
    parsed_url = URL(return_to)
    hostname = parsed_url.host
    if not hostname:
        raise ValueError("Invalid return_to URL: hostname could not be determined")

    # kickstart the oauth 2.0 login flow by getting the authorization URL to redirect the user to
    login_payload = await auth_client.get_login_url_login_post(
        data=LoginRequest(
            scope="openid email profile offline_access entitlements",
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
    app_settings: Annotated[AppSettings, Depends(get_app_settings)],
    refresh_token: Annotated[str | None, Cookie(alias="refresh_token")] = None,
    return_to: str | None = None,
):
    """Return the current user's identity context."""
    # default return_to to the base URL of wherever the request came from (e.g. FE app)
    if not return_to:
        return_to = URL(str(request.base_url)).with_path("/").human_repr()

    login_redirect = URL("/auth/login").with_query({"return_to": return_to}).human_repr()
    if not refresh_token:
        logger.debug("Missing refresh token, redirecting to login")
        return RedirectResponse(url=login_redirect, status_code=status.HTTP_302_FOUND)

    # exchange the auth code for tokens
    try:
        token = await auth_client.refresh_token_refresh_post(
            data=RefreshTokenRequest(
                refresh_token=refresh_token,
            ),
        )
    except Exception as e:
        logger.debug("Token refresh failed, redirecting to login", exc_info=e)
        return RedirectResponse(url=login_redirect, status_code=status.HTTP_302_FOUND)

    return _handle_cookie_redirect(return_to, token=token, app_settings=app_settings)


@router.get("/callback", response_model=OAuth2TokenExposed)
async def callback(
    auth_client: Annotated[AuthClient, Depends(get_auth_client)],
    app_settings: Annotated[AppSettings, Depends(get_app_settings)],
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

    return _handle_cookie_redirect(return_to, token=token, app_settings=app_settings)


@router.get("/logout")
async def logout(
    request: Request,
    app_settings: Annotated[AppSettings, Depends(get_app_settings)],
    return_to: str | None = None,
):
    """Logout the user by clearing cookies and redirecting to the given return_to URL (or base URL if not provided)."""
    # Where to send the browser after logout
    if not return_to:
        return_to = URL(str(request.base_url)).with_path("/").human_repr()

    # no token forces cookie clearing in the redirect response
    return _handle_cookie_redirect(return_to, token=None, app_settings=app_settings)


@router.get("/me", response_model=IdentityContext)
async def me(
    request: Request,
    identity_context: Annotated[IdentityContext, Depends(get_identity_context)],
):
    """Return the current user's identity context."""
    return identity_context


def _get_cookie_domain(url: str) -> str | None:
    parsed_url = URL(url)
    hostname = parsed_url.host
    cookie_domain = None

    # localhost / ip addresses should not have a cookie domain,
    # but other hostnames should be set with a cookie domain
    # of the base domain (e.g. "example.com" or ".example.com")
    # to allow subdomains to access the cookies
    if hostname and hostname != "localhost":
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            cookie_domain = f".{hostname}"

    return cookie_domain


def _handle_cookie_redirect(
    return_to: str,
    *,
    token: OAuth2TokenExposed | None = None,
    app_settings: AppSettings,
) -> RedirectResponse:
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
        secure=app_settings.APP_ENV in {Environment.PRODUCTION, Environment.STAGING},
        samesite="lax",
        path="/",
    )

    # save token to cookies
    if token:
        for key in ("access_token", "refresh_token", "id_token"):
            value = getattr(token, key)
            if value:
                redirect.set_cookie(key, value, **cookie_kwargs)
            else:
                logger.warning(f"No {key} returned from callback; frontend may not work as expected")

    # clear token cookies
    else:
        for key in ("access_token", "refresh_token", "id_token"):
            redirect.delete_cookie(key, **cookie_kwargs)

    return redirect
