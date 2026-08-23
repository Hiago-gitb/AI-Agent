import os
from providers.base import LLMProvider
from providers.nvidia import NVIDIAProvider
from providers.openrouter import OpenRouterProvider

def create_provider() -> LLMProvider:
    # Read the provider selected in the environment.
    provider = os.environ.get("LLM_PROVIDER", "nvidia").lower()

    if provider == "nvidia":
        return NVIDIAProvider()

    if provider == "openrouter":
        return OpenRouterProvider()

    # Reject unsupported providers.
    raise ValueError(f"Unknown LLM provider: {provider}")