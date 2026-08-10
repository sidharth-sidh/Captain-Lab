from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Computer
from ..schemas import ComputerHeartbeat, ComputerRegister, ComputerResponse


router = APIRouter(prefix="/api/computers", tags=["computers"])
HEARTBEAT_TIMEOUT_SECONDS = 20


def mark_stale_computers(db: Session) -> None:
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=HEARTBEAT_TIMEOUT_SECONDS)
    stale = db.scalars(
        select(Computer).where(Computer.status == "online", Computer.last_seen < cutoff)
    ).all()
    if stale:
        for computer in stale:
            computer.status = "offline"
        db.commit()


@router.get("", response_model=list[ComputerResponse])
def list_computers(db: Session = Depends(get_db)) -> list[Computer]:
    mark_stale_computers(db)
    return list(db.scalars(select(Computer).order_by(Computer.id)).all())


@router.get("/{computer_id}", response_model=ComputerResponse)
def get_computer(computer_id: int, db: Session = Depends(get_db)) -> Computer:
    mark_stale_computers(db)
    computer = db.get(Computer, computer_id)
    if computer is None:
        raise HTTPException(status_code=404, detail="Computer not found")
    return computer


@router.post("/register", response_model=ComputerResponse, status_code=status.HTTP_201_CREATED)
def register_computer(payload: ComputerRegister, db: Session = Depends(get_db)) -> Computer:
    computer = Computer(**payload.model_dump(), status="offline")
    db.add(computer)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A computer with this name or hostname already exists")
    db.refresh(computer)
    return computer


@router.post("/{computer_id}/heartbeat", response_model=ComputerResponse)
def heartbeat(computer_id: int, payload: ComputerHeartbeat, db: Session = Depends(get_db)) -> Computer:
    computer = db.get(Computer, computer_id)
    if computer is None:
        raise HTTPException(status_code=404, detail="Computer not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(computer, field, value)
    computer.status = "online"
    computer.last_seen = datetime.now(timezone.utc)
    db.commit()
    db.refresh(computer)
    return computer


@router.delete("/{computer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_computer(computer_id: int, db: Session = Depends(get_db)) -> None:
    computer = db.get(Computer, computer_id)
    if computer is None:
        raise HTTPException(status_code=404, detail="Computer not found")
    db.delete(computer)
    db.commit()
