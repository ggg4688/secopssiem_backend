import time

from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        started_at = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        print(
            f"{request.method} {request.url.path} -> {response.status_code} "
            f"in {elapsed_ms:.2f}ms"
        )
        return response

