import json
import time
import threading

from kafka import KafkaProducer

from buslines_app.db.session import SessionLocal
from buslines_app.repositories.outbox_repository import OutboxRepository

import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

_producer: KafkaProducer | None = None


def _get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode(),
        )
    return _producer


def _relay_once() -> None:
    global _producer
    db = SessionLocal()
    try:
        repo = OutboxRepository(db)
        events = repo.get_unpublished()
        for event in events:
            payload = {"event": event.event_type, "data": event.payload}
            try:
                _get_producer().send(event.topic, payload)
                repo.mark_published(event)
            except Exception as exc:
                _producer = None
                print(f"[outbox_relay] send failed: {exc}")
                break
    finally:
        db.close()


def run_relay() -> None:
    print("[outbox_relay] started")
    while True:
        try:
            _relay_once()
        except Exception as exc:
            print(f"[outbox_relay] error: {exc}")
        time.sleep(1)


def start_relay() -> None:
    t = threading.Thread(target=run_relay, daemon=True)
    t.start()
