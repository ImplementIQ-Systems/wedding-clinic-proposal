import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.product import Product, ProductImage
from app.schemas.product import ProductCreate, ProductImageOut, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


def _upload_dir() -> Path:
    p = Path(settings.UPLOAD_DIR)
    p.mkdir(parents=True, exist_ok=True)
    return p


@router.get("/", response_model=list[ProductOut])
def list_products(
    category_id: int | None = None,
    disponivel: bool | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Product)
    if category_id is not None:
        q = q.filter(Product.category_id == category_id)
    if disponivel is not None:
        q = q.filter(Product.disponivel == disponivel)
    return q.all()


@router.get("/{id}", response_model=ProductOut)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(404, "Produto não encontrado")
    return product


@router.post("/", response_model=ProductOut, status_code=201, dependencies=[Depends(get_current_user)])
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.patch("/{id}", response_model=ProductOut, dependencies=[Depends(get_current_user)])
def update_product(id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(404, "Produto não encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{id}", status_code=204, dependencies=[Depends(get_current_user)])
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(404, "Produto não encontrado")
    db.delete(product)
    db.commit()


@router.post("/{id}/images", response_model=ProductImageOut, dependencies=[Depends(get_current_user)])
async def upload_image(
    id: int,
    file: UploadFile = File(...),
    capa: bool = Form(False),
    db: Session = Depends(get_db),
):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(404, "Produto não encontrado")

    ext = Path(file.filename).suffix if file.filename else ".jpg"
    filename = f"{uuid.uuid4()}{ext}"
    dest = _upload_dir() / filename

    content = await file.read()
    dest.write_bytes(content)

    if capa:
        db.query(ProductImage).filter(
            ProductImage.product_id == id, ProductImage.capa == True  # noqa: E712
        ).update({"capa": False})

    ordem = db.query(ProductImage).filter(ProductImage.product_id == id).count()
    image = ProductImage(
        product_id=id,
        url=f"/uploads/{filename}",
        ordem=ordem,
        capa=capa,
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.delete("/{product_id}/images/{image_id}", status_code=204, dependencies=[Depends(get_current_user)])
def delete_image(product_id: int, image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(
        ProductImage.id == image_id, ProductImage.product_id == product_id
    ).first()
    if not image:
        raise HTTPException(404, "Imagem não encontrada")
    path = Path(image.url.lstrip("/"))
    path.unlink(missing_ok=True)
    db.delete(image)
    db.commit()
