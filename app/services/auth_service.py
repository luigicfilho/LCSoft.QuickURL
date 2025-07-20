import jwt
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core import settings

security = HTTPBearer()


class AuthService:
    @staticmethod
    def create_admin_token() -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": "admin",
            "jti": str(uuid.uuid4()),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(hours=12)).timestamp()),
            "aud": "lcsoft-admin",
            "iss": "lcsoft-auth-service",
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
        return token

    @staticmethod
    def verify_admin_token(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):
        try:
            payload = jwt.decode(
                credentials.credentials,
                settings.jwt_secret,
                algorithms=["HS256"],
                audience="lcsoft-admin",
                issuer="lcsoft-auth-service",
            )

            if payload.get("sub") != "admin":
                raise HTTPException(status_code=403, detail="Invalid admin token")

            if "jti" not in payload or not payload["jti"]:
                raise HTTPException(status_code=403, detail="Missing token ID (jti)")

            if "iat" not in payload or not isinstance(payload["iat"], int):
                raise HTTPException(
                    status_code=403, detail="Invalid issued-at claim (iat)"
                )

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidAudienceError:
            raise HTTPException(status_code=403, detail="Invalid token audience")
        except jwt.InvalidIssuerError:
            raise HTTPException(status_code=403, detail="Invalid token issuer")
        except jwt.PyJWTError:
            raise HTTPException(status_code=403, detail="Invalid token")
