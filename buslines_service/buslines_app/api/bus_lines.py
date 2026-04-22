from datetime import time

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from buslines_app.db.dependencies import get_db
from buslines_app.schemas.bus_line import LineCreate, LineUpdate, LineRead
from buslines_app.repositories.bus_line_repository import BusLineRepository
from buslines_app.repositories.bus_line_event_repository import BusLineEventRepository, replay
from buslines_app.repositories.outbox_repository import OutboxRepository
from shared.auth_deps import get_current_user

TOPIC = "busline_events"

router = APIRouter(prefix="/bus-lines", tags=["bus-lines"])


def _can_modify(current_user, line) -> bool:
    return bool(getattr(current_user, "is_admin", False)) or (line.owner_id == current_user.id)


def _serialize(obj):
    if isinstance(obj, time):
        return obj.strftime("%H:%M")
    return obj


def _line_dict(line) -> dict:
    return {
        "id": line.id,
        "line_number": line.line_number,
        "depot_number": line.depot_number,
        "start_time": _serialize(line.start_time),
        "end_time": _serialize(line.end_time),
        "length_km": line.length_km,
        "owner_id": line.owner_id,
    }


@router.post("", response_model=LineRead, status_code=status.HTTP_201_CREATED)
def create_line(
    payload: LineCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    line = BusLineRepository(db).create(payload, owner_id=current_user.id)
    data = _line_dict(line)
    BusLineEventRepository(db).append(line.id, "BusLineCreated", data)
    OutboxRepository(db).append(TOPIC, "BusLineCreated", data)
    db.commit()
    return line


@router.get("", response_model=list[LineRead])
def list_lines(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return BusLineRepository(db).list(limit=limit, offset=offset)


@router.get("/{line_id}", response_model=LineRead)
def get_line(line_id: int, db: Session = Depends(get_db)):
    line = BusLineRepository(db).get(line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return line


@router.get("/{line_id}/replay", tags=["event-sourcing"])
def replay_line(line_id: int, db: Session = Depends(get_db)):
    events = BusLineEventRepository(db).get_events(line_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this id")
    state = replay(events)
    return {
        "aggregate_id": line_id,
        "state": state,
        "events": [
            {"id": e.id, "event_type": e.event_type, "payload": e.payload, "occurred_at": e.occurred_at}
            for e in events
        ],
    }


@router.put("/{line_id}", response_model=LineRead)
def update_line(
    line_id: int,
    payload: LineUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = BusLineRepository(db)
    line = repo.get(line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    if not _can_modify(current_user, line):
        raise HTTPException(status_code=403, detail="Forbidden")

    line = repo.update(line, payload)
    data = _line_dict(line)
    BusLineEventRepository(db).append(line.id, "BusLineUpdated", data)
    OutboxRepository(db).append(TOPIC, "BusLineUpdated", data)
    db.commit()
    return line


@router.delete("/{line_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_line(
    line_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = BusLineRepository(db)
    line = repo.get(line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    if not _can_modify(current_user, line):
        raise HTTPException(status_code=403, detail="Forbidden")

    data = {"id": line.id, "line_number": line.line_number}
    BusLineEventRepository(db).append(line.id, "BusLineDeleted", data)
    OutboxRepository(db).append(TOPIC, "BusLineDeleted", data)
    repo.delete(line)
    db.commit()
    return None
