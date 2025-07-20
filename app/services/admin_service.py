import logging
from app.models import ShortURL

logger = logging.getLogger("admin_actions")


class AdminService:

    @staticmethod
    async def delete_url_by_code(code: str) -> bool:
        url = await ShortURL.get_or_none(code=code)
        if not url:
            return False
        await url.delete()
        logger.info(f"[ADMIN] Deleted URL with code: {code}")
        return True

    @staticmethod
    async def get_url_stats(code: str) -> dict | None:
        url = await ShortURL.get_or_none(code=code)
        if not url:
            return None
        logger.info(f"[ADMIN] Retrieved stats for URL with code: {code}")
        return {
            "code": url.code,
            "target_url": url.target_url,
            "created_at": url.created_at,
            "expires_at": url.expires_at,
            "clicks": url.clicks,
        }
