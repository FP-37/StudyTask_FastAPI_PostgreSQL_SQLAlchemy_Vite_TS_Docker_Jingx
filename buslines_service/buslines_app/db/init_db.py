from buslines_app.db.session import engine
from buslines_app.db.base import Base

from buslines_app.models.bus_line import BusLine  # noqa: F401

def init_db() -> None:
    Base.metadata.create_all(bind=engine)