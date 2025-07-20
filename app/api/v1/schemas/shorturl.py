from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime
from typing import Optional


class URLCreate(BaseModel):
    target_url: HttpUrl
    expires_in_days: Optional[int] = None

    @validator("expires_in_days")
    def max_expiration(cls, v):
        if v is not None and (v <= 0 or v > 365):
            raise ValueError("Expiration must be between 1 and 365 days")
        return v


class URLInfo(BaseModel):
    code: str
    target_url: str
    created_at: datetime
    expires_at: Optional[datetime]
    clicks: int
