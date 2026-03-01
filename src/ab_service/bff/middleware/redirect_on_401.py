from urllib.parse import quote

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse, Response


class RedirectOn401Middleware(BaseHTTPMiddleware):
    """Middleware to redirect to refresh/login on 401 Unauthorized responses."""

    def __init__(
        self,
        app,
        login_path: str = "/auth/login",
        refresh_path: str = "/auth/refresh",
        refresh_cookie_name: str = "refresh_token",
        redirect_status_code: int = 302,
    ):
        super().__init__(app)
        self.login_path = login_path
        self.refresh_path = refresh_path
        self.refresh_cookie_name = refresh_cookie_name
        self.redirect_status_code = redirect_status_code

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        if response.status_code != 401:
            return response

        # Preserve where the user was trying to go
        return_to = request.url
        return_to_url = quote(str(return_to), safe="")

        has_refresh_cookie = bool(request.cookies.get(self.refresh_cookie_name))

        target = self.refresh_path if has_refresh_cookie else self.login_path
        return RedirectResponse(
            url=f"{target}?return_to={return_to_url}",
            status_code=self.redirect_status_code,
        )
