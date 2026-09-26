from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[list[Product]] = relationship("Product", back_populates="category")


from app.models.product import Product  # noqa: E402 — resolve forward ref
