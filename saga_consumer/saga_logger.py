import os

from kafka import KafkaConsumer

from schema_registry import avro_deserialize

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
SAGA_TOPIC = "busline_saga"


def main():
    consumer = KafkaConsumer(
        SAGA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="saga_logger",
        auto_offset_reset="earliest",
    )
    print(f"[saga_logger] listening on {SAGA_TOPIC}...")
    for msg in consumer:
        try:
            event = avro_deserialize(msg.value)
            print(f"[SAGA RESULT] {event['event']}: {event['data']}")
        except Exception as exc:
            print(f"[saga_logger] deserialize error: {exc}")


if __name__ == "__main__":
    main()
