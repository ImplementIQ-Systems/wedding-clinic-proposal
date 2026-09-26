from datetime import datetime

from pydantic import BaseModel


class BlogPostCreate(BaseModel):
    titulo: str
    slug: str | None = None  # gerado automaticamente se omitido
    conteudo: str | None = None
    imagem_capa: str | None = None
    publicado: bool = False
    data_publicacao: datetime | None = None


class BlogPostUpdate(BaseModel):
    titulo: str | None = None
    conteudo: str | None = None
    imagem_capa: str | None = None
    publicado: bool | None = None
    data_publicacao: datetime | None = None


class BlogPostImport(BaseModel):
    titulo: str
    slug: str  # obrigatório no import — slug exacto do Wix
    conteudo: str | None = None
    imagem_capa: str | None = None
    publicado: bool = True
    data_publicacao: datetime | None = None


class BlogPostOut(BaseModel):
    id: int
    titulo: str
    slug: str
    conteudo: str | None
    imagem_capa: str | None
    publicado: bool
    data_publicacao: datetime | None

    model_config = {"from_attributes": True}
