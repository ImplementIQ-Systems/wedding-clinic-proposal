from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.slugify import slugify
from app.db.session import get_db
from app.models.blog_post import BlogPost
from app.schemas.blog_post import BlogPostCreate, BlogPostImport, BlogPostOut, BlogPostUpdate

router = APIRouter(prefix="/blog", tags=["blog"])


def _unique_slug(base: str, db: Session, exclude_id: int | None = None) -> str:
    slug = base
    n = 1
    while True:
        q = db.query(BlogPost).filter(BlogPost.slug == slug)
        if exclude_id:
            q = q.filter(BlogPost.id != exclude_id)
        if not q.first():
            return slug
        slug = f"{base}-{n}"
        n += 1


@router.get("/", response_model=list[BlogPostOut])
def list_posts(db: Session = Depends(get_db)):
    return (
        db.query(BlogPost)
        .filter(BlogPost.publicado == True)  # noqa: E712
        .order_by(BlogPost.data_publicacao.desc())
        .all()
    )


# /import DEVE vir antes de /{slug} para não ser capturado como slug
@router.post("/import", response_model=list[BlogPostOut], status_code=201, dependencies=[Depends(get_current_user)])
def import_posts(posts: list[BlogPostImport], db: Session = Depends(get_db)):
    """Importa posts com slug exacto (migração do Wix). Ignora duplicados de slug."""
    created = []
    for p in posts:
        if db.query(BlogPost).filter(BlogPost.slug == p.slug).first():
            continue
        post = BlogPost(**p.model_dump())
        db.add(post)
        db.flush()
        created.append(post)
    db.commit()
    for post in created:
        db.refresh(post)
    return created


@router.post("/", response_model=BlogPostOut, status_code=201, dependencies=[Depends(get_current_user)])
def create_post(payload: BlogPostCreate, db: Session = Depends(get_db)):
    base = payload.slug if payload.slug else slugify(payload.titulo)
    if not base:
        raise HTTPException(400, "Não foi possível gerar um slug a partir do título")
    slug = _unique_slug(base, db)
    post = BlogPost(**{**payload.model_dump(exclude={"slug"}), "slug": slug})
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{slug}", response_model=BlogPostOut)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post or not post.publicado:
        raise HTTPException(404, "Post não encontrado")
    return post


@router.patch("/{id}", response_model=BlogPostOut, dependencies=[Depends(get_current_user)])
def update_post(id: int, payload: BlogPostUpdate, db: Session = Depends(get_db)):
    post = db.get(BlogPost, id)
    if not post:
        raise HTTPException(404, "Post não encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id}", status_code=204, dependencies=[Depends(get_current_user)])
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.get(BlogPost, id)
    if not post:
        raise HTTPException(404, "Post não encontrado")
    db.delete(post)
    db.commit()
