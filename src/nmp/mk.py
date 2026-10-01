"""Core logic for discovering and generating practical files from templates."""

import shutil
from pathlib import Path
from typing import List, Optional, Union


class NMPError(Exception):
    """Base exception for all nmp-notes library errors."""


class TemplateNotFoundError(NMPError, FileNotFoundError):
    """Raised when a requested template does not exist."""


class TargetFileExistsError(NMPError, FileExistsError):
    """Raised when the target output file already exists and force=False."""


def _get_template_root() -> Path:
    """Return the absolute filesystem path to the templates directory."""
    return Path(__file__).resolve().parent / "templates"


def available_templates() -> List[str]:
    """Dynamically scan the templates folder and return available template identifiers.

    Returns:
        Sorted list of template names in dot notation (e.g. ['ai.p1', 'dbms.p1']).
    """
    root = _get_template_root()
    if not root.is_dir():
        return []

    templates: List[str] = []
    for file_path in root.rglob("*.py"):
        # Ignore private files, dunder files, and cache directories (e.g. __init__.py, __pycache__)
        if any(part.startswith(("_", ".")) for part in file_path.parts):
            continue

        rel_path = file_path.relative_to(root).with_suffix("")
        template_name = ".".join(rel_path.parts)
        templates.append(template_name)

    return sorted(templates)


def file(
    name: str,
    output_dir: Union[str, Path] = ".",
    filename: Optional[str] = None,
    force: bool = False,
) -> Path:
    """Instantiate a practical file from a dot-notation template name.

    Parameters:
        name: Dot-notation template identifier (e.g., 'ai.p1').
        output_dir: Directory where the file should be generated (default: '.').
        filename: Custom destination filename. If None, defaults to '<name_with_underscores>.py'
                  (e.g., 'ai_p1.py').
        force: If True, overwrite existing destination file. Defaults to False.

    Returns:
        Path object pointing to the created file.

    Raises:
        ValueError: If `name` is empty or invalid.
        TemplateNotFoundError: If the requested template does not exist.
        TargetFileExistsError: If destination file exists and `force` is False.
    """
    if not name or not isinstance(name, str):
        raise ValueError("Template name must be a non-empty string (e.g., 'ai.p1').")

    # Clean name and strip optional trailing extension
    clean_name = name.strip()
    if clean_name.endswith(".py"):
        clean_name = clean_name[:-3]

    parts = [part.strip() for part in clean_name.split(".") if part.strip()]
    if not parts:
        raise ValueError(f"Invalid template name: '{name}'. Expected dot notation like 'ai.p1'.")

    root = _get_template_root()
    rel_template_path = Path(*parts).with_suffix(".py")
    template_path = (root / rel_template_path).resolve()

    # Prevent directory traversal attacks
    try:
        template_path.relative_to(root.resolve())
    except ValueError:
        raise ValueError(f"Template path '{name}' resolves outside the template directory.")

    if not template_path.is_file():
        available = available_templates()
        suggestions = f" Available templates: {', '.join(available)}" if available else " No templates currently found."
        raise TemplateNotFoundError(
            f"Template '{name}' not found at '{template_path.name}'.{suggestions}"
        )

    # Determine destination filename
    if filename:
        clean_filename = filename.strip()
        out_filename = clean_filename if clean_filename.endswith(".py") else f"{clean_filename}.py"
    else:
        out_filename = f"{'_'.join(parts)}.py"

    dest_dir = Path(output_dir).resolve()
    dest_path = dest_dir / out_filename

    if dest_path.exists() and not force:
        raise TargetFileExistsError(
            f"Target file already exists: '{dest_path}'. Use force=True (or --force flag) to overwrite."
        )

    # Ensure parent directory exists
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Copy template code to destination
    shutil.copyfile(template_path, dest_path)

    return dest_path
