import os
from openai import OpenAI
from providers.base import LLMProvider

class NVIDIAProvider(LLMProvider):

    def __init__(self):
        # Load the NVIDIA API key from the environment.
        api_key = os.environ.get("NVIDIA_API_KEY")
        model = os.eviron.get("PROVIDER_MODEL")

        if not api_key:
            raise RuntimeError(
                "NVIDIA_API_KEY is not set. Check your .env file."
            )

        # Create the client using NVIDIA's OpenAI-compatible API.
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
        )

        if not model:
            self.model = "nvidia/nemotron-3-super-120b-a12b"
        else:
            self.model = model

    def generate(self, messages, tools):
        # Send the conversation and available tools to the model.
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
        )