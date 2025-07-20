import secrets
import logging
from datetime import datetime, timedelta
from tortoise.exceptions import IntegrityError
from app.models import ShortURL
from app.api.v1.schemas import URLCreate, URLInfo
from app.core import settings

logger = logging.getLogger("shorturl_service")


class ShortURLService:

    @staticmethod
    async def create_url(data: URLCreate) -> URLInfo:
        retries = settings.shorturl_max_retries
        attempt = 0
        expires_at = None

        if data.expires_in_days is not None:
            expires_at = datetime.utcnow() + timedelta(days=data.expires_in_days)
        else:
            expires_at = datetime.utcnow() + timedelta(
                days=settings.default_expiration_days
            )

        while attempt < retries:
            code = secrets.token_urlsafe(4)[:6]
            try:
                short_url = await ShortURL.create(
                    code=code, target_url=data.target_url, expires_at=expires_at
                )
                return URLInfo(
                    code=short_url.code,
                    target_url=short_url.target_url,
                    created_at=short_url.created_at,
                    expires_at=short_url.expires_at,
                    clicks=short_url.clicks,
                )
            except IntegrityError:
                logger.warning(
                    f"Attempt {attempt+1}/{retries}: Code {code} already exists. Retrying..."
                )
                attempt += 1

        logger.error(
            f"Failed to generate unique code after {retries} attempts for URL: {data.target_url}"
        )
        raise Exception(
            f"Failed to generate unique short code after {retries} attempts"
        )

    @staticmethod
    async def get_url_by_code(code: str) -> str | None:
        short_url = await ShortURL.get_or_none(code=code)
        if not short_url:
            return None
        if short_url.is_expired():
            return None

        short_url.clicks += 1
        await short_url.save()
        return short_url.target_url

    @staticmethod
    async def list_urls() -> list[URLInfo]:
        urls = await ShortURL.all()
        return [
            URLInfo(
                code=u.code,
                target_url=u.target_url,
                created_at=u.created_at,
                expires_at=u.expires_at,
                clicks=u.clicks,
            )
            for u in urls
        ]
