import os
from openai import OpenAI
from providers.base import LLMProvider

class OpenRouterProvider(LLMProvider):

    def __init__(self):
        # Load the OpenRouter API key from the environment.
        api_key = os.environ.get("OPENROUTER_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. Check your .env file."
            )

        # Create the client using OpenRouter's OpenAI-compatible API.
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        self.model = "openrouter/free"

    def generate(self, messages, tools):
        # Send the conversation and available tools to the model.
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
        )