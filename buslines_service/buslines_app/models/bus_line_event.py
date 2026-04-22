from sqlalchemy import Integer, String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from buslines_app.db.base import Base


class BusLineEvent(Base):
    __tablename__ = "busline_event_store"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    aggregate_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
