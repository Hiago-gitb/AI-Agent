import os
import subprocess
from functions.get_valid_path import get_valid_path

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory, file_path, args: list[str] | None = None):
    try:
        full_path = get_valid_path(working_directory, file_path)
        output = ""

        if full_path is None:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path) and not os.path.isdir(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
            
        command = ["python", full_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return f'Process exited with code {result.returncode}'

        if not result.stdout and not result.stderr:
            return "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"

            if result.stderr:
                output += f"STDERR:\n{result.stderr}"
        
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"