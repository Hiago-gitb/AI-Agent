# tests/test_get_files_info.py

from functions.get_files_info import get_files_info

# Verify listing the contents of the working directory.
print(get_files_info("calculator", "."))

# Verify listing a subdirectory within the working directory.
print(get_files_info("calculator", "pkg"))

# Verify that access to directories outside the working directory is rejected.
print(get_files_info("calculator", "/bin"))

# Verify that parent directory traversal is rejected.
print(get_files_info("calculator", "../"))