from fastapi import Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from jwt import PyJWTError

class VerifyUserMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_service, exclude_paths=None):
        super().__init__(app)
        self.auth_service = auth_service
        self.exclude_paths = exclude_paths or []

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"status": "failed", "message": "Missing or invalid token"},
                )

        token = auth_header.split(" ")[1]
        user = self.auth_service.verify_user_token(token)
        request.state.user = user
        return await call_next(request)