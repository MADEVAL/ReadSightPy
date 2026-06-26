from __future__ import annotations

from .config import Config
from .exceptions import UnsupportedFormulaException
from .formula.formula_registry import FormulaRegistry
from .formula.formula_registry_factory import FormulaRegistryFactory
from .formula.formula_result import FormulaResult
from .formula.wiener_sachtextformel import WienerSachtextformel
from .hyphenation.cache.json_pattern_cache import JsonPatternCache
from .hyphenation.hyphenator import Hyphenator
from .hyphenation.liang_hyphenator import LiangHyphenator
from .hyphenation.source.tex_source import TexSource
from .language.json_language_repository import JsonLanguageRepository
from .language.language import Language
from .syllable.composite_syllable_counter import CompositeSyllableCounter
from .syllable.heuristic_syllable_counter import HeuristicSyllableCounter
from .syllable.syllable_counter import SyllableCounter
from .syllable.tex_syllable_counter import TexSyllableCounter
from .text.text_analyzer import TextAnalyzer
from .text.text_splitter import TextSplitter
from .text.text_statistics import TextStatistics


class ReadSight:
    _default_config: Config | None = None

    __slots__ = (
        "_formula_registry",
        "_hyphenator",
        "_language",
        "_syllable_counter",
        "_text",
    )

    def __init__(
        self,
        language: str,
        patterns_dir: str | None = None,
        languages_dir: str | None = None,
        cache_dir: str | None = None,
    ) -> None:
        config = self._resolve_config(patterns_dir, languages_dir, cache_dir)

        language_repository = JsonLanguageRepository(config.languages_dir)
        self._language = language_repository.find(language)

        self._hyphenator = self._load_hyphenator(self._language, config.patterns_dir, config.cache_dir)
        self._syllable_counter = self._load_syllable_counter()
        text_splitter = TextSplitter(self._language)

        self._text = TextAnalyzer(self._hyphenator, self._syllable_counter, text_splitter, self._language)
        self._formula_registry = FormulaRegistryFactory.create()

    @classmethod
    def with_config(cls, language: str, config: Config) -> ReadSight:
        return cls(language, config.patterns_dir, config.languages_dir, config.cache_dir)

    # --- Static configuration ---

    @classmethod
    def set_default_config(cls, config: Config) -> None:
        cls._default_config = config

    @classmethod
    def set_default_cache_dir(cls, directory: str) -> None:
        prev = cls._default_config or Config.default()
        cls._default_config = Config(prev.patterns_dir, prev.languages_dir, directory)

    @classmethod
    def set_default_patterns_dir(cls, directory: str) -> None:
        prev = cls._default_config or Config.default()
        cls._default_config = Config(directory, prev.languages_dir, prev.cache_dir)

    @classmethod
    def set_default_languages_dir(cls, directory: str) -> None:
        prev = cls._default_config or Config.default()
        cls._default_config = Config(prev.patterns_dir, directory, prev.cache_dir)

    @classmethod
    def get_supported_languages(cls, config: Config | None = None) -> list[str]:
        languages_dir = (config or cls._default_config or Config.default()).languages_dir
        return JsonLanguageRepository(languages_dir).list_codes()

    # --- Accessors ---

    @property
    def language(self) -> Language:
        return self._language

    @property
    def hyphenator(self) -> Hyphenator:
        return self._hyphenator

    @property
    def formula_registry(self) -> FormulaRegistry:
        return self._formula_registry

    def get_supported_formulas(self) -> list[str]:
        return self._formula_registry.list_for_language(self._language)

    # --- Text / Syllable API ---

    def split_word(self, word: str) -> list[str]:
        return self._text.split_word(word)

    def split_syllables(self, word: str) -> list[str]:
        return self._text.split_syllables(word)

    def syllable_count(self, word: str) -> int:
        return self._text.syllable_count(word)

    def word_count(self, text: str) -> int:
        return self._text.word_count(text)

    def sentence_count(self, text: str) -> int:
        return self._text.sentence_count(text)

    def letter_count(self, text: str) -> int:
        return self._text.letter_count(text)

    def total_syllables(self, text: str) -> int:
        return self._text.total_syllables(text)

    def average_syllables_per_word(self, text: str) -> float:
        return self._text.average_syllables_per_word(text)

    def average_words_per_sentence(self, text: str) -> float:
        return self._text.average_words_per_sentence(text)

    def polysyllable_count(self, text: str, count_proper_nouns: bool = True) -> int:
        return self._text.polysyllable_count(text, count_proper_nouns)

    def words_with_more_than_n_syllables(
        self, text: str, n: int, count_proper_nouns: bool = True
    ) -> int:
        return self._text.words_with_more_than_n_syllables(text, n, count_proper_nouns)

    def histogram_syllables(self, text: str) -> dict[int, int]:
        return self._text.histogram_syllables(text)

    def analyze(self, text: str) -> TextStatistics:
        return self._text.analyze(text)

    def add_hyphenations(self, hyphenations: dict[str, str]) -> None:
        self._text.add_hyphenations(hyphenations)

    # --- Formula API ---

    def score(self, formula_name: str, text: str) -> FormulaResult:
        return self._formula_registry.calculate(formula_name, self._language, self.analyze(text))

    def flesch_reading_ease(self, text: str) -> FormulaResult:
        return self.score("flesch_reading_ease", text)

    def flesch_kincaid_grade_level(self, text: str) -> FormulaResult:
        return self.score("flesch_kincaid_grade_level", text)

    def gunning_fog(self, text: str) -> FormulaResult:
        return self.score("gunning_fog", text)

    def smog_index(self, text: str) -> FormulaResult:
        return self.score("smog", text)

    def coleman_liau(self, text: str) -> FormulaResult:
        return self.score("coleman_liau", text)

    def automated_readability_index(self, text: str) -> FormulaResult:
        return self.score("ari", text)

    def lix(self, text: str) -> FormulaResult:
        return self.score("lix", text)

    def wiener_sachtextformel(self, text: str, variant: int = 1) -> FormulaResult:
        stats = self.analyze(text)
        formula = self._formula_registry.get("wiener_sachtextformel")
        if isinstance(formula, WienerSachtextformel):
            return formula.calculate_variant(stats, self._language, variant)
        raise UnsupportedFormulaException.for_language("wiener_sachtextformel", self._language.code)

    def gulpease(self, text: str) -> FormulaResult:
        return self.score("gulpease", text)

    def fernandez_huerta(self, text: str) -> FormulaResult:
        return self.score("fernandez_huerta", text)

    def szigriszt_pazos(self, text: str) -> FormulaResult:
        return self.score("szigriszt_pazos", text)

    def gutierrez_polini(self, text: str) -> FormulaResult:
        return self.score("gutierrez_polini", text)

    def crawford(self, text: str) -> FormulaResult:
        return self.score("crawford", text)

    def fog_pl(self, text: str) -> FormulaResult:
        return self.score("fog_pl", text)

    def dale_chall(self, text: str) -> FormulaResult:
        return self.score("dale_chall", text)

    def spache(self, text: str) -> FormulaResult:
        return self.score("spache", text)

    def osman(self, text: str) -> FormulaResult:
        return self.score("osman", text)

    # --- Private helpers ---

    @classmethod
    def _resolve_config(
        cls, patterns_dir: str | None, languages_dir: str | None, cache_dir: str | None
    ) -> Config:
        default = cls._default_config or Config.default()
        return Config(
            patterns_dir=patterns_dir or default.patterns_dir,
            languages_dir=languages_dir or default.languages_dir,
            cache_dir=cache_dir or default.cache_dir,
        )

    def _load_syllable_counter(self) -> SyllableCounter:
        tex = TexSyllableCounter(self._hyphenator)
        mode = self._language.syllable_mode

        if mode == "tex" or self._language.syllable_heuristics is None:
            return tex

        heuristic = HeuristicSyllableCounter(self._language.syllable_heuristics)

        if mode == "heuristic":
            return heuristic

        return CompositeSyllableCounter([heuristic, tex])

    @staticmethod
    def _load_hyphenator(language: Language, patterns_dir: str, cache_dir: str) -> Hyphenator:
        cache = JsonPatternCache(cache_dir)
        language_code = language.code

        if cache.has(language_code):
            cached = cache.get(language_code)
            if cached is not None:
                return LiangHyphenator(
                    cached["patterns"],
                    cached["exceptions"],
                    language.min_hyphen_left,
                    language.min_hyphen_right,
                )

        tex_file = f"{patterns_dir}/hyph-{language_code}.tex"
        source = TexSource(tex_file)
        loaded = source.load()

        cache.set(language_code, loaded)

        return LiangHyphenator(
            loaded["patterns"],
            loaded["exceptions"],
            language.min_hyphen_left,
            language.min_hyphen_right,
        )
