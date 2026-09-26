import io
from pathlib import Path

import pytest
from PIL import Image

from app.services.image import MAX_FULL_PX, MAX_THUMB_PX, process_upload


def _make_jpeg(width: int, height: int) -> bytes:
    img = Image.new("RGB", (width, height), color=(200, 100, 50))
    buf = io.BytesIO()
    img.save(buf, "JPEG")
    return buf.getvalue()


def test_output_is_webp_and_files_exist(tmp_path: Path):
    data = _make_jpeg(800, 600)
    full_url, thumb_url = process_upload(data, tmp_path)

    assert full_url.endswith(".webp")
    assert thumb_url.endswith("_thumb.webp")

    full_path = tmp_path / Path(full_url).name
    thumb_path = tmp_path / Path(thumb_url).name
    assert full_path.exists()
    assert thumb_path.exists()

    with Image.open(full_path) as img:
        assert img.format == "WEBP"
    with Image.open(thumb_path) as img:
        assert img.format == "WEBP"


def test_large_image_is_downscaled(tmp_path: Path):
    data = _make_jpeg(3000, 2000)
    full_url, thumb_url = process_upload(data, tmp_path)

    full_path = tmp_path / Path(full_url).name
    thumb_path = tmp_path / Path(thumb_url).name

    with Image.open(full_path) as img:
        assert max(img.size) <= MAX_FULL_PX

    with Image.open(thumb_path) as img:
        assert max(img.size) <= MAX_THUMB_PX


def test_small_image_not_upscaled(tmp_path: Path):
    data = _make_jpeg(200, 150)
    full_url, _thumb_url = process_upload(data, tmp_path)

    full_path = tmp_path / Path(full_url).name
    with Image.open(full_path) as img:
        assert img.size == (200, 150)


def test_invalid_file_raises_value_error(tmp_path: Path):
    with pytest.raises(ValueError, match="inválido"):
        process_upload(b"not an image at all", tmp_path)
