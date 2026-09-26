import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BookingStatus(str, enum.Enum):
    pendente = "pendente"
    confirmada = "confirmada"
    cancelada = "cancelada"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_cliente: Mapped[str] = mapped_column(String(255), nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(255))
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), nullable=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus), default=BookingStatus.pendente
    )
    notas: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
