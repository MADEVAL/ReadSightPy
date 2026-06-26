# Changelog

All notable changes to ReadSightPy will be documented in this file.

## [1.0.0] - 2026-06-26

### Added
- Initial release — Python port of ReadSight (PHP)
- Frank M. Liang (TeX) hyphenation algorithm for syllable counting
- 86 languages across 19 writing systems
- 17 readability formulas:
  Flesch Reading Ease, Flesch-Kincaid Grade Level, Gunning Fog, SMOG,
  Coleman-Liau, ARI, LIX, Gulpease, Wiener Sachtextformel (4 variants),
  Fernandez Huerta, Szigriszt-Pazos, Gutierrez Polini, Crawford,
  Fog-PL, Dale-Chall, Spache, Osman
- Composite syllable counter (heuristic + TeX fallback)
- JSON pattern cache via `platformdirs`
- Language-specific formula coefficients
- Text analysis (word/sentence/letter/syllable counts, syllable histogram)
- User-defined hyphenation overrides
- Interactive demo CLI
- `mypy` strict mode type checking (0 errors)
- `ruff` lint & format (0 errors)
- Python 3.10+ support
- Zero runtime dependencies beyond `regex` and `platformdirs`
- GitHub Actions CI pipeline
- 133 tests (unit + integration)
