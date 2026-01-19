# APIRouter - объект группировки эндпоинтов в один модуль
# Depends - механизм "подсовывания" в функции наших объектов
# HTTPException - способ вернуть http-ошибку по коду с деталями
# status - набор констант HTTP-кодов
from fastapi import APIRouter, Depends, HTTPException, status
# Session - объект, ответственный за выполнение запросов к БД, реализует транзакции и кэширование
from sqlalchemy.orm import Session
# get_db - функция выдачи новых Session для каждого отдельного запроса
from auth_app.db.dependencies import get_db
# UserRepository реализует инкапсуляцию нашей CRUD для ORM
from auth_app.repositories.users import UserRepository
# Какие поля для логина, регистрации и токен туды-сюды
from auth_app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
# Безопасная отдача юзера без password hash
from auth_app.schemas.user import UserRead
# Формирование токена доступа
from auth_app.security.jwt import create_access_token
# Для хэширования и сравнения с хэшем
from auth_app.security.passwords import hash_password, verify_password
# чтение, валидация и поиск [по БД] пользователя
from auth_app.security.dependencies import get_current_user

# Реализация модульности формирования эндпоинтов
# Создаём роутер-объект, который по префиксу объявляет в адресе путь /auth для дальнейших эндпоинтов
# tags-параметр - указание для группировки в Swagger
router = APIRouter(prefix="/auth", tags=["auth"])

# Регистрация эндпоинта /register
# response_model валидирует ответ по нашей схеме учётных данных
@router.post("/register", response_model=UserRead)
def register(payload: RegisterRequest, db: Session = Depends(get_db)): # payload парсит через pydantic-модель
    repo = UserRepository(db) # репозиторий для работы с БД через методы
    if repo.get_by_username(payload.username) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user = repo.create(
        username=payload.username,
        password_hash=hash_password(payload.password), # не храним пароль как текст, сразу хэшируем
        is_admin=False,
    )
    return user

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_username(payload.username)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    # expires_minutes - параметр жизни логина
    token = create_access_token(user_id=user.id, is_admin=user.is_admin, expires_minutes=60)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserRead)
def me(current_user=Depends(get_current_user)):
    return current_user