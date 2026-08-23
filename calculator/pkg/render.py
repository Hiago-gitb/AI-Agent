# calculator/pkg/render.py

import json

def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    # Convert whole-number floats to integers for cleaner output.
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }

    # Format the result as a readable JSON string.
    return json.dumps(output_data, indent=indent)