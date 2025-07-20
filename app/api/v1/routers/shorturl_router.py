from fastapi import APIRouter, HTTPException, Request
from app.services import ShortURLService
from app.api.v1.schemas import URLCreate, URLInfo
from app.core.extensions import limiter
from app.core import settings
from starlette.responses import RedirectResponse

router = APIRouter(prefix="/api/v1/urls", tags=["URLs"])

shared_limit = limiter.shared_limit(settings.shorturl_default_limit, scope="user")


@router.post("/shorten", response_model=URLInfo, summary="Create a short URL")
@shared_limit
async def create_url(request: Request, data: URLCreate):
    return await ShortURLService.create_url(data)


@router.get("/{code}", summary="Redirect to the URL")
@shared_limit
async def redirect(request: Request, code: str):
    target_url = await ShortURLService.get_url_by_code(code)
    if not target_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=target_url)
