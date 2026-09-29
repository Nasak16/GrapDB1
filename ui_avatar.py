"""Profile photo helpers for GraphBook.

Pure stdlib on purpose (no Streamlit import) so the avatar HTML can be unit
tested without a running app.

Two kinds of photo
------------------
1. รูปของผู้ดูแลระบบ (admin/owner) - ตั้งครั้งเดียวไว้ใช้ทั้งแอป
   วางไฟล์เป็น  assets/profile.jpg   (หรือ .png / .jpeg / .webp)
   หรืออัปโหลดจากหน้า Admin / Setup (จะบันทึกเป็น assets/profile.<ext>)

2. รูปของนักศึกษาแต่ละคน (ไม่บังคับ) - assets/students/<student_id>.jpg
   ถ้าไม่มีจะใช้  assets/students/default.jpg  ถ้ายังไม่มีอีกจะโชว์อักษรย่อ
"""

from __future__ import annotations

import base64
import html
from pathlib import Path

ASSETS_ROOT = Path(__file__).resolve().parent / "assets"
ASSET_DIR = ASSETS_ROOT / "students"
PROFILE_STEM = "profile"

PHOTO_EXTS = (".png", ".jpg", ".jpeg", ".webp")
MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}
MAX_PHOTO_BYTES = 8 * 1024 * 1024  # 8 MB


def _first_existing(folder: Path, stem: str) -> Path | None:
    for ext in PHOTO_EXTS:
        candidate = folder / f"{stem}{ext}"
        if candidate.is_file():
            return candidate
    return None


def find_photo(student_id: str | None = None) -> Path | None:
    """Photo for this student_id, else the shared default photo, else None."""
    for key in (student_id, "default"):
        if not key:
            continue
        found = _first_existing(ASSET_DIR, key)
        if found is not None:
            return found
    return None


def find_profile_photo() -> Path | None:
    """รูปของผู้ดูแลระบบ (assets/profile.<ext>) หรือ None ถ้ายังไม่ได้ตั้ง."""
    return _first_existing(ASSETS_ROOT, PROFILE_STEM)


def save_profile_photo(data: bytes, filename: str) -> Path:
    """บันทึกรูปผู้ดูแลระบบเป็น assets/profile.<ext> แทนไฟล์เดิม (ถ้ามี)."""
    if not data:
        raise ValueError("ไฟล์รูปว่างเปล่า")
    if len(data) > MAX_PHOTO_BYTES:
        raise ValueError(f"ไฟล์ใหญ่เกิน {MAX_PHOTO_BYTES // (1024 * 1024)} MB")
    ext = Path(filename or "").suffix.lower()
    if ext not in PHOTO_EXTS:
        raise ValueError("นามสกุลที่รองรับ: " + ", ".join(PHOTO_EXTS))

    ASSETS_ROOT.mkdir(parents=True, exist_ok=True)
    for other in PHOTO_EXTS:
        stale = ASSETS_ROOT / f"{PROFILE_STEM}{other}"
        if stale.exists() and stale != ASSETS_ROOT / f"{PROFILE_STEM}{ext}":
            stale.unlink()
    target = ASSETS_ROOT / f"{PROFILE_STEM}{ext}"
    target.write_bytes(data)
    return target


def initials(name: str | None) -> str:
    """'Anan Srisuk' -> 'AS'. Falls back to '?' for empty names."""
    parts = [w for w in str(name or "").strip().split() if w]
    return "".join(w[0] for w in parts[:2]).upper() or "?"


def _avatar(photo: Path | None, name: str | None, size: int, accent: str) -> str:
    """HTML วงกลม: ใส่รูปถ้ามี ไม่งั้นโชว์อักษรย่อ."""
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
            f'font-size:{max(14, size // 3)}px;letter-spacing:.06em;">'
            f"{html.escape(initials(name))}</div>"
        )
        border = "3px dashed rgba(128,128,128,.55)"
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;overflow:hidden;'
        f'border:{border};box-shadow:0 8px 20px rgba(0,0,0,.28);margin-bottom:.6rem;">'
        f"{inner}</div>"
    )


def avatar_html(
    student_id: str | None,
    name: str | None = None,
    size: int = 132,
    accent: str = "#0f766e",
) -> str:
    """วงกลมประจำตัวนักศึกษา: รูปของคนนั้นถ้ามี ไม่งั้นอักษรย่อ."""
    return _avatar(find_photo(student_id), name, size, accent)


def profile_avatar_html(
    name: str | None = None,
    size: int = 96,
    accent: str = "#0f766e",
) -> str:
    """วงกลมของผู้ดูแลระบบจาก assets/profile.<ext> (รูปที่ตั้งไว้เฉย ๆ)."""
    return _avatar(find_profile_photo(), name, size, accent)
