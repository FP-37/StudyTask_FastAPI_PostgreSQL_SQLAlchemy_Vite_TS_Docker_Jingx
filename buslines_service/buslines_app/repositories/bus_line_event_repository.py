from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from buslines_app.models.bus_line_event import BusLineEvent


class BusLineEventRepository:
    def __init__(self, db: Session):
        self.db = db

    def append(self, aggregate_id: int, event_type: str, payload: dict) -> BusLineEvent:
        event = BusLineEvent(
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=payload,
            occurred_at=datetime.utcnow(),
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_events(self, aggregate_id: int) -> list[BusLineEvent]:
        stmt = (
            select(BusLineEvent)
            .where(BusLineEvent.aggregate_id == aggregate_id)
            .order_by(BusLineEvent.id)
        )
        return list(self.db.execute(stmt).scalars().all())


def replay(events: list[BusLineEvent]) -> dict | None:
    state = None
    for event in events:
        if event.event_type == "BusLineCreated":
            state = dict(event.payload)
        elif event.event_type == "BusLineUpdated" and state is not None:
            state.update(event.payload)
        elif event.event_type == "BusLineDeleted":
            state = None
    return state
