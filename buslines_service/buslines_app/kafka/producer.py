import json
import os
from datetime import time

from kafka import KafkaProducer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "busline_events"

_producer: KafkaProducer | None = None


def _get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode(),
        )
    return _producer


def _serialize(obj):
    if isinstance(obj, time):
        return obj.strftime("%H:%M")
    return obj


def publish_event(event_type: str, data: dict) -> None:
    global _producer
    payload = {
        "event": event_type,
        "data": {k: _serialize(v) for k, v in data.items()},
    }
    try:
        _get_producer().send(TOPIC, payload)
    except Exception as exc:
        _producer = None
        print(f"[kafka] publish failed: {exc}")
