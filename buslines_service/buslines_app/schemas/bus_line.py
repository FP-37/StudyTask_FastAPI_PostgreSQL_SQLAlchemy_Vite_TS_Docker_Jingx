from datetime import time
import re

from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator

"""
Валидация данных через библиотеку Pydantic.
Троеточие делает поле обязательным, None - необязательным.
Значения параметров: gt - >, ge - >=, lt - <, le - <=.
"""

_TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})$")


def _parse_time_hhmm(v: str) -> time:
    s = v.strip()
    m = _TIME_RE.match(s)
    if not m:
        raise ValueError("time must be in H:MM or HH:MM format")

    h = int(m.group(1))
    mm = int(m.group(2))

    if not (0 <= h <= 23):
        raise ValueError("hour must be in 0..23")
    if not (0 <= mm <= 59):
        raise ValueError("minute must be in 0..59")

    return time(hour=h, minute=mm)


class LineBase(BaseModel):
    line_number: int = Field(..., gt=0, description="Номер маршрута (положительное число)")
    depot_number: int = Field(..., gt=0, description="Номер парка (положительное число)")
    start_time: time = Field(..., description="Время начала движения (H:MM или HH:MM)")
    end_time: time = Field(..., description="Время окончания движения (H:MM или HH:MM)")
    length_km: float = Field(..., gt=0, description="Длина маршрута в км (положительное число)")

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_time(cls, v):
        # Уже time — не трогаем
        if isinstance(v, time):
            return v
        # Пришло строкой — парсим H:MM / HH:MM
        if isinstance(v, str):
            return _parse_time_hhmm(v)
        raise ValueError("invalid time value")

    # model_validator применяем в случае необходимости нескольких проверок одновеменно.
    # Значение параметра mode задаёт условие проверки - в данном случае после прочтения данных и преобразования.
    @model_validator(mode="after")
    def check_time_order(self):
        # Проверяем порядок времени
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be earlier than end_time")
        return self


class LineCreate(LineBase):
    pass


class LineUpdate(BaseModel):
    line_number: int | None = Field(None, gt=0)
    depot_number: int | None = Field(None, gt=0)
    start_time: time | None = None
    end_time: time | None = None
    length_km: float | None = Field(None, gt=0)

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_time(cls, v):
        if v is None:
            return None
        if isinstance(v, time):
            return v
        if isinstance(v, str):
            return _parse_time_hhmm(v)
        raise ValueError("invalid time value")

    @model_validator(mode="after")
    def check_time_order(self):
        # Для update проверяем время только если оба значения переданы
        if self.start_time is not None and self.end_time is not None:
            if self.start_time >= self.end_time:
                raise ValueError("start_time must be earlier than end_time")
        return self


class LineRead(LineBase):
    id: int
    owner_id: int
    # Создание ответной схемы из ORM-объекта SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
