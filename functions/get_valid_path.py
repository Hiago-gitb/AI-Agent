import os

def get_valid_path(working_directory, path):
    working_dir_abs = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_dir_abs, path))

    if os.path.commonpath([working_dir_abs, full_path]) != working_dir_abs:
        return None

    return full_path