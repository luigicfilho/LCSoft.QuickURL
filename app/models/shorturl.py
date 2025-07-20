from datetime import datetime, timezone
from tortoise import fields
from tortoise.models import Model


class ShortURL(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=10, unique=True)
    target_url = fields.CharField(max_length=500)
    created_at = fields.DatetimeField(auto_now_add=True)
    expires_at = fields.DatetimeField(null=True)
    clicks = fields.IntField(default=0)

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at
