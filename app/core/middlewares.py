from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import time

from fastapi import APIRouter, FastAPI, Request, Response
from app.utils.time_conversion import _str_time


class AccessMiddleware(BaseHTTPMiddleware):
    """Middleware"""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

