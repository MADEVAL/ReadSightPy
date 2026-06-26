# ReadSightPy - Multilingual Readability Engine for Python

[![Python](https://img.shields.io/badge/Python-%3E%3D%203.10-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-85%20passed-brightgreen)](https://github.com/MADEVAL/ReadSightPy)
[![Mypy](https://img.shields.io/badge/mypy-strict-brightgreen)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/badge/ruff-lint%20format-brightgreen)](https://astral.sh/ruff)
[![Languages](https://img.shields.io/badge/languages-86-9cf)](https://github.com/MADEVAL/ReadSightPy)
[![Formulas](https://img.shields.io/badge/formulas-17-orange)](https://github.com/MADEVAL/ReadSightPy)

ReadSightPy is a Python library for measuring text readability across **86 languages**. It implements **17 readability formulas** with language-specific coefficients and uses the Frank M. Liang (TeX) hyphenation algorithm for accurate syllable counting.

This is a Python port of [ReadSight](https://github.com/MADEVAL/ReadSight) (PHP).

## Installation

```bash
pip install readsight
```

**Requirements:**
- Python >= 3.10
- `regex` (for Unicode regex support)
- `platformdirs` (for cache directory)

## Quick Start

```python
from readsight import ReadSight

rs = ReadSight("en-us")

# Syllable counting
rs.syllable_count("banana")         # 3
rs.split_word("hyphenation")        # ['hy', 'phen', 'a', 'tion']

# Text analysis
stats = rs.analyze("The quick brown fox jumps over the lazy dog.")
print(f"Words: {stats.word_count}, Syllables: {stats.syllable_count}")

# Readability formulas
fre = rs.flesch_reading_ease(text)
print(f"Flesch Reading Ease: {fre.score} - {fre.interpretation}")

fog = rs.gunning_fog(text)
print(f"Gunning Fog: {fog.score} (grade {fog.grade_level})")

lix = rs.lix(text)
print(f"LIX: {lix.score} - {lix.interpretation}")
```

## Demo

```bash
python examples/demo.py
```

## Supported Languages

86 languages across **19 writing systems**: Latin, Cyrillic, Arabic, Hebrew, Devanagari, Bengali, Tamil, Thai, Greek, Armenian, Georgian, Gujarati, Gurmukhi, Kannada, Malayalam, Odia, Telugu, Ethiopic, Coptic.

```python
rs = ReadSight("ru")        # Russian
rs = ReadSight("de-1996")   # German (1996 reform)
rs = ReadSight("es")        # Spanish
rs = ReadSight("th")        # Thai

# List all supported languages
langs = ReadSight.get_supported_languages()
# ['af', 'ar', 'as', 'be', 'bg', 'bn', 'ca', 'cop', 'cs', ...
```

## Readability Formulas

### Universal (all 86 languages)

| Formula | Method | Type | Score Range |
|---|---|---|---|
| Gunning Fog | `gunning_fog()` | Syllable-based | 0-20+ |
| SMOG Index | `smog_index()` | Syllable-based | 3-18+ |
| Coleman-Liau | `coleman_liau()` | Letter-based | 0-18+ |
| ARI | `automated_readability_index()` | Letter-based | 0-18+ |
| LIX | `lix()` | Letter-based | 20-60+ |

### Language-Specific

| Language | Formulas |
|---|---|
| English (`en-us`, `en-gb`) | Flesch Reading Ease, FK Grade Level, Dale-Chall, Spache |
| German (`de-*`) | Flesch Reading Ease (Amstad), FKGL, Wiener Sachtextformel (4 variants) |
| Russian (`ru`) | Flesch Reading Ease (Oborneva), FKGL |
| Spanish (`es`) | Flesch Reading Ease, Fernandez-Huerta, Szigriszt-Pazos, Gutierrez-Polini, Crawford |
| Italian (`it`) | Flesch Reading Ease, Gulpease |
| French (`fr`) | Flesch Reading Ease (Kandel-Moles) |
| Dutch (`nl`) | Flesch Reading Ease (Douma) |
| Portuguese (`pt`) | Flesch Reading Ease (Martins) |
| Turkish (`tr`) | Flesch Reading Ease (Ateşman) |
| Polish (`pl`) | FOG-PL |
| Arabic (`ar`) | OSMAN |

## FormulaResult

```python
result.score           # float - raw formula score
result.grade_level     # float | None - normalized grade level
result.interpretation  # str - qualitative interpretation ("Easy", "Hard")
result.formula_name    # str - formula key
result.language_code   # str - language code used
result.inputs          # dict[str, float|int] - intermediate values
```

## Architecture

```
ReadSight (facade)
  ├── TextAnalyzer
  │   ├── SyllableCounter (tex | heuristic | composite)
  │   │   ├── CompositeSyllableCounter
  │   │   ├── HeuristicSyllableCounter (vowel patterns + word list)
  │   │   └── TexSyllableCounter → LiangHyphenator (TeX hyphenation)
  │   ├── LiangHyphenator (Frank M. Liang algorithm)
  │   │   ├── TexSource (parses .tex from hyph-utf8)
  │   │   ├── PatternsCollection
  │   │   ├── HyphenationExceptionsCollection
  │   │   └── JsonPatternCache
  │   └── TextSplitter (word/sentence/letter counting)
  ├── Language (JSON config per language)
  └── FormulaRegistry (17 formulas)
```

## Quality

| Metric | Value |
|---|---|
| Tests | **85** (unit + integration) |
| Mypy | **strict mode, 0 errors** |
| Ruff | **all checks pass** |
| Supported languages | 86 |
| Writing systems | 19 |
| Readability formulas | 17 |

## License

MIT. Author: Yevhen Leonidov.

TeX pattern files from hyph-utf8 are packaged under their original licenses.
