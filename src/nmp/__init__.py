"""nmp: Quick practical file generation from templates."""

from nmp import mk
from nmp.mk import (
    NMPError,
    TargetFileExistsError,
    TemplateNotFoundError,
    available_templates,
    file,
)

__version__ = "0.1.0"

__all__ = [
    "mk",
    "file",
    "available_templates",
    "NMPError",
    "TemplateNotFoundError",
    "TargetFileExistsError",
    "__version__",
]
