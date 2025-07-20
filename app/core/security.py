import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# from starlette.middleware.base import BaseHTTPMiddleware
from app.core.settings import settings
from app.core.middlewares import TraceIDMiddleware


logger = logging.getLogger("security")


def configure_security(app: FastAPI):
    logger.info("Configuring security middleware...")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["*"],
    )

    # TraceID
    app.add_middleware(TraceIDMiddleware)

    # HTTPS redirect only if in production
    if settings.env == "production":
        app.add_middleware(HTTPSRedirectMiddleware)
        logger.info("HTTPS redirect enabled (production mode)")

    logger.info("Security middleware configured.")
