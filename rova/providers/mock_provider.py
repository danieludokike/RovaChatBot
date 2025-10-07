from __future__ import annotations
from typing import Iterable
import time
from .base import Provider

class MockProvider(Provider):
    name = "mock"
    def complete(self, messages: list[dict]) -> str:
        q = messages[-1]["content"]
        return f"Rova (mock): I received — “{q}”."

    def stream(self, messages: list[dict]) -> Iterable[str]:
        text = self.complete(messages)
        for ch in text:
            time.sleep(0.01)
            yield ch
