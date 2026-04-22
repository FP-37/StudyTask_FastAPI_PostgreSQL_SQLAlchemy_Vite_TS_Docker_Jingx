import io
import json
import os
import struct

import fastavro
import requests

SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://schema_registry:8081")

SAGA_EVENT_SCHEMA = {
    "type": "record",
    "name": "BusSagaEvent",
    "namespace": "buslines",
    "fields": [
        {"name": "event", "type": "string"},
        {"name": "data", "type": {"type": "map", "values": "string"}},
    ],
}

_schema_id_cache: dict[str, int] = {}


def _register_schema(subject: str, schema: dict) -> int:
    if subject in _schema_id_cache:
        return _schema_id_cache[subject]
    resp = requests.post(
        f"{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions",
        headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        json={"schema": json.dumps(schema)},
        timeout=10,
    )
    resp.raise_for_status()
    schema_id = resp.json()["id"]
    _schema_id_cache[subject] = schema_id
    return schema_id


def _get_schema_by_id(schema_id: int) -> dict:
    resp = requests.get(f"{SCHEMA_REGISTRY_URL}/schemas/ids/{schema_id}", timeout=10)
    resp.raise_for_status()
    return json.loads(resp.json()["schema"])


def avro_serialize(subject: str, schema: dict, record: dict) -> bytes:
    schema_id = _register_schema(subject, schema)
    parsed = fastavro.parse_schema(schema)
    buf = io.BytesIO()
    buf.write(b"\x00")
    buf.write(struct.pack(">I", schema_id))
    fastavro.schemaless_writer(buf, parsed, record)
    return buf.getvalue()


def avro_deserialize(data: bytes) -> dict:
    schema_id = struct.unpack(">I", data[1:5])[0]
    schema = _get_schema_by_id(schema_id)
    parsed = fastavro.parse_schema(schema)
    buf = io.BytesIO(data[5:])
    return fastavro.schemaless_reader(buf, parsed)
