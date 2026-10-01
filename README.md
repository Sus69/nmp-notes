# nmp-notes 📝

[![PyPI version](https://img.shields.io/pypi/v/nmp-notes.svg)](https://pypi.org/project/nmp-notes/)
[![Python versions](https://img.shields.io/pypi/pyversions/nmp-notes.svg)](https://pypi.org/project/nmp-notes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`nmp-notes`** (imported as **`nmp`**) is a lightweight Python library and CLI tool that drops a college practical's full code into your current folder.

---

## 📦 Installation

```bash
git clone https://github.com/Sus69/nmp-notes.git
cd nmp-notes
pip install -e .
```

---

## 🚀 CLI Usage

### 1. Interactive menu (default)

```bash
nmp
```

Shows an arrow-key menu (up/down + Enter, type-to-filter, `q` to quit). Pick one and its `.py` file is created in the current folder. Falls back to a numbered prompt when piped.

### 2. List practicals

```bash
nmp list
```

### 3. Create directly

```bash
nmp create 1a-bfs
nmp create 3-decision-tree -o my_tree.py
```

Generated files land in the current folder and are never overwritten silently — you'll be asked first (`create` prompts; the Python API needs `force=True`).

Practical 1a/1b/2a/2b also copy a shared `RMP.py` helper next to the file (never overwritten).

---

## 🐍 Python API Usage

```python
import nmp
from nmp.mk import TemplateNotFoundError, TargetFileExistsError

print(nmp.mk.available_templates())  # ['10-tensorflow-demo', '1a-bfs', ...]

nmp.mk.file("1a-bfs")                            # ./bfs.py (+ ./RMP.py)
nmp.mk.file("3-decision-tree", filename="t.py")  # custom name
nmp.mk.file("5-svm", output_dir="./labs")        # custom dir
nmp.mk.file("5-svm", force=True)                 # overwrite
```

---

## ➕ Adding New Templates

1. Drop the file in `src/nmp/templates/` (e.g. `kmeans.py`).
2. Register it in `src/nmp/mk.py` → `PRACTICALS` (slug → title + filename).
3. If it needs a shared helper, add it to `EXTRA_FILES`.
4. Reinstall.

---

## 📄 License

MIT — see the LICENSE file for details.
