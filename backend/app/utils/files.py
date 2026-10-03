from pathlib import Path
from uuid import uuid4


def create_safe_filename(
    extension: str,
) -> str:
    clean_extension = extension.lstrip(".").lower()

    return f"{uuid4().hex}.{clean_extension}"


def ensure_directory(path: Path) -> Path:
    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path