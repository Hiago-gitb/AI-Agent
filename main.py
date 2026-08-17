import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

load_dotenv()
# Read the OpenRouter key from the environment file.
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key or api_key == None:
    raise RuntimeError("Error with API key, check it")

# Configure the OpenAI client to send requests through OpenRouter.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Accept the user's message as a command-line argument.
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="Error in prompt, try again")
args = parser.parse_args()

messages = [
    {"role": "user", "content": args.user_prompt},
]

# Send the prompt to the selected chat model.
response = client.chat.completions.create(
    model = "openrouter/free",
    messages = messages,
)

# Stop if the API did not return token usage data.
if response.usage == None:
    raise RuntimeError("Failed API request")

# Display the prompt, usage details, and generated reply.
print(f"User prompt: {args.user_prompt}")
print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")
print(f"Response:\n{response.choices[0].message.content}")
