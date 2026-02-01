from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.exceptions import HTTPException
from fastapi import status
import re


from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import re

class PasswordValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/users" and request.method == "POST":
            try:
                body = await request.json()
                password = body.get("password")

                if not password:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Password is required"}
                    )

                if len(password) < 8:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Password must be at least 8 characters long"}
                    )

                if not re.search(r"[A-Z]", password):
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Password must contain an uppercase letter"}
                    )

                if not re.search(r"\d", password):
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Password must contain a digit"}
                    )

                if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Password must contain a special character"}
                    )

            except Exception as e:
                # Catch JSON parsing errors or unexpected issues
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": f"Invalid request body: {str(e)}"}
                )

        # Continue normal request flow
        response = await call_next(request)
        return response

