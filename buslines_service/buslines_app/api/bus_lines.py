from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from buslines_app.db.dependencies import get_db
from buslines_app.schemas.bus_line import LineCreate, LineUpdate, LineRead
from buslines_app.repositories.bus_line_repository import BusLineRepository
from shared.auth_deps import get_current_user

router = APIRouter(prefix="/bus-lines", tags=["bus-lines"])


def _can_modify(current_user, line) -> bool:
    return bool(getattr(current_user, "is_admin", False)) or (line.owner_id == current_user.id)


@router.post("", response_model=LineRead, status_code=status.HTTP_201_CREATED)
def create_line(
    payload: LineCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = BusLineRepository(db)
    return repo.create(payload, owner_id=current_user.id)


@router.get("", response_model=list[LineRead])
def list_lines(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    repo = BusLineRepository(db)
    return repo.list(limit=limit, offset=offset)


@router.get("/{line_id}", response_model=LineRead)
def get_line(line_id: int, db: Session = Depends(get_db)):
    repo = BusLineRepository(db)
    line = repo.get(line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return line


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

    return repo.update(line, payload)


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

    repo.delete(line)
    return None
