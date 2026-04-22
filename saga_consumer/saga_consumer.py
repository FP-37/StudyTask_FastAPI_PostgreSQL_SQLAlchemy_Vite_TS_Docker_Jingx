import json
import os

from kafka import KafkaConsumer, KafkaProducer
from sqlalchemy import create_engine, text

from schema_registry import avro_serialize, SAGA_EVENT_SCHEMA

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
EVENTS_TOPIC = "busline_events"
SAGA_TOPIC = "busline_saga"
SAGA_SUBJECT = "busline_saga-value"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://bus_user:bus_pass@postgres_buslines:5432/buslines_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
)


def _publish_saga(event_type: str, data: dict) -> None:
    str_data = {k: str(v) for k, v in data.items()}
    raw = avro_serialize(SAGA_SUBJECT, SAGA_EVENT_SCHEMA, {"event": event_type, "data": str_data})
    producer.send(SAGA_TOPIC, raw)


def _check_duplicate(line_id: int, line_number: int, depot_number: int) -> bool:
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT id FROM bus_lines "
                "WHERE line_number = :ln AND depot_number = :dn AND id != :lid"
            ),
            {"ln": line_number, "dn": depot_number, "lid": line_id},
        ).fetchone()
    return row is not None


def _delete_line(line_id: int) -> None:
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM bus_lines WHERE id = :id"), {"id": line_id})
        conn.execute(
            text("DELETE FROM busline_event_store WHERE aggregate_id = :id"),
            {"id": line_id},
        )
        conn.commit()


def main():
    consumer = KafkaConsumer(
        EVENTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda m: json.loads(m.decode()),
        group_id="saga_consumer",
        auto_offset_reset="earliest",
    )
    print(f"[saga_consumer] listening on {EVENTS_TOPIC}...")

    for msg in consumer:
        event = msg.value
        if event.get("event") != "BusLineCreated":
            continue

        data = event["data"]
        line_id = data["id"]
        line_number = data["line_number"]
        depot_number = data["depot_number"]

        if _check_duplicate(line_id, line_number, depot_number):
            _delete_line(line_id)
            _publish_saga("BusLineRejected", {
                "id": str(line_id),
                "reason": f"line_number={line_number} already exists in depot={depot_number}",
            })
            print(f"[saga] REJECTED line_id={line_id}: duplicate in depot {depot_number}")
        else:
            _publish_saga("BusLineApproved", {"id": str(line_id)})
            print(f"[saga] APPROVED line_id={line_id}")


if __name__ == "__main__":
    main()
