"""
mdforge -- a reusable, extensible framework for analysing GROMACS molecular
dynamics simulations of arbitrary biomolecular systems.

Point it at a simulation directory and it will discover the files, detect the
system composition (protein / ligand / nucleic acid / membrane / ions / ...),
select the appropriate analyses, run them with streaming-friendly performance,
and produce publication-quality figures plus a fully reproducible report.

Public API
----------
    from mdforge import analyze, detect_system, __version__
"""

from __future__ import annotations

__version__ = "0.2.1"
__author__ = "Hossam Mahmoud"

# Re-export the most commonly used entry points (kept import-light).
from mdforge.core.system import detect_system, SystemInfo, SystemType, ComponentType  # noqa: E402
from mdforge.core.registry import registry  # noqa: E402

__all__ = [
    "__version__",
    "detect_system",
    "SystemInfo",
    "SystemType",
    "ComponentType",
    "registry",
    "analyze",
]


def analyze(*args, **kwargs):
    """Convenience wrapper around :func:`mdforge.core.pipeline.run_pipeline`."""
    from mdforge.core.pipeline import run_pipeline
    return run_pipeline(*args, **kwargs)
