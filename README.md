# AI Agent

A small Python AI agent that can interact with a local workspace through tool calling.

The agent can inspect files, read file contents, create or update files, and run Python files inside a permitted working directory (`workspace/`). The workspace currently contains two projects: a simple expression calculator and a book analyzer (Bookbot). All file operations are restricted to the workspace so the agent cannot access anything outside it.

The project uses NVIDIA's API by default, but can also be configured to use OpenRouter.

## Features

- Chat with an LLM from the command line
- Function/tool calling
- List files and directories
- Read file contents
- Write and create files
- Run Python files
- Restrict file operations to the `workspace/` directory
- Limit file reads to avoid returning extremely large files
- Optional verbose tool-call output
- Simple calculator with operator precedence
- Bookbot: word count and character frequency analysis for `.txt` files
- Tests for both workspace projects and agent tools

## Project Structure

```
.
├── workspace/
│   ├── calculator/
│   │   ├── pkg/
│   │   │   ├── calculator.py
│   │   │   └── render.py
│   │   ├── lorem.txt
│   │   ├── main.py
│   │   └── tests.py
│   └── bookbot/
│       ├── books/
│       ├── main.py
│       ├── stats.py
│       └── tests.py
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

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- An API key from NVIDIA or OpenRouter

## Installation

Clone the repository and install the dependencies with `uv`:

```
uv sync
```

Create your environment file:

```
cp .env.example .env
```

On Windows PowerShell:

```
Copy-Item .env.example .env
```

Then add your API key to `.env`.

## API Providers

The project uses the OpenAI Python SDK, so both NVIDIA and OpenRouter can be used with the same basic client structure. Provider configuration lives in the `providers/` directory.

### NVIDIA

NVIDIA provides an OpenAI-compatible API endpoint at:

```
https://integrate.api.nvidia.com/v1
```

Get your key from the NVIDIA API Catalog:

<https://build.nvidia.com/>

Add it to `.env`:

```
NVIDIA_API_KEY=nvapi-your-key-here
```

Nvidia model names normally follow the format:

```
provider/model
```

pick one and add it to `.env` aswell:

```
PROVIDER_MODEL=your_model
```

if no model is specified, the default model will be `nvidia/nemotron-3-super-120b-a12b`

Always check the current model list before choosing a model:

https://build.nvidia.com/models

#### Free Tier Limits

| Limit                     | Value                                     |
| ------------------------- | ----------------------------------------- |
| Requests per minute (RPM) | ~40 RPM per model (community baseline)    |
| Free credits              | ~1,000 on signup; up to ~5,000 by request |
| Credit card required      | No                                        |
| RPM upgrade available     | Yes, by request (up to ~200 RPM)          |

A few things worth knowing:

- The 40 RPM ceiling is a community-acknowledged baseline. NVIDIA does not publish a hard SLA for the free tier, so the actual limit can vary by model and overall traffic.
- Credits are consumed per request. Lightweight models use a fraction of a credit; large models use more. Once your credits run out you will start getting `429 Too Many Requests` errors.
- You can request additional credits or a rate limit increase through the [NVIDIA Developer Forums](https://forums.developer.nvidia.com/).
- For unlimited usage, NVIDIA AI Enterprise or one of the hosted NIM providers (Together AI, Baseten, Fireworks) are the options to look into.

### OpenRouter

OpenRouter is useful if you want to switch between many models and providers without changing the rest of the API integration. Its API is OpenAI-compatible and uses:

```
https://openrouter.ai/api/v1
```

Create an API key from:

<https://openrouter.ai/keys>

Add it to `.env`:

```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

OpenRouter model names normally follow the format:

```
provider/model
```

pick one and add it to `.env` aswell:

```
PROVIDER_MODEL=your_model
```

if no model is specified, the default model will be `openrouter/free`

Always check the current model list before choosing a model, choose a model that supports tool/function calling. OpenRouter provides a model catalog with capabilities, context windows, and pricing:

<https://openrouter.ai/models>

#### Free Tier Limits

| Limit                     | Free account         | After one-time $10 purchase |
| ------------------------- | -------------------- | --------------------------- |
| Requests per minute (RPM) | 20 RPM               | 20 RPM (unchanged)          |
| Requests per day          | 50 req/day           | 1,000 req/day               |
| Cost per token            | $0 on `:free` models | $0 on `:free` models        |
| Credit card required      | No                   | No (credits never expire)   |

A few things worth knowing:

