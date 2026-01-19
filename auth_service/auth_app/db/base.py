# Импортируем базовый класс, который нужен для декларативного описания моделей
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass