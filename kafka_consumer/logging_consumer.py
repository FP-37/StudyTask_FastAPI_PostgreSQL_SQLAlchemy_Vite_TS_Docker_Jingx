import json
import os
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "busline_events"


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda m: json.loads(m.decode()),
        group_id="logging_consumer",
        auto_offset_reset="earliest",
    )
    print(f"[logging_consumer] listening on {TOPIC}...")
    for msg in consumer:
        event = msg.value
        print(f"[EVENT] {event['event']}: {event['data']}")


if __name__ == "__main__":
    main()
