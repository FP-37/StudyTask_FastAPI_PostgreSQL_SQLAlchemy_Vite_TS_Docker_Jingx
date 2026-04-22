from sqlalchemy import Integer, Float, Time
from sqlalchemy.orm import Mapped, mapped_column
from datetime import time

from buslines_app.db.base import Base


class BusLine(Base):
    __tablename__ = "bus_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    depot_number: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    length_km: Mapped[float] = mapped_column(Float, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
