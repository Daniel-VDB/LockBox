from pathlib import Path

p = Path("some/relative/path/file.txt")

# Absolute path as a Path object
abs_path = p.resolve()

# Absolute path as a string
abs_path_str = str(p.resolve())

print(abs_path_str)