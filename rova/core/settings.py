from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
from dotenv import load_dotenv
import os

APP_DIR = Path.cwd()
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
PREF_PATH = DATA_DIR / "app_prefs.json"

load_dotenv(dotenv_path=APP_DIR / ".env", override=False)

@dataclass
class AppSettings:
    theme: str = "light"               # "light" | "dark"
    provider: str = os.getenv("PROVIDER", "mock")
    model: str = os.getenv("MODEL", "mock-small")

    @classmethod
    def load(cls) -> "AppSettings":
        if PREF_PATH.exists():
            try:
                return cls(**json.loads(PREF_PATH.read_text(encoding="utf-8")))
            except Exception:
                pass
        return cls()

    def save(self) -> None:
        PREF_PATH.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
