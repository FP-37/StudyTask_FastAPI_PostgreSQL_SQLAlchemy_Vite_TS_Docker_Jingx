from sqlalchemy import Integer, String, JSON, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from buslines_app.db.base import Base


class OutboxEvent(Base):
    __tablename__ = "outbox"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    topic: Mapped[str] = mapped_column(String(128), nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
