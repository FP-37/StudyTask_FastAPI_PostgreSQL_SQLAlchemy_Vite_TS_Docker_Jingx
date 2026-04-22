import json
import os
from datetime import datetime

from kafka import KafkaConsumer
from sqlalchemy import create_engine, text

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "busline_events"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://bus_user:bus_pass@postgres_buslines:5432/buslines_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS busline_event_log (
    id          SERIAL PRIMARY KEY,
    event_type  VARCHAR(64) NOT NULL,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
"""


def main():
    with engine.connect() as conn:
        conn.execute(text(CREATE_TABLE))
        conn.commit()

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda m: json.loads(m.decode()),
        group_id="db_consumer",
        auto_offset_reset="earliest",
    )
    print(f"[db_consumer] listening on {TOPIC}...")
    for msg in consumer:
        event = msg.value
        with engine.connect() as conn:
            conn.execute(
                text(
                    "INSERT INTO busline_event_log (event_type, payload, created_at) "
                    "VALUES (:event_type, :payload, :created_at)"
                ),
                {
                    "event_type": event["event"],
                    "payload": json.dumps(event["data"]),
                    "created_at": datetime.utcnow(),
                },
            )
            conn.commit()
        print(f"[db_consumer] saved {event['event']} id={event['data'].get('id')}")


if __name__ == "__main__":
    main()
