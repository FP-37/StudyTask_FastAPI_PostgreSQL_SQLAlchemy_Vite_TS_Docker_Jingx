from auth_app.db.session import engine
from auth_app.db.base import Base

from auth_app.models.user import User  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
