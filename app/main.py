"""Entry point for the URL Shortner."""

import logging
import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# from fastapi.openapi.docs import get_swagger_ui_html
from tortoise import Tortoise
from app.api.v1.routers import shorturl_router, admin_router
from app.core.extensions import limiter
from app.core.exception_handlers import register_exception_handlers
from app.core.security import configure_security

from app.core.config import (
    APP_TITLE,
    APP_DESCRIPTION,
    APP_SUMMARY,
    APP_VERSION,
    TERMS_URL,
    CONTACT,
    LICENSE,
)
from app.core.logging_config import LOGGING


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    summary=APP_SUMMARY,
    version=APP_VERSION,
    terms_of_service=TERMS_URL,
    contact=CONTACT,
    license_info=LICENSE,
    lifespan=lifespan,
)
# app = FastAPI(docs_url=None)

register_exception_handlers(app)
configure_security(app)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title="My API Docs",
#         swagger_favicon_url="/static/favicon.png",
#     )

app.state.limiter = limiter

app.include_router(shorturl_router)
app.include_router(admin_router)

logging.config.dictConfig(LOGGING)
