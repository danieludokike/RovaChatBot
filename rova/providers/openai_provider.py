# rova/providers/openai_provider.py
from __future__ import annotations
import os
from typing import Iterable
from openai import OpenAI
from .base import Provider

class OpenAIProvider(Provider):
    name = "openai"

    def __init__(self, model: str | None = None, api_key: str | None = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Add it to your .env.")
        self.model = model or os.getenv("MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=api_key)

    def complete(self, messages: list[dict]) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""

    def stream(self, messages: list[dict]) -> Iterable[str]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
