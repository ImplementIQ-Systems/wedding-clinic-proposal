from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingOut, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    booking = Booking(**payload.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/", response_model=list[BookingOut], dependencies=[Depends(get_current_user)])
def list_bookings(
    status: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Booking).order_by(Booking.data_hora)
    if status:
        q = q.filter(Booking.status == status)
    return q.all()


@router.get("/{id}", response_model=BookingOut, dependencies=[Depends(get_current_user)])
def get_booking(id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, id)
    if not booking:
        raise HTTPException(404, "Marcação não encontrada")
    return booking


@router.patch("/{id}", response_model=BookingOut, dependencies=[Depends(get_current_user)])
def update_booking(id: int, payload: BookingUpdate, db: Session = Depends(get_db)):
    booking = db.get(Booking, id)
    if not booking:
        raise HTTPException(404, "Marcação não encontrada")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(booking, field, value)
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{id}", status_code=204, dependencies=[Depends(get_current_user)])
def delete_booking(id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, id)
    if not booking:
        raise HTTPException(404, "Marcação não encontrada")
    db.delete(booking)
    db.commit()
