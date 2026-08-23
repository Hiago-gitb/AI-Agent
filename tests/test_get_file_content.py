# tests/test_get_file_content.py

from functions.get_files_content import get_file_content

# Check that large files are truncated at the configured character limit.
result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

# Verify that files in the working directory can be read correctly.
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))

# Verify that access outside the working directory is rejected.
print(get_file_content("calculator", "/bin/cat"))

# Verify that missing files return an appropriate error.
print(get_file_content("calculator", "pkg/does_not_exist.py"))