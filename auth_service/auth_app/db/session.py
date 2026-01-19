# os в данном случае для чтения переменных окружения (getenv)
import os
# Создание объекта для управления низкоуровневым доступом
from sqlalchemy import create_engine
# Вызываем как функцию для создания нашего session-объекта
from sqlalchemy.orm import sessionmaker

# Берёт переменную окружения DATABASE_URL, а если её нет — использует значение по умолчанию
# Через Docker реализовали подключение PosgreSQL, но по умолчанию берём SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine, #привязываем объект к engine
    autoflush=False,
    autocommit=False,
)
