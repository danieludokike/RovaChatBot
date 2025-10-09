# rova/providers/factory.py
from __future__ import annotations
from ..core.settings import AppSettings
from .base import Provider

def build_provider(settings: AppSettings) -> Provider:
    provider = (settings.provider or "mock").lower()

    if provider == "openai":
        from .openai_provider import OpenAIProvider
        return OpenAIProvider(model=settings.model)

    # fallback to mock if provider not supported
    from .mock_provider import MockProvider
    return MockProvider()
