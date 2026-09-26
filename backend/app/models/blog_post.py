from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    conteudo: Mapped[str | None] = mapped_column(Text)
    imagem_capa: Mapped[str | None] = mapped_column(String(500))
    publicado: Mapped[bool] = mapped_column(Boolean, default=False)
    data_publicacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
