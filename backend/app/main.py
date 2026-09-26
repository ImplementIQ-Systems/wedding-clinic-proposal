from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routers import auth, blog, bookings, categories, products

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(bookings.router)
app.include_router(blog.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
