# rova/ui/theme.py
from __future__ import annotations
from pathlib import Path
import re

QSS_DIR = Path(__file__).parent / "qss"

_token_line = re.compile(r"^\s*--([a-zA-Z0-9_-]+)\s*:\s*(.+?)\s*;\s*$")
_var_ref    = re.compile(r"var\(--([a-zA-Z0-9_-]+)\)")

def _load_tokens(file: Path) -> dict[str, str]:
    toks: dict[str, str] = {}
    for raw in file.read_text(encoding="utf-8").splitlines():
        m = _token_line.match(raw)
        if m:
            toks[m.group(1)] = m.group(2)
    return toks

def _apply_tokens(qss: str, tokens: dict[str, str]) -> str:
    def repl(m: re.Match):
        key = m.group(1)
        return tokens.get(key, f"/*UNRESOLVED:{key}*/")
    return _var_ref.sub(repl, qss)

def load_theme(theme: str) -> str:
    tokens_path = QSS_DIR / f"tokens_{'dark' if theme=='dark' else 'light'}.qss"
    base_path   = QSS_DIR / "base.qss"

    tokens = _load_tokens(tokens_path)
    base_qss = base_path.read_text(encoding="utf-8")
    resolved = _apply_tokens(base_qss, tokens)

    # Optional safety: raise if any var(...) remains
    if "var(--" in resolved:
        # Helps catch typos like var(--accnt)
        unresolved = set(m.group(1) for m in _var_ref.finditer(resolved))
        raise ValueError(f"Unresolved QSS tokens: {sorted(unresolved)}")

    return resolved
