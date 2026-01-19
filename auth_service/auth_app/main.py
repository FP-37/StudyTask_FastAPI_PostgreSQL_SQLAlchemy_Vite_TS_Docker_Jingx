# Стандартный декоратор, чтобы хукнуть lifespan (startup/shutdown) через асинхронную функцию,
# Асинхронность нужна для ускорения общения сервера с клиентами.
from contextlib import asynccontextmanager
# Наш слоистый друг всего бэка: хранит роуты, middleware, настройки и lifespan
from fastapi import FastAPI
# Middleware даёт возможность нашему фронтенду общаться с несколькими ориджинами (схема + хост + порт)
# CORS - сопутствующий механизм браузера
from fastapi.middleware.cors import CORSMiddleware
# Функция инициализации базы данных
from auth_app.db.init_db import init_db
# Роутер - объект, объявляющий эндпоинты для логина и регистрации
from auth_app.api.auth import router as auth_router

# lifespan для FastAPI необязателен как факт, но подготавливает БД к работе ещё до факта запроса
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# Создаём объект приложения
# title/version параметры - для swagger'а
app = FastAPI(title="Auth Service", version="0.1.0", lifespan=lifespan)

# Разрешили список ориджинов фронта, учётные данные, любые CRUD методы и заголовки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Существование эндпоинтов аутентификации и регистрации
app.include_router(auth_router)

# Регистрация обработчика GET/health с возвратом статуса формата JSON-объекта
@app.get("/health")
def health():
    return {"status": "ok"}