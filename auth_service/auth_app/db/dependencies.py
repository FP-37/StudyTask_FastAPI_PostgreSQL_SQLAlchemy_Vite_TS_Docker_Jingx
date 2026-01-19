# Будем явно аннотировать тип нашей функции как генераторной
from typing import Generator
from sqlalchemy.orm import Session
# SessionLocal - объект-фабрика
from auth_app.db.session import SessionLocal

# Отдаём через yield наш Session, ничего не возвращаем в генератор, без return
# Выше - всё также про типизацию
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()