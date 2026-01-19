import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

ALGORITHM = "HS256"

def _secret() -> str:
    key = os.getenv("JWT_SECRET_KEY")
    if not key:
        raise RuntimeError("JWT_SECRET_KEY is not set")
    return key

def create_access_token(user_id: int, is_admin: bool, expires_minutes: int = 60) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_minutes)

    payload = {
        "sub": str(user_id),
        "is_admin": bool(is_admin),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, _secret(), algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, _secret(), algorithms=[ALGORITHM])
    except JWTError as e:
        raise ValueError("Invalid token") from e
