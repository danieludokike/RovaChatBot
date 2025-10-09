# rova/core/settings.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json, os
from dotenv import load_dotenv

APP_DIR = Path.cwd()
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
PREF_PATH = DATA_DIR / "app_prefs.json"

load_dotenv(APP_DIR / ".env", override=False)

@dataclass
class AppSettings:
    theme: str = "light"
    provider: str = os.getenv("PROVIDER", "mock")
    model: str = os.getenv("MODEL", "mock-small")

    @classmethod
    def load(cls) -> "AppSettings":
        # start with defaults (incl. env)
        s = cls()
        # overlay saved prefs if present
        if PREF_PATH.exists():
            try:
                saved = json.loads(PREF_PATH.read_text(encoding="utf-8"))
                # only overlay fields not set via env
                if "provider" in saved and not os.getenv("PROVIDER"):
                    s.provider = saved["provider"]
                if "model" in saved and not os.getenv("MODEL"):
                    s.model = saved["model"]
                if "theme" in saved:
                    s.theme = saved["theme"]
            except Exception:
                pass
        # final: if env present, force override (safety)
        if os.getenv("PROVIDER"):
            s.provider = os.getenv("PROVIDER")
        if os.getenv("MODEL"):
            s.model = os.getenv("MODEL")
        return s

    def save(self) -> None:
        PREF_PATH.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
