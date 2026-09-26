from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get("/{id}", response_model=CategoryOut)
def get_category(id: int, db: Session = Depends(get_db)):
    cat = db.get(Category, id)
    if not cat:
        raise HTTPException(404, "Categoria não encontrada")
    return cat


@router.post("/", response_model=CategoryOut, status_code=201, dependencies=[Depends(get_current_user)])
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    cat = Category(nome=payload.nome)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.patch("/{id}", response_model=CategoryOut, dependencies=[Depends(get_current_user)])
def update_category(id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    cat = db.get(Category, id)
    if not cat:
        raise HTTPException(404, "Categoria não encontrada")
    if payload.nome is not None:
        cat.nome = payload.nome
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{id}", status_code=204, dependencies=[Depends(get_current_user)])
def delete_category(id: int, db: Session = Depends(get_db)):
    cat = db.get(Category, id)
    if not cat:
        raise HTTPException(404, "Categoria não encontrada")
    db.delete(cat)
    db.commit()
