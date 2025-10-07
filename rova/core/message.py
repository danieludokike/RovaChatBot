from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    role: str          # "user" | "assistant"
    text: str
    ts: datetime
