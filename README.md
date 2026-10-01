# nmp-notes 📝

[![PyPI version](https://img.shields.io/pypi/v/nmp-notes.svg)](https://pypi.org/project/nmp-notes/)
[![Python versions](https://img.shields.io/pypi/pyversions/nmp-notes.svg)](https://pypi.org/project/nmp-notes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`nmp-notes`** (imported as **`nmp`**) is a lightweight Python library and CLI tool designed to help students and educators quickly scaffold prefilled practical lab files from templates.

Instead of writing boilerplate from scratch for every computer science lab assignment, run a single command or Python function to generate an organized, ready-to-run practical file.

---

## ⚡ Features

- **CLI & Python API**: Use the `nmp` command in your terminal or `import nmp` in your scripts.
- **Dot-Notation Access**: Target templates cleanly using dot-syntax (e.g., `ai.p1` $\rightarrow$ `src/nmp/templates/ai/p1.py`).
- **Dynamic Template Discovery**: Automatically discovers any new templates placed in the `templates/` folder without code modifications.
- **Safe by Default**: Won't accidentally overwrite existing lab files unless explicitly requested with `--force` or `force=True`.
- **Zero External Runtime Dependencies**: Built entirely with Python's standard library.

---

## 📦 Installation

### From Source (Development / Editable Mode)
```bash
git clone https://github.com/Sus69/nmp-notes.git
cd nmp-notes
pip install -e .
```

### From PyPI
```bash
pip install nmp-notes
```

---

## 🚀 CLI Usage

After installation, the `nmp` command is available in your shell.

### 1. List Available Templates
Discover all practical templates bundled with the package:

```bash
nmp list
```

**Output:**
```text
Available practical templates (2):
  • ai.p1
  • dbms.p1

Tip: Run 'nmp make <template_name>' to generate a practical file.
```

### 2. Generate a Practical File
Create a practical file in the current working directory:

```bash
nmp make ai.p1
```
*Creates `ai_p1.py` in your current directory.*

### 3. Specify Output Directory and Custom Filename
```bash
# Save into a specific folder:
nmp make dbms.p1 --output-dir ./lab_submissions

# Save with a custom filename:
nmp make dbms.p1 --filename practical_01_dbms.py

# Combine options:
nmp make ai.p1 -o ./practicals -f lab1.py
```

### 4. Overwrite Existing Files (`--force`)
If the destination file already exists, `nmp` stops to prevent data loss:
```bash
nmp make ai.p1
# [Error] Target file already exists: '.../ai_p1.py'. Use force=True (or --force flag) to overwrite.

# To overwrite:
nmp make ai.p1 --force
```

---

## 🐍 Python API Usage

You can also use `nmp` directly inside Python:

```python
import nmp

# 1. Discover all available templates
templates = nmp.mk.available_templates()
print("Available:", templates)
# Output: ['ai.p1', 'dbms.p1']

# 2. Generate a template file (default: ./ai_p1.py)
created_path = nmp.mk.file("ai.p1")
print(f"Created at: {created_path}")

# 3. Specify custom directory, filename, and force overwrite
nmp.mk.file(
    name="dbms.p1",
    output_dir="./labs",
    filename="dbms_lab_01.py",
    force=True
)
```

### Exception Handling
The library provides clean, typed exceptions:

```python
import nmp
from nmp.mk import TemplateNotFoundError, TargetFileExistsError

try:
    nmp.mk.file("ai.p99")
except TemplateNotFoundError as e:
    print(f"Template missing: {e}")

try:
    nmp.mk.file("ai.p1", force=False)
except TargetFileExistsError as e:
    print(f"File already exists: {e}")
```

---

## 📂 Project Structure

```text
nmp-notes/
├── .gitignore
├── MANIFEST.in
├── pyproject.toml
├── README.md
└── src/
    └── nmp/
        ├── __init__.py
        ├── __main__.py
        ├── cli.py
        ├── mk.py
        └── templates/
            ├── ai/
            │   └── p1.py
            └── dbms/
                └── p1.py
```

---

## ➕ Adding New Templates

To add a new lab practical template:

1. Create a folder under `src/nmp/templates/` representing your subject (e.g., `os/`, `cn/`, `ml/`).
2. Add your Python template file (e.g., `src/nmp/templates/os/p1.py`).
3. That's it! `nmp list` and `nmp make os.p1` will immediately detect and use it.

---

## 🛠 Building and Publishing

To build the wheel and source distribution:

```bash
# Install build tools
pip install --upgrade build twine

# Build distribution packages (.whl and .tar.gz)
python -m build

# Check distribution integrity
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

- **Author**: kc9ru
- **Email**: [kc9ru@protonmail.com](mailto:kc9ru@protonmail.com)
