from pydantic import BaseModel


class CategoryCreate(BaseModel):
    nome: str


class CategoryUpdate(BaseModel):
    nome: str | None = None


class CategoryOut(BaseModel):
    id: int
    nome: str

    model_config = {"from_attributes": True}
