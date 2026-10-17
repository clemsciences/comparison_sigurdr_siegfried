"""Comparison between the *Nibelungenlied* and the *Völsunga saga*."""

from importlib.metadata import version
from pathlib import Path

__all__ = ["PACKAGE_DIR", "PACKDIR", "__version__"]

__version__ = version("sigurd")

#: Directory of the installed package, which also holds the bundled corpora.
PACKAGE_DIR = Path(__file__).resolve().parent

#: Kept for backward compatibility; prefer :data:`PACKAGE_DIR`.
PACKDIR = str(PACKAGE_DIR)
