import os
from functions.get_valid_path import get_valid_path

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory, directory="."):
    try:
        file_info = []
        target_dir = get_valid_path(working_directory, directory)

        if target_dir is None:
            return f'Result for {directory} directory:\n Error: Cannot list "{directory}" as it is outside the permitted working directory'

        for item in os.listdir(target_dir):
            if item == "__pycache__":
                continue
            path = os.path.join(target_dir, item)
            info = (f"- {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}")
            file_info.append(info)
        file_str = '\n'.join(file_info)
        
        if directory == ".":
            return f'Result for current directory:\n{file_str} '
        return f'Result for {directory} directory:\n{file_str} '

    except Exception as e:
        return f"Error: {e}"