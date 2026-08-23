import os
from functions.get_valid_path import get_valid_path

def get_file_content(working_directory, file_path):
    try:
        MAX_CHARS = 10000
        full_path = get_valid_path(working_directory, file_path)

        if full_path is None:
            return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
            
        with open(full_path, mode="r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'Error: {e}'