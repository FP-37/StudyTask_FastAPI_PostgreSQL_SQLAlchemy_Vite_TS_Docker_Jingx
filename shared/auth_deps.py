from dataclasses import dataclass
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from shared.jwt import decode_token

bearer = HTTPBearer(auto_error=False)

@dataclass(frozen=True)
class CurrentUser:
    id: int
    is_admin: bool

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> CurrentUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_token(credentials.credentials)
        sub = payload.get("sub")
        if not sub:
            raise ValueError("No sub")
        user_id = int(sub)
        is_admin = bool(payload.get("is_admin", False))
        return CurrentUser(id=user_id, is_admin=is_admin)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")