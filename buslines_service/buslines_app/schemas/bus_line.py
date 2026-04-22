from datetime import time
import re

from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator

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
    line_number: int = Field(..., gt=0)
    depot_number: int = Field(..., gt=0)
    start_time: time = Field(...)
    end_time: time = Field(...)
    length_km: float = Field(..., gt=0)

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_time(cls, v):
        if isinstance(v, time):
            return v
        if isinstance(v, str):
            return _parse_time_hhmm(v)
        raise ValueError("invalid time value")

    @model_validator(mode="after")
    def check_time_order(self):
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
        if self.start_time is not None and self.end_time is not None:
            if self.start_time >= self.end_time:
                raise ValueError("start_time must be earlier than end_time")
        return self


class LineRead(LineBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
