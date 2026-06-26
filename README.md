# ReadSightPy — Multilingual Readability Engine for Python

[![CI](https://github.com/MADEVAL/ReadSightPy/actions/workflows/ci.yml/badge.svg)](https://github.com/MADEVAL/ReadSightPy/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-%3E%3D%203.10-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-133%20passed-brightgreen)](https://github.com/MADEVAL/ReadSightPy)
[![Mypy](https://img.shields.io/badge/mypy-strict-brightgreen)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/badge/ruff-0%20errors-brightgreen)](https://astral.sh/ruff)
[![Languages](https://img.shields.io/badge/languages-86-9cf)](https://github.com/MADEVAL/ReadSightPy)
[![Formulas](https://img.shields.io/badge/formulas-17-orange)](https://github.com/MADEVAL/ReadSightPy)

ReadSightPy measures text readability across **86 languages** using **17 readability formulas** with language-specific coefficients. Syllable counting is powered by the **Frank M. Liang (TeX) hyphenation algorithm** — the same algorithm used by TeX for decades. All with **zero heavy dependencies**.

This is a Python port of [ReadSight](https://github.com/MADEVAL/ReadSight) (PHP).

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Demo](#demo)
- [Supported Languages](#supported-languages)
- [Readability Formulas](#readability-formulas)
- [FormulaResult](#formularesult)
- [Performance](#performance)
- [Custom Configuration](#custom-configuration)
- [Architecture](#architecture)
- [Data Sources](#data-sources)
- [Development](#development)
- [License](#license)

## Installation

```bash
pip install readsight
```

**Requirements:**
- Python >= 3.10
- `regex` (for Unicode regex `\p{L}` support)
- `platformdirs` (for cache directory)

No other runtime dependencies.

## Quick Start

```python
from readsight import ReadSight

rs = ReadSight("en-us")

# Syllable counting
rs.syllable_count("banana")         # 3
rs.split_syllables("hyphenation")   # ['hyp', 'hen', 'ati', 'on']  (4 syllables, heuristic split)
rs.split_word("hyphenation")        # ['hy', 'phen', 'a', 'tion']  (TeX hyphenation points)

# Text analysis
stats = rs.analyze("The quick brown fox jumps over the lazy dog.")
print(f"Words: {stats.word_count}, Syllables: {stats.syllable_count}")

# Readability formulas
fre = rs.flesch_reading_ease(text)
print(f"Flesch Reading Ease: {fre.score} - {fre.interpretation}")

fog = rs.gunning_fog(text)
print(f"Gunning Fog: {fre.score} (grade {fre.grade_level})")

lix = rs.lix(text)
print(f"LIX: {fre.score} - {fre.interpretation}")
```

## Syllable Counting Modes

ReadSightPy has three syllable counting modes, configured per language via `syllableMode` in `data/languages/*.json`:

| Mode | How it works | `count` accuracy | `split` accuracy |
|------|-------------|:---:|:---:|
| **`heuristic`** | Vowel patterns + word list + prefix/suffix rules | ✓ | ≈ approximate |
| **`tex`** | Frank M. Liang hyphenation algorithm (TeX `.tex` patterns) | ✓ | ✓ exact |
| **`composite`** | Heuristic first, TeX as fallback | ✓ | ≈ approximate (uses heuristic split) |

**80 languages use `tex`**, **4 use `composite`** (en-us, en-gb, it, pl), **2 use `heuristic`**.

### Example: "hyphenation" in each mode

```python
rs = ReadSight("en-us")   # composite mode — heuristic wins
rs.syllable_count("hyphenation")   # 4 ✓ (in problemWords list)
rs.split_syllables("hyphenation")  # ['hyp', 'hen', 'ati', 'on']   — heuristic: equal-width split, ≈ approximate
rs.split_word("hyphenation")       # ['hy', 'phen', 'a', 'tion']   — TeX hyphenator: exact points

rs = ReadSight("de-1996")  # tex mode
rs.syllable_count("hyphenation")   # 4 ✓ (TeX patterns)
rs.split_syllables("hyphenation")  # ['hy', 'phen', 'a', 'tion']   — TeX: exact
rs.split_word("hyphenation")       # ['hy', 'phen', 'a', 'tion']   — same, both use TeX
```

> **Tip:** `split_word()` always uses the TeX hyphenator (exact). `split_syllables()` may use heuristic (approximate). For syllable *counts* both are correct.

> **Note:** `add_hyphenations()` adds overrides to the TeX hyphenator. These affect `split_word()` but NOT `split_syllables()` in `composite`/`heuristic` modes (the heuristic counter doesn't see them).

## Demo

Run the interactive demo to see ReadSightPy in action:

```bash
python examples/demo.py
```

This analyzes built-in sample text and outputs:
- **Syllable breakdown** with hyphenation points for common words
- **Text statistics** — letters, words, sentences, syllables, histogram
- **All applicable readability formulas** with scores and interpretations

Compare the same text across 6 languages:

```bash
# Built into demo.py — runs multilingual comparison automatically
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
# ['af', 'ar', 'as', 'be', 'bg', 'bn', 'ca', 'cop', 'cs', 'cu', 'cy', 'da',
#  'de-1901', 'de-1996', 'de-ch-1901', 'el-monoton', 'el-polyton', 'en-gb',
#  'en-us', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fi-x-school', 'fr', 'fur',
#  'ga', 'gl', 'grc', 'gu', 'he', 'hi', 'hr', 'hsb', 'hu', 'hy', 'ia', 'id',
#  'is', 'it', 'ka', 'kk', 'kmr', 'kn', 'la', 'la-x-classic', 'la-x-liturgic',
#  'lt', 'lv', 'mk', 'ml', 'mn-cyrl', 'mn-cyrl-x-lmc', 'mr', 'mul-ethi', 'nb',
#  'nl', 'nn', 'oc', 'or', 'pa', 'pi', 'pl', 'pms', 'pt', 'rm', 'ro', 'ru',
#  'sa', 'sh-cyrl', 'sh-latn', 'sk', 'sl', 'sq', 'sr-cyrl', 'sv', 'ta', 'te',
#  'th', 'tk', 'tr', 'uk', 'vi', 'zh-latn-pinyin']
```

## Readability Formulas

### Universal (all 86 languages)

| Formula | Method | Type | Score Range |
|---|---|---|---|
| Gunning Fog | `gunning_fog()` | Syllable-based | 0–20+ |
| SMOG Index | `smog_index()` | Syllable-based | 3–18+ |
| Coleman-Liau | `coleman_liau()` | Letter-based | 0–18+ |
| ARI | `automated_readability_index()` | Letter-based | 0–18+ |
| LIX | `lix()` | Letter-based | 20–60+ |

### Language-Specific

| Language | Formulas |
|---|---|
| English (`en-us`, `en-gb`) | Flesch Reading Ease, FK Grade Level, Dale-Chall*, Spache* |
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

> **\*Note:** Dale-Chall and Spache formulas use a syllable-based heuristic to estimate difficult words (1-syllable ≈ easy). This is a simplified estimation, not based on the original Dale/Spache word lists.

Generic dispatching:

```python
result = rs.score("gunning_fog", text)
result = rs.score("wiener_sachtextformel", text)
```

## FormulaResult

```python
result.score           # float — raw formula score
result.grade_level     # float | None — normalized grade level (FKGL, GF, SMOG, CL, ARI)
result.interpretation  # str — qualitative interpretation ("Easy", "Hard")
result.formula_name    # str — formula key
result.language_code   # str — language code used
result.inputs          # dict[str, float | int] — intermediate values for debugging
```

### API Reference

#### Text Analysis Methods

```python
rs.syllable_count(word: str) -> int
rs.split_syllables(word: str) -> list[str]
rs.split_word(word: str) -> list[str]
rs.word_count(text: str) -> int
rs.sentence_count(text: str) -> int
rs.letter_count(text: str) -> int
rs.total_syllables(text: str) -> int
rs.average_syllables_per_word(text: str) -> float
rs.average_words_per_sentence(text: str) -> float
rs.polysyllable_count(text: str, count_proper_nouns: bool = True) -> int
rs.words_with_more_than_n_syllables(text: str, n: int, count_proper_nouns: bool = True) -> int
rs.histogram_syllables(text: str) -> dict[int, int]
rs.analyze(text: str) -> TextStatistics
```

> **split_syllables vs split_word:** `split_syllables` may use heuristic ≈approximate split (depends on language's `syllableMode`). `split_word` always uses the TeX hyphenator for exact hyphenation points. Syllable *counts* are accurate in all modes. See [Syllable Counting Modes](#syllable-counting-modes).

#### Formula Methods

```python
rs.flesch_reading_ease(text: str) -> FormulaResult
rs.flesch_kincaid_grade_level(text: str) -> FormulaResult
rs.gunning_fog(text: str) -> FormulaResult
rs.smog_index(text: str) -> FormulaResult
rs.coleman_liau(text: str) -> FormulaResult
rs.automated_readability_index(text: str) -> FormulaResult
rs.lix(text: str) -> FormulaResult
rs.wiener_sachtextformel(text: str, variant: int = 1) -> FormulaResult
rs.gulpease(text: str) -> FormulaResult
rs.fernandez_huerta(text: str) -> FormulaResult
rs.szigriszt_pazos(text: str) -> FormulaResult
rs.gutierrez_polini(text: str) -> FormulaResult
rs.crawford(text: str) -> FormulaResult
rs.fog_pl(text: str) -> FormulaResult
rs.dale_chall(text: str) -> FormulaResult
rs.spache(text: str) -> FormulaResult
rs.osman(text: str) -> FormulaResult
```

## Performance

Measured on CPython 3.12, Intel Core i7 (limited data — full benchmarks TBD):

| Operation | Time |
|---|---|
| Syllable counting (single word) | ~0.05 ms |
| Text analysis (45 words) | ~1 ms |
| Formula calculation (incl. analysis) | ~1 ms |
| Engine init (en-us, cached) | ~10 ms |
| Engine init (de-1996, first load) | ~60 ms |

Caching: compiled patterns are stored as JSON in the system cache directory (`platformdirs.user_cache_dir`). First load parses `.tex` files (native hyph-utf8 format); subsequent loads use the pre-compiled cache.

## Custom Configuration

```python
from readsight import ReadSight, Config

# Set default paths (before creating engines)
ReadSight.set_default_config(Config(
    patterns_dir="/custom/patterns",
    languages_dir="/custom/languages",
    cache_dir="/var/cache/readsight",
))

# Or per-instance
rs = ReadSight(
    language="en-us",
    patterns_dir="/custom/patterns",
    cache_dir="/custom/cache",
)

# Add custom hyphenation rules (affects split_word, not split_syllables)
rs.add_hyphenations({
    "customword": "cus-tom-word",
})
rs.split_word("customword")  # ['cus', 'tom', 'word']
```

## Architecture

```
ReadSight (facade)
  ├── TextAnalyzer (syllable counting, text metrics)
  │   ├── SyllableCounter (strategy: tex | heuristic | composite)
  │   │   ├── CompositeSyllableCounter (problemWords → heuristic, rest → TeX)
  │   │   ├── HeuristicSyllableCounter (vowel patterns + word list)
  │   │   └── TexSyllableCounter → LiangHyphenator (TeX hyphenation)
  │   ├── LiangHyphenator
  │   │   ├── TexSource (parses .tex from hyph-utf8)
  │   │   ├── PatternsCollection (pattern data)
  │   │   ├── HyphenationExceptionsCollection (word overrides)
  │   │   └── JsonPatternCache (compiled patterns)
  │   └── TextSplitter (word/sentence/letter counting)
  ├── Language (JSON config per language, syllableMode + formulaConfigs)
  └── FormulaRegistry (17 formulas)
      ├── FleschReadingEase (with lang-specific coefficients)
      ├── GunningFog, SMOG, ColemanLiau, ARI, LIX (universal)
      └── WSTF, Gulpease, Fernandez-Huerta, etc. (lang-specific)
```

## Data Sources

- **TeX hyphenation patterns**: [hyph-utf8](https://ctan.org/pkg/hyph-utf8) version 2026-02-21 —
  the canonical TeX hyphenation repository maintained by the TeX Users Group (TUG).
  86 `.tex` pattern files from hyph-utf8 covering 86 language variants.
  Packaged under each pattern file's original license.
- **FRE coefficients**: Amstad (DE), Oborneva (RU), Fernandez-Huerta (ES),
  Vacca-Franchina (IT), Kandel-Moles (FR), Douma (NL), Martins (PT), Ateşman (TR)
- **WSTF**: Bamberger & Vanecek (DE)
- **Gulpease**: GULP, La Sapienza University (IT)

## Development

```bash
pip install -e ".[dev]"    # Install with dev dependencies

pytest                     # Run all tests (133 tests)
pytest --cov=readsight     # With coverage report
mypy src/                  # Static type checking (strict mode)
ruff check src/ tests/     # Lint
ruff format src/ tests/    # Format
```

### Quality Metrics

| Metric | Value |
|---|---|
| Tests | **133** |
| Mypy | **Strict mode, 0 errors** |
| Ruff | **0 errors** |
| Source files | 56 |
| Test files | 18 |
| Supported languages | 86 |
| Writing systems | 19 |
| Readability formulas | 17 |
| Runtime dependencies | 2 (`regex`, `platformdirs`) |

## License

MIT. Author: Yevhen Leonidov.

TeX pattern files from hyph-utf8 are packaged under their original licenses (see individual file headers).
