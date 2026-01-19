from auth_app.db.session import engine
from auth_app.db.base import Base

# Регистрируем модель в Base.metadata, но не применяем напрямую
# Влияет на знание о существовании модели как таковой
from auth_app.models.user import User  # noqa: F401

def init_db() -> None:
    Base.metadata.create_all(bind=engine)