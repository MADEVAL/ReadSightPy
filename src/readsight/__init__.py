"""
ReadSight - Multilingual Readability Library for Python.

86 languages, 17 readability formulas, TeX-based syllable counting
via the Frank M. Liang hyphenation algorithm.
"""

from __future__ import annotations

from .config import Config
from .engine import ReadSight
from .exceptions import (
    EmptyTextException,
    ReadabilityEngineException,
    UnsupportedFormulaException,
    UnsupportedLanguageException,
)
from .formula.formula_result import FormulaResult
from .language.language import Language
from .language.script import Script
from .text.text_statistics import TextStatistics

__version__ = "1.0.0"
__all__ = [
    "Config",
    "EmptyTextException",
    "FormulaResult",
    "Language",
    "ReadSight",
    "ReadabilityEngineException",
    "Script",
    "TextStatistics",
    "UnsupportedFormulaException",
    "UnsupportedLanguageException",
]
