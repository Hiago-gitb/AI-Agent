from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from collections.abc import Callable
import json

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_write_file,
    schema_run_python_file
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(tool_call, verbose = False):
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")
    function_args["working_directory"] = "./calculator"
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    if function_name not in function_map:
        return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": f"Error: Unknown function: {function_name}",
    }

    result = function_map[function_name](**function_args)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    }
