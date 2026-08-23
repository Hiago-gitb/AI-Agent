# tests/write_file.py

from functions.write_file import write_file

# Verify writing content to an existing file.
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

# Verify writing to a file inside a subdirectory.
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

# Verify that writing outside the working directory is rejected.
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))