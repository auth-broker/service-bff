from urllib.parse import quote

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse, Response


class RedirectOn401Middleware(BaseHTTPMiddleware):
    """Middleware to redirect to login page on 401 Unauthorized responses."""

    def __init__(
        self,
        app,
        login_path: str = "/auth/login",
        redirect_status_code: int = 302,
    ):
        """Middleware to redirect to login page on 401 Unauthorized responses."""
        super().__init__(app)
        self.login_path = login_path
        self.redirect_status_code = redirect_status_code

    async def dispatch(self, request: Request, call_next) -> Response:
        """Middleware to redirect to login page on 401 Unauthorized responses."""
        response = await call_next(request)
        if response.status_code != 401:
            return response

        # Preserve where the user was trying to go
        return_to = request.url
        return_to_param = quote(str(return_to), safe="")
        return RedirectResponse(
            url=f"{self.login_path}?return_to={return_to_param}",
            status_code=self.redirect_status_code,
        )
