import uuid
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import (
    correlation_id_var,
    logger,
)


class CorrelationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        correlation_id = str(uuid.uuid4())

        correlation_id_var.set(correlation_id)

        start_time = time.perf_counter()

        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
            }
        )

        response = await call_next(request)

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        logger.info(
            "Request completed",
            extra={
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            }
        )

        response.headers["X-Correlation-ID"] = correlation_id

        return response