from sqlalchemy import select
from sqlalchemy.orm import Session

from buslines_app.models.outbox import OutboxEvent


class OutboxRepository:
    def __init__(self, db: Session):
        self.db = db

    def append(self, topic: str, event_type: str, payload: dict) -> OutboxEvent:
        event = OutboxEvent(topic=topic, event_type=event_type, payload=payload)
        self.db.add(event)
        return event

    def get_unpublished(self) -> list[OutboxEvent]:
        stmt = (
            select(OutboxEvent)
            .where(OutboxEvent.published == False)  # noqa: E712
            .order_by(OutboxEvent.id)
            .limit(100)
        )
        return list(self.db.execute(stmt).scalars().all())

    def mark_published(self, event: OutboxEvent) -> None:
        event.published = True
        self.db.add(event)
        self.db.commit()
