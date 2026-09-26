import io
import uuid
from pathlib import Path

from PIL import Image, UnidentifiedImageError

MAX_FULL_PX = 1600
MAX_THUMB_PX = 400
WEBP_QUALITY = 80


def _resize(img: Image.Image, max_px: int) -> Image.Image:
    w, h = img.size
    if max(w, h) <= max_px:
        return img
    ratio = max_px / max(w, h)
    return img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)


def process_upload(data: bytes, upload_dir: Path) -> tuple[str, str]:
    """
    Valida, redimensiona e converte para WebP.

    Devolve (full_url, thumb_url) como paths relativos servíveis.
    Lança ValueError se os dados não forem uma imagem válida.

    A thumbnail é guardada com sufixo _thumb no mesmo directório —
    o URL é sempre derivável do full_url, não precisamos de coluna extra.
    """
    try:
        # verify() consome o stream; reabrimos para processar
        Image.open(io.BytesIO(data)).verify()
        img = Image.open(io.BytesIO(data))
    except (UnidentifiedImageError, Exception) as exc:
        raise ValueError(f"Ficheiro inválido ou corrompido: {exc}") from exc

    # WebP suporta RGBA; para outros modos convertemos para RGB
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    name = uuid.uuid4().hex
    upload_dir.mkdir(parents=True, exist_ok=True)

    full_img = _resize(img.copy(), MAX_FULL_PX)
    full_path = upload_dir / f"{name}.webp"
    full_img.save(full_path, "WEBP", quality=WEBP_QUALITY)

    thumb_img = _resize(img.copy(), MAX_THUMB_PX)
    thumb_path = upload_dir / f"{name}_thumb.webp"
    thumb_img.save(thumb_path, "WEBP", quality=WEBP_QUALITY)

    return f"/uploads/{name}.webp", f"/uploads/{name}_thumb.webp"
