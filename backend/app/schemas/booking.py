from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.booking import BookingStatus


class BookingCreate(BaseModel):
    nome_cliente: str
    telefone: str | None = None
    email: EmailStr | None = None
    product_id: int | None = None
    data_hora: datetime
    notas: str | None = None


class BookingUpdate(BaseModel):
    nome_cliente: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None
    product_id: int | None = None
    data_hora: datetime | None = None
    status: BookingStatus | None = None
    notas: str | None = None


class BookingOut(BaseModel):
    id: int
    nome_cliente: str
    telefone: str | None
    email: str | None
    product_id: int | None
    data_hora: datetime
    status: BookingStatus
    notas: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
