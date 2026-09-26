from datetime import datetime

from pydantic import BaseModel


class ProductImageOut(BaseModel):
    id: int
    url: str
    ordem: int
    capa: bool

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    nome: str
    descricao: str | None = None
    category_id: int | None = None
    sku: str | None = None
    disponivel: bool = True


class ProductUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    category_id: int | None = None
    sku: str | None = None
    disponivel: bool | None = None


class ProductOut(BaseModel):
    id: int
    nome: str
    descricao: str | None
    category_id: int | None
    sku: str | None
    disponivel: bool
    created_at: datetime
    updated_at: datetime
    images: list[ProductImageOut] = []

    model_config = {"from_attributes": True}
