import re
import unicodedata


def slugify(text: str) -> str:
    """Converte título em slug URL-seguro (minúsculas, sem acentos, hífens)."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text
