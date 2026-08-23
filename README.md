# AI Agent

A small Python AI agent that can interact with a local project through tool calling.

The agent can inspect files, read file contents, create or update files, and run Python files inside a permitted working directory. It also includes a simple calculator project used as the agent's working environment and for testing the tools.

The project supports multiple LLM providers through a simple provider abstraction. NVIDIA is used by default, but OpenRouter can also be selected without changing the agent code.

## Features

- Chat with an LLM from the command line
- Function/tool calling
- Multiple LLM providers
- Switch providers through environment variables
- List files and directories
- Read file contents
- Write and create files
- Run Python files
- Restrict file operations to the configured working directory
- Limit file reads to avoid returning extremely large files
- Optional verbose output
- Simple calculator with operator precedence
- Tests for the calculator and agent tools

## Project Structure

```text
.
├── calculator/
│   ├── pkg/
│   │   ├── calculator.py
│   │   └── render.py
│   ├── lorem.txt
│   ├── main.py
│   └── tests.py
│
├── functions/
│   ├── call_function.py
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── get_valid_path.py
│   ├── run_python_file.py
│   └── write_file.py
│
├── providers/
│   ├── base.py
│   ├── factory.py
│   ├── nvidia.py
│   └── openrouter.py
│
├── tests/
│   ├── test_get_file_content.py
│   ├── test_get_files_info.py
│   ├── test_run_python_file.py
│   └── test_write_file.py
│
├── .env.example
├── .gitignore
├── .python-version
├── main.py
├── prompts.py
├── pyproject.toml
└── uv.lock
```

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- An API key from NVIDIA or OpenRouter

## Installation

Clone the repository:

```bash
git clone https://github.com/Hiago-gitb/AI-Agent.git
cd AI-Agent
```

Install the dependencies with `uv`:

```bash
uv sync
```

Create your environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then open `.env` and configure your provider and API key.

## Configuration

The provider and model are configured through environment variables.

Your `.env` file can look like this:

```env
LLM_PROVIDER=nvidia
LLM_MODEL=nvidia/nemotron-3-super-120b-a12b

NVIDIA_API_KEY=nvapi-your-key-here
OPENROUTER_API_KEY=
```

### Available providers

The project currently supports:

- `nvidia`
- `openrouter`

If `LLM_PROVIDER` is not set, NVIDIA is used by default.

The provider is selected automatically when the agent starts. You do not need to change the Python code.

---

## NVIDIA

NVIDIA provides an OpenAI-compatible API that can be used by the agent without changing the tool-calling system.

The project currently uses:

```text
nvidia/nemotron-3-super-120b-a12b
```

Get an API key from the NVIDIA API Catalog:

