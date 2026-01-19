import os
from jose import JWTError, jwt

ALGORITHM = "HS256"

def _secret() -> str:
    key = os.getenv("JWT_SECRET_KEY")
    if not key:
        raise RuntimeError("JWT_SECRET_KEY is not set")
    return key

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, _secret(), algorithms=[ALGORITHM])
    except JWTError as e:
        raise ValueError("Invalid token") from e