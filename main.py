import argparse
import sys
from dotenv import load_dotenv
from prompts import system_prompt
from functions.call_function import available_functions, call_function
from providers.factory import create_provider

load_dotenv()

# Create the provider selected in the environment.
provider = create_provider()

# Parse the user's prompt and optional command-line arguments.
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="Error in prompt, try again")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

# Allow the model to call tools and continue processing their results.
for i in range(20):
    response = provider.generate(
        messages = messages,
        tools=available_functions,
    )

    if response.usage == None:
        raise RuntimeError("The API request failed: no usage information was returned.")

    message = response.choices[0].message
    messages.append(message.model_dump())

    # Stop when the model provides a final response without tool calls.
    if not message.tool_calls:
        break

    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, args.verbose)

        if result_message is None:
            raise Exception("The tool call failed to return a result.")

        messages.append(result_message)

else:
    print("Maximum number of iterations reached. The model did not produce a final response.")
    sys.exit(1)

# Display token usage and the response when verbose mode is enabled.
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")
    if message.content != None:
        print(f"Response:\n{message.content}")

else:
    if message.content != None:
        print(f"Response:\n{message.content}")