from sqlalchemy import Integer, Float, Time
from sqlalchemy.orm import Mapped, mapped_column
from datetime import time

from buslines_app.db.base import Base

class BusLine(Base):
    __tablename__ = "bus_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # номер маршрута
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # номер парка
    depot_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # время начала движения
    start_time: Mapped[time] = mapped_column(Time, nullable=False)

    # время окончания движения
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    # длина маршрута в км
    length_km: Mapped[float] = mapped_column(Float, nullable=False)

    # владелец (id пользователя из auth_service)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)