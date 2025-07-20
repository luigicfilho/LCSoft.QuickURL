import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("request_tracer")


class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id

        logger.info(
            f"[{trace_id}] Incoming request: {request.method} {request.url.path}"
        )

        response: Response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id

        logger.info(f"[{trace_id}] Response status: {response.status_code}")
        return response