- The 20 RPM cap is fixed regardless of your credit balance. Purchasing credits only raises the daily request ceiling from 50 to 1,000.
- Free models rotate. A model listed as `:free` today may move to paid without notice. Always verify at [openrouter.ai/models](https://openrouter.ai/models) before committing to a specific model ID.
- When any limit is exceeded the API returns HTTP `429 Too Many Requests`. The per-minute window resets after 60 seconds; the daily window resets at midnight UTC.
- OpenRouter offers `openrouter/free` as a meta-model that automatically routes your request to a suitable free model if you do not want to track which free models are currently available.

## Switching Providers

The provider is configured in the `providers/` directory and referenced in `main.py`.

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

Then set the model to one available on OpenRouter in the `.env` file:

```python
PROVIDER_MODEL="provider/model-name"
```

### From OpenRouter back to NVIDIA

```python
api_key = os.environ.get("NVIDIA_API_KEY")
model = os.eviron.get("PROVIDER_MODEL")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
)
```

You do not need to rewrite the tool-calling system when switching providers. The important parts are the API key, base URL, and model name.

## Running the Agent

Run the agent with:

```
uv run main.py "What files are in the workspace?"
```

For verbose output:

```
uv run main.py "Read workspace/calculator/main.py" --verbose
```

The agent can decide when to use its available tools based on the request. For example:

```
uv run main.py "Analyze the book in workspace/bookbot/books/"
```

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

## Workspace Projects

The `workspace/` directory is the controlled environment where the agent operates. All agent file tools are scoped to this directory.

### Adding a New Project

To give the agent access to a new project, place it inside `workspace/`:

```
workspace/
└── your-project/
    └── main.py
```

No changes to the agent or its tools are required. The agent will be able to list, read, write, and run files inside `your-project/` as soon as it exists in the workspace. The path validation already handles anything placed there.

### Calculator

A small expression calculator.

Run it with:

```
uv run workspace/calculator/main.py "3 + 5"
```

Example output:

```json
{
  "expression": "3 + 5",
  "result": 8
}
```

Supported operations:

- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Operator precedence

Example:

```
uv run workspace/calculator/main.py "2 * 3 - 8 / 2 + 5"
```

### Bookbot

Bookbot is an older personal project included here as a second workspace example. The original repository is at [Hiago-gitb/BookBot](https://github.com/Hiago-gitb/BookBot). The agent did not exist when it was originally written — it was added to the workspace to show that any standalone Python project can be dropped into workspace/ and made accessible to the agent without modification.

A book analyzer that reads a `.txt` file and returns the total word count and the frequency of each character in the text.

Run it with:

```
uv run workspace/bookbot/main.py
```

Or let the agent run it for you:

```
uv run main.py "Run the bookbot on the book in workspace/bookbot/books/"
```

The script reads from the `books/` subdirectory. Place any `.txt` file there and point the script at it to get an analysis.

Example output:

```
============ BOOKBOT ============
Analyzing book found at books/frankenstein.txt
----------- Word Count ----------
Found 75767 total words
--------- Character Count -------
e: 44538
t: 29493
a: 25894
o: 24494
i: 23927
n: 23643
s: 20360
r: 20079
h: 19176
...
============= END ===============
```

## Testing

Each workspace project has its own `tests.py`. Run them directly:

```
uv run workspace/calculator/tests.py
```

```
uv run workspace/bookbot/tests.py
```

Or let the agent run them for you:

```
uv run main.py "Run the calculator tests at workspace/calculator"
```

```
uv run main.py "Run the bookbot tests at workspace/bookbot"
```

The agent tool tests live in `tests/` at the project root and are run separately:`

```
uv run tests/test_get_file_content.py
```

```
uv run tests/test_get_files_info.py
```

```
uv run tests/test_run_python_file.py
```

```
uv run tests/test_write_file.py
```

These scripts also test invalid paths, missing files, file truncation, writing restrictions, and Python execution restrictions.

### Writing tests for new projects

When you add a new project to `workspace/`, you can ask the agent to write tests for it. The existing `tests.py` files in `calculator/` and `bookbot/` serve as style references — the agent can read them and follow the same pattern for the new project.

### Writing tests for new projects

When you add a new project to `workspace/`, you can ask the agent to write tests for it. The existing `tests.py` files in `calculator/` and `bookbot/` serve as style references — the agent can read them and follow the same pattern for the new project.

```
uv run main.py "Read workspace/bookbot/tests.py and write a tests.py for workspace/your-project/ following the same style"
```

## Security Notes

The file tools are intentionally restricted to the `workspace/` directory so the agent cannot read or write anywhere else on the system.

The `.env` file is listed in `.gitignore` to keep the API key out of version control. The `.env.example` file serves as the template for the required environment variables.

## Why NVIDIA or OpenRouter?

NVIDIA is a simple starting point: one hosted model, one OpenAI-compatible endpoint, and a free tier that requires no credit card.

OpenRouter is a good alternative when you want to experiment with different models without rebuilding the agent. The only changes are the API key, base URL, and model name.

## Notes

This is a learning project, so the implementation is intentionally simple. The agent loop, tool execution, path validation, and workspace projects are all kept relatively small so the behavior is easy to understand and modify.
