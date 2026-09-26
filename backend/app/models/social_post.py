from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SocialPost(Base):
    __tablename__ = "social_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), nullable=True)
    imagem_url: Mapped[str | None] = mapped_column(String(500))
    legenda: Mapped[str | None] = mapped_column(String(2200))
    # ex: ["instagram", "facebook"]
    plataformas: Mapped[list | None] = mapped_column(JSON)
    # ex: {"instagram": "buf_xxx", "facebook": "buf_yyy"}
    buffer_ids: Mapped[dict | None] = mapped_column(JSON)
    # ex: {"instagram": "success", "facebook": "error"}
    status: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
