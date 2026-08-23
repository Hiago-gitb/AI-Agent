# tests/test_run_python_file.py

from functions.run_python_file import run_python_file

# Verify running a Python file without arguments.
print(run_python_file("calculator", "main.py"))

# Verify passing command-line arguments to the Python file.
print(run_python_file("calculator", "main.py", ["3 + 5"]))

# Verify running the test file successfully.
print(run_python_file("calculator", "tests.py"))

# Verify that parent directory traversal is rejected.
print(run_python_file("calculator", "../main.py"))

# Verify that nonexistent files return an appropriate error.
print(run_python_file("calculator", "nonexistent.py"))

# Verify that non-Python files cannot be executed.
print(run_python_file("calculator", "lorem.txt"))