from __future__ import annotations
from pathlib import Path

QSS_DIR = Path(__file__).parent / "qss"

def load_theme(theme: str) -> str:
    tokens = (QSS_DIR / f"tokens_{'dark' if theme=='dark' else 'light'}.qss").read_text(encoding="utf-8")
    base = (QSS_DIR / "base.qss").read_text(encoding="utf-8")
    return tokens + "\n" + base
