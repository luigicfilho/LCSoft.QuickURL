from fastapi import APIRouter, Depends, HTTPException, Request
from app.services.auth_service import AuthService
from app.services import ShortURLService
from app.api.v1.schemas import URLInfo
from app.core.extensions import limiter
from app.core import settings
from app.services.admin_service import AdminService

arouter = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@arouter.get("/urls", response_model=list[URLInfo], summary="List all URLs (Admin)")
@limiter.limit(settings.admin_list_urls_limit)
async def list_all_urls(
    request: Request, admin=Depends(AuthService.verify_admin_token)
):
    return await ShortURLService.list_urls()


@arouter.delete("/urls/{code}", summary="Remove URL by code (Admin)")
@limiter.limit(settings.admin_delete_url_limit)
async def delete_url(
    request: Request, code: str, admin=Depends(AuthService.verify_admin_token)
):
    success = await AdminService.delete_url_by_code(code)
    if not success:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"detail": f"URL with code {code} deleted"}


@arouter.get("/stats/{code}", summary="Get estatistics of a URL (Admin)")
@limiter.limit(settings.admin_stats_limit)
async def url_stats(
    request: Request, code: str, admin=Depends(AuthService.verify_admin_token)
):
    stats = await AdminService.get_url_stats(code)
    if not stats:
        raise HTTPException(status_code=404, detail="URL not found")
    return stats
