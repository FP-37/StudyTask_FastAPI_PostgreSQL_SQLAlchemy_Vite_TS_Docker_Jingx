from sqlalchemy import select
from sqlalchemy.orm import Session

from buslines_app.models.bus_line import BusLine
from buslines_app.schemas.bus_line import LineCreate, LineUpdate


class BusLineRepository:
    """Слой доступа к данным (SQLAlchemy)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: LineCreate, owner_id: int) -> BusLine:
        data = payload.model_dump()
        line = BusLine(**data, owner_id=owner_id)

        self.db.add(line)
        self.db.commit()
        self.db.refresh(line)
        return line

    def list(self, limit: int, offset: int) -> list[BusLine]:
        stmt = select(BusLine).order_by(BusLine.id).limit(limit).offset(offset)
        return list(self.db.execute(stmt).scalars().all())

    def get(self, line_id: int) -> BusLine | None:
        return self.db.get(BusLine, line_id)

    def update(self, line: BusLine, payload: LineUpdate) -> BusLine:
        data = payload.model_dump(exclude_unset=True)

        data.pop("owner_id", None)

        for key, value in data.items():
            setattr(line, key, value)

        self.db.commit()
        self.db.refresh(line)
        return line

    def delete(self, line: BusLine) -> None:
        self.db.delete(line)
        self.db.commit()