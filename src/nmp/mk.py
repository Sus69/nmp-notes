"""Core logic for discovering and generating practical files from templates."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import importlib.resources as res


class NMPError(Exception):
    """Base exception for all nmp-notes library errors."""


class TemplateNotFoundError(NMPError, FileNotFoundError):
    """Raised when a requested template does not exist."""


class TargetFileExistsError(NMPError, FileExistsError):
    """Raised when the target output file already exists and force=False."""


# slug -> (title, template filename). Add new practicals here + drop file in templates/.
PRACTICALS: Dict[str, Tuple[str, str]] = {
    "1a-bfs": ("P1a - Breadth First Search", "bfs.py"),
    "1b-dfs": ("P1b - Iterative Depth First Search", "dfs.py"),
    "2a-a-star": ("P2a - A* Search", "a_star.py"),
    "2b-rbfs": ("P2b - Recursive Best-First Search", "rbfs.py"),
    "3-decision-tree": ("P3 - Decision Tree Learning", "decision_tree.py"),
    "4-neural-network": ("P4 - Feedforward Backprop NN", "neural_network.py"),
    "5-svm": ("P5 - Support Vector Machine", "svm.py"),
    "6-adaboost": ("P6 - AdaBoost Ensemble", "adaboost.py"),
    "7-naive-bayes": ("P7 - Naive Bayes Classifier", "naive_bayes.py"),
    "8-knn": ("P8 - K-Nearest Neighbors", "knn.py"),
    "9-association-rules": ("P9 - Association Rule Mining", "association_rules.py"),
    "10-tensorflow-demo": ("P10 - TensorFlow Demo", "tensorflow_demo.py"),
}

# Shared helper copied alongside practicals that need it (slug -> extra files).
EXTRA_FILES: Dict[str, Tuple[str, ...]] = {
    "1a-bfs": ("RMP.py",),
    "1b-dfs": ("RMP.py",),
    "2a-a-star": ("RMP.py",),
    "2b-rbfs": ("RMP.py",),
}


def _read_template(filename: str) -> str:
    return res.files("nmp").joinpath(f"templates/{filename}").read_text(encoding="utf-8")


def available_templates() -> List[str]:
    """Return template slugs in practical order (e.g. ['1a-bfs', ...])."""
    return list(PRACTICALS)


def file(
    name: str,
    output_dir: Union[str, Path] = ".",
    filename: Optional[str] = None,
    force: bool = False,
) -> Path:
    """Instantiate a practical file from a template slug.

    Parameters:
        name: Template slug (e.g., '1a-bfs').
        output_dir: Directory where the file should be generated (default: '.').
        filename: Custom destination filename. Defaults to the template's
                  filename (e.g., 'bfs.py').
        force: If True, overwrite existing files. Defaults to False.

    Returns:
        Path object pointing to the created file.

    Raises:
        ValueError: If `name` is empty or invalid.
        TemplateNotFoundError: If the requested template does not exist.
        TargetFileExistsError: If destination file exists and `force` is False.
    """
    if not name or not isinstance(name, str):
        raise ValueError("Template name must be a non-empty string (e.g., '1a-bfs').")

    slug = name.strip()
    if slug.endswith(".py"):
        slug = slug[:-3]
    if slug not in PRACTICALS:
        available = ", ".join(PRACTICALS)
        raise TemplateNotFoundError(
            f"Template '{name}' not found. Available templates: {available}"
        )

    _, template_file = PRACTICALS[slug]
    out_filename = filename.strip() if filename and filename.strip() else template_file
    if not out_filename.endswith(".py"):
        out_filename = f"{out_filename}.py"

    dest_dir = Path(output_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / out_filename

    if dest_path.exists() and not force:
        raise TargetFileExistsError(
            f"Target file already exists: '{dest_path}'. Use force=True (or answer y) to overwrite."
        )

    dest_path.write_text(_read_template(template_file), encoding="utf-8")

    for extra in EXTRA_FILES.get(slug, ()):
        extra_dest = dest_dir / extra
        if extra_dest.exists():
            continue  # never overwrite shared helper silently
        extra_dest.write_text(_read_template(extra), encoding="utf-8")

    return dest_path.resolve()
