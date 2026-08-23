import os
from functions.get_valid_path import get_valid_path

def write_file(working_directory, file_path, content):
    try:
        full_path = get_valid_path(working_directory, file_path)

        if full_path is None:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_dir = os.path.dirname(full_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(full_path, mode="w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'