# AI Agent

A small Python AI agent that can interact with a local project through tool calling.

The agent can inspect files, read file contents, create or update files, and run Python files inside a permitted working directory. It also includes a simple calculator project used as the agent's working environment and for testing the tools.

The project currently uses NVIDIA's API by default, but it can also be configured to use OpenRouter.

## Features

- Chat with an LLM from the command line
- Function/tool calling
- List files and directories
- Read file contents
- Write and create files
- Run Python files
- Restrict file operations to the configured working directory
- Limit file reads to avoid returning extremely large files
- Optional verbose tool-call output
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

Clone the repository and install the dependencies with `uv`:

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

Then add your API key to `.env`.

## API Providers

The project uses the OpenAI Python SDK, so both NVIDIA and OpenRouter can be used with the same basic client structure.

### NVIDIA

NVIDIA provides an OpenAI-compatible API endpoint at:

```text
https://integrate.api.nvidia.com/v1
```

The project currently uses:

```text
nvidia/nemotron-3-super-120b-a12b
```

NVIDIA's model page provides a `Generate API Key` option and uses the same OpenAI-compatible base URL shown above.

Get your key from the NVIDIA API Catalog:

https://build.nvidia.com/

Add it to `.env`:

```env
NVIDIA_API_KEY=nvapi-your-key-here
```

The current `main.py` reads this variable:

```python
api_key = os.environ.get("NVIDIA_API_KEY")
```

NVIDIA's hosted API documentation and model examples are available in the [NVIDIA API Catalog](https://build.nvidia.com/) and [NVIDIA documentation](https://docs.nvidia.com/).

#### Free Tier Limits

The free tier on `build.nvidia.com` is intended for prototyping and experimentation, not production.

| Limit                     | Value                                     |
| ------------------------- | ----------------------------------------- |
| Requests per minute (RPM) | ~40 RPM per model (community baseline)    |
| Free credits              | ~1,000 on signup; up to ~5,000 by request |
| Token limit per model     | Not published by NVIDIA                   |
| Credit card required      | No                                        |
| RPM upgrade available     | Yes, by request (up to ~200 RPM)          |

A few things worth knowing:

- The 40 RPM ceiling is a community-acknowledged baseline. NVIDIA does not publish a hard SLA for the free tier, so the actual limit can vary by model and overall traffic.
- Credits are consumed per request. Lightweight models use a fraction of a credit; large models use more. Once your credits run out you will start getting `429 Too Many Requests` errors.
- NVIDIA does not publish per-model token limits for the hosted API. If you hit an undocumented limit it will also come back as a 429.
- You can request additional credits or a rate limit increase through the [NVIDIA Developer Forums](https://forums.developer.nvidia.com/). Results vary, so treat this as a best-effort process.
- For unlimited usage, NVIDIA AI Enterprise or one of the hosted NIM providers (Together AI, Baseten, Fireworks) are the options to look into.

### OpenRouter

OpenRouter is useful if you want to switch between many models and providers without changing the rest of the API integration. Its API is OpenAI-compatible and uses:

```text
https://openrouter.ai/api/v1
```

Create an API key from:

https://openrouter.ai/keys

Add it to `.env`:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

OpenRouter model names normally follow the format:

```text
provider/model
```

For example:

```text
openai/gpt-4o-mini
```

Always check the current model list before choosing a model:

https://openrouter.ai/models

#### Free Tier Limits

OpenRouter has two kinds of models: free models (IDs ending in `:free`) and paid models billed per token.

| Limit                     | Free account         | After one-time $10 purchase |
| ------------------------- | -------------------- | --------------------------- |
| Requests per minute (RPM) | 20 RPM               | 20 RPM (unchanged)          |
| Requests per day          | 50 req/day           | 1,000 req/day               |
| Cost per token            | $0 on `:free` models | $0 on `:free` models        |
| Credit card required      | No                   | No (credits never expire)   |

A few things worth knowing:

- The 20 RPM cap is fixed regardless of your credit balance. Purchasing credits only raises the daily request ceiling from 50 to 1,000.
- Free models rotate. A model listed as `:free` today may move to paid without notice as providers adjust their capacity. Always verify at [openrouter.ai/models](https://openrouter.ai/models) before committing to a specific model ID.
- Paid models are billed per input and output token. Pricing varies widely by model and provider. Check the catalog page for each model to see its current rate.
- When any limit is exceeded the API returns HTTP `429 Too Many Requests`. The per-minute window resets after 60 seconds; the daily window resets at midnight UTC.
- If you do not want to track which free models are currently available, OpenRouter offers `openrouter/free` as a meta-model that automatically routes your request to a suitable free model based on what the request requires (tool calling, image input, and so on). You trade control over the exact model for stability as the free catalog changes.

## Switching Providers

The provider is currently configured directly in `main.py`.

### From NVIDIA to OpenRouter

Change the API key variable:

```python
api_key = os.environ.get("OPENROUTER_API_KEY")
```

Change the base URL:

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
```

Then change the model to a model available on OpenRouter:

```python
model="provider/model-name"
```

For example:

```python
response = client.chat.completions.create(
    model="provider/model-name",
    messages=messages,
    tools=available_functions,
)
```

You do not need to rewrite the tool-calling system just because you changed providers. The important parts are the API key, base URL, and model.

### From OpenRouter back to NVIDIA

Use:

```python
api_key = os.environ.get("NVIDIA_API_KEY")
```

```python
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
)
```

Then select an NVIDIA model available through the NVIDIA API Catalog.

## Running the Agent

Run the agent with:

```bash
uv run main.py "What files are in the calculator directory?"
```

For verbose output:

```bash
uv run main.py "Read calculator/main.py" --verbose
```

The agent can decide when to use its available tools. For example, a request such as:

```text
Read the contents of calculator/pkg/calculator.py
```

can cause the model to call `get_file_content`.

## Available Tools

### `get_files_info`

Lists files in a directory and returns their sizes and whether they are directories.

### `get_file_content`

Reads a file relative to the working directory. File contents are limited to 10,000 characters.

### `write_file`

Writes content to a file and creates missing parent directories when necessary.

### `run_python_file`

Runs a Python file with optional command-line arguments. Execution is limited to the permitted working directory and has a 30-second timeout.

### `get_valid_path`

Validates paths before file operations so the tools cannot access locations outside the permitted working directory.

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

Run the calculator tests with:

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

These scripts also test invalid paths, missing files, file truncation, writing restrictions, and Python execution restrictions.

## Security Notes

The file tools are intentionally restricted to the `calculator` working directory so the agent cannot read or write anywhere else on the system.

This project restricts file paths, but it is not intended to be a secure sandbox for untrusted code.

## Model Selection

If you use OpenRouter, choose a model that supports the features required by the agent, especially tool/function calling.

OpenRouter provides a model catalog with capabilities, context windows, pricing, and other model information:

https://openrouter.ai/models

For NVIDIA, check the current NVIDIA API Catalog because available hosted models can change over time:

https://build.nvidia.com/

## Why NVIDIA or OpenRouter?

I recommend starting with NVIDIA if you want a simple setup with a hosted NVIDIA model and an OpenAI-compatible API.

OpenRouter is a great alternative when you want to experiment with different models and providers without rebuilding the rest of the agent. You mainly change the API key, base URL, and model name.

## Notes

This is a learning project, so the implementation is intentionally simple. The agent loop, tool execution, path validation, and calculator are all kept relatively small so the behavior is easy to understand and modify.
