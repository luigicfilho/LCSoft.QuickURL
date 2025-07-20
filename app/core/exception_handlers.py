import uuid
import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from tortoise.exceptions import IntegrityError
from jwt import ExpiredSignatureError, PyJWTError
from pydantic import ValidationError
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger("exception_handlers")


def create_problem_response(
    request: Request, status_code: int, title: str, detail: str
):
    trace_id = str(uuid.uuid4())
    logger.error(f"[{trace_id}] {title}: {detail} | Path: {request.url.path}")

    return JSONResponse(
        status_code=status_code,
        content={
            "type": "about:blank",
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": request.url.path,
            "trace_id": trace_id,
        },
    )


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request, exc):
        return create_problem_response(
            request,
            status_code=429,
            title="Rate limit Error",
            detail="Rate limit exceeded",
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return create_problem_response(
            request,
            status_code=400,
            title="Database Integrity Error",
            detail="Possible duplicate or constraint violation",
        )

    @app.exception_handler(ExpiredSignatureError)
    async def jwt_expired_handler(request: Request, exc: ExpiredSignatureError):
        return create_problem_response(
            request, status_code=401, title="JWT Expired", detail="Token has expired"
        )

    @app.exception_handler(PyJWTError)
    async def jwt_invalid_handler(request: Request, exc: PyJWTError):
        return create_problem_response(
            request,
            status_code=403,
            title="Invalid JWT",
            detail="Invalid token provided",
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return create_problem_response(
            request, status_code=422, title="Validation Error", detail=str(exc.errors())
        )

    @app.exception_handler(ConnectionError)
    async def db_connection_error_handler(request: Request, exc: ConnectionError):
        return create_problem_response(
            request,
            status_code=500,
            title="Database Connection Error",
            detail="Could not connect to the database",
        )
