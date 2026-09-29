"""Profile photo helpers for GraphBook.

Pure stdlib on purpose (no Streamlit import) so the avatar HTML can be unit
tested without a running app.

How to add your own photo
-------------------------
1. Save the picture as  assets/students/<student_id>.jpg   e.g. assets/students/S001.jpg
2. Supported extensions: .png .jpg .jpeg .webp
3. A file named  default.png / default.jpg  is used for every student that has
   no photo of their own.
4. Nothing to configure - the Dashboard picks the file up automatically.
"""

from __future__ import annotations

import base64
import html
from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parent / "assets" / "students"
PHOTO_EXTS = (".png", ".jpg", ".jpeg", ".webp")
MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def find_photo(student_id: str | None = None) -> Path | None:
    """Photo for this student_id, else the shared default photo, else None."""
    for key in (student_id, "default"):
        if not key:
            continue
        for ext in PHOTO_EXTS:
            candidate = ASSET_DIR / f"{key}{ext}"
            if candidate.is_file():
                return candidate
    return None


def initials(name: str | None) -> str:
    """'Anan Srisuk' -> 'AS'. Falls back to '?' for empty names."""
    parts = [w for w in str(name or "").strip().split() if w]
    return "".join(w[0] for w in parts[:2]).upper() or "?"


def avatar_html(
    student_id: str | None,
    name: str | None = None,
    size: int = 132,
    accent: str = "#0f766e",
) -> str:
    """Circular avatar: the student's photo if present, otherwise initials."""
    photo = find_photo(student_id)
    if photo is not None:
        mime = MIME_BY_EXT.get(photo.suffix.lower(), "application/octet-stream")
        b64 = base64.b64encode(photo.read_bytes()).decode("ascii")
        inner = (
            f'<img src="data:{mime};base64,{b64}" alt="{html.escape(str(name or ""))}" '
            'style="width:100%;height:100%;object-fit:cover;display:block;"/>'
        )
        border = f"3px solid {accent}"
    else:
        inner = (
            '<div style="width:100%;height:100%;display:flex;align-items:center;'
            "justify-content:center;background:#1f2937;color:#e5e7eb;font-weight:700;"
            f'font-size:{max(16, size // 3)}px;letter-spacing:.06em;">'
            f"{html.escape(initials(name))}</div>"
        )
        border = "3px dashed rgba(128,128,128,.55)"
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;overflow:hidden;'
        f'border:{border};box-shadow:0 8px 20px rgba(0,0,0,.28);margin-bottom:.6rem;">'
        f"{inner}</div>"
    )
