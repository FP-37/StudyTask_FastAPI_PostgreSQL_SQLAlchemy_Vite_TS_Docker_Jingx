from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_app.db.dependencies import get_db
from auth_app.repositories.users import UserRepository
from auth_app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from auth_app.schemas.user import UserRead
from auth_app.security.jwt import create_access_token
from auth_app.security.passwords import hash_password, verify_password
from auth_app.security.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_by_username(payload.username) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = repo.create(
        username=payload.username,
        password_hash=hash_password(payload.password),
        is_admin=False,
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_username(payload.username)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    token = create_access_token(user_id=user.id, is_admin=user.is_admin, expires_minutes=60)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user=Depends(get_current_user)):
    return current_user