[NVIDIA API Catalog](https://build.nvidia.com/?utm_source=chatgpt.com)

Add it to your `.env`:

```env
LLM_PROVIDER=nvidia
LLM_MODEL=nvidia/nemotron-3-super-120b-a12b

NVIDIA_API_KEY=nvapi-your-key-here
```

The NVIDIA provider handles the API endpoint and authentication separately from the agent itself.

---

## OpenRouter

OpenRouter provides access to many different models through an OpenAI-compatible API.

The project can use:

```text
openrouter/free
```

as a convenient free-model router.

Get an API key from:

[OpenRouter API Keys](https://openrouter.ai/keys?utm_source=chatgpt.com)

Then configure `.env`:

```env
LLM_PROVIDER=openrouter
LLM_MODEL=openrouter/free

NVIDIA_API_KEY=
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

You can also choose another OpenRouter model.

Check the available models here:

[OpenRouter Models](https://openrouter.ai/models?utm_source=chatgpt.com)

When choosing a model, make sure it supports tool/function calling, since the agent relies on this feature.

---

## Switching Providers

One of the main features of the project is that providers can be switched without modifying the agent code.

### Use NVIDIA

```env
LLM_PROVIDER=nvidia
LLM_MODEL=nvidia/nemotron-3-super-120b-a12b

NVIDIA_API_KEY=nvapi-your-key-here
OPENROUTER_API_KEY=
```

### Use OpenRouter

```env
LLM_PROVIDER=openrouter
LLM_MODEL=openrouter/free

NVIDIA_API_KEY=
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

That's it.

The agent reads `LLM_PROVIDER` and creates the corresponding provider automatically.

## Provider Architecture

The project uses a small abstraction to keep provider-specific code separate from the agent logic.

```text
                    Agent
                      |
                      v
                LLMProvider
                      |
             +--------+--------+
             |                 |
             v                 v
          NVIDIA          OpenRouter
```

`LLMProvider` defines the interface that each provider must implement.

The provider factory then selects the correct implementation:

```text
.env
 |
 | LLM_PROVIDER=nvidia
 |
 v
create_provider()
 |
 v
NVIDIAProvider
```

or:

```text
.env
 |
 | LLM_PROVIDER=openrouter
 |
 v
create_provider()
 |
 v
OpenRouterProvider
```

This means the agent does not need to know which API it is using.

The agent simply calls:

```python
response = provider.generate(
    messages=messages,
    tools=available_functions,
)
```

This makes it easier to add more providers in the future without changing the agent loop.

## How the Agent Works

The agent follows a simple tool-calling loop:

```text
User prompt
     |
     v
    Agent
     |
     v
 LLM Provider
     |
     v
Model decides whether a tool is needed
     |
     v
Tool execution
     |
     v
Tool result
     |
     v
 LLM Provider
     |
     v
Final response
```

For example, if you ask:

```text
Read the contents of calculator/pkg/calculator.py
```

the model can decide to call:

```text
get_file_content
```

The tool executes the operation and returns the result to the model.

The model can then continue using other tools or provide the final response.

The agent currently allows up to 20 iterations for a single request.

## Running the Agent

Run the agent with:

```bash
uv run main.py "What files are in the calculator directory?"
```

Another example:

```bash
uv run main.py "Read calculator/pkg/calculator.py"
```

For verbose output:

```bash
uv run main.py "Read calculator/main.py" --verbose
```

Verbose mode displays additional information such as token usage and the final response.

## Available Tools

### `get_files_info`

Lists files and directories inside the permitted working directory.

It returns information such as:

- File name
- File size
- Whether the entry is a directory

### `get_file_content`

Reads the contents of a file relative to the working directory.

File contents are limited to 10,000 characters to prevent very large responses.

### `write_file`

Writes content to a file.

It also creates missing parent directories when necessary.

### `run_python_file`

Runs a Python file with optional command-line arguments.

Python execution is restricted to the permitted working directory and has a 30-second timeout.

### `get_valid_path`

Validates paths before file operations.

It prevents the tools from accessing paths outside the permitted working directory.

## Calculator

The `calculator` directory contains a small expression calculator used by the agent.

Run it with:

```bash
uv run calculator/main.py "3 + 5"
```

Example output:

```json
{
  "expression": "3 + 5",
  "result": 8
}
```

It supports:

- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Operator precedence

For example:

```bash
uv run calculator/main.py "2 * 3 - 8 / 2 + 5"
```

## Testing

Run the calculator tests:

```bash
uv run calculator/tests.py
```

The tool tests can be run individually:

```bash
uv run tests/test_get_file_content.py
uv run tests/test_get_files_info.py
uv run tests/test_run_python_file.py
uv run tests/test_write_file.py
```

The tests cover cases such as:

- Invalid paths
- Missing files
- File truncation
- Writing restrictions
- Python execution restrictions

## Security Notes

The file tools are restricted to the `calculator` working directory.

Path validation prevents the agent from using paths that escape the permitted working directory.

The `run_python_file` tool also has a 30-second execution timeout.

However, this project is not a secure sandbox for untrusted code. Python files are executed using the local Python interpreter, so only trusted code should be executed.

## Model Selection

The model is configured through:

```env
LLM_MODEL=provider/model-name
```

For NVIDIA:

```env
LLM_PROVIDER=nvidia
LLM_MODEL=nvidia/nemotron-3-super-120b-a12b
```

For OpenRouter:

```env
LLM_PROVIDER=openrouter
LLM_MODEL=openrouter/free
```

If you use OpenRouter, you can browse its current model catalog here:

[OpenRouter Models](https://openrouter.ai/models?utm_source=chatgpt.com)

For NVIDIA models:

[NVIDIA API Catalog](https://build.nvidia.com/?utm_source=chatgpt.com)

Always check the provider's current model capabilities before selecting a model. In particular, the model should support tool/function calling.

## Why NVIDIA or OpenRouter?

I recommend NVIDIA if you want a simple setup with a hosted NVIDIA model and an OpenAI-compatible API.

OpenRouter is useful when you want to experiment with different models and providers without rebuilding the rest of the agent.

Because the provider implementation is separated from the agent logic, switching between them only requires changing the configuration in `.env`.

## Limitations

This project is intentionally small and focused on learning the fundamentals of building an AI agent.

Some current limitations include:

- No persistent conversation memory
- No streaming responses
- No parallel tool execution
- Limited error recovery for API failures
- Only a small number of supported providers
- Python execution is not a secure sandbox
- Tool behavior depends on the capabilities of the selected model

## Notes

This is a learning project built to explore how LLM tool calling, agent loops, file operations, provider abstraction, and basic security restrictions can work together in Python.

The implementation is intentionally kept relatively small so that the main concepts are easy to understand, modify, and extend.
