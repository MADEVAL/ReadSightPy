from __future__ import annotations

from readsight.formula.automated_readability_index import AutomatedReadabilityIndex
from readsight.formula.coleman_liau import ColemanLiau
from readsight.formula.gunning_fog import GunningFog
from readsight.formula.lix import Lix
from readsight.formula.smog_index import SmogIndex
from readsight.language.language import Language
from readsight.text.text_statistics import TextStatistics


def _make_language(code: str = "en-us") -> Language:
    return Language.from_dict({
        "code": code,
        "name": "English (US)",
        "nativeName": "English (US)",
        "script": "Latin",
        "hyphenMins": {"left": 2, "right": 2},
        "letterPattern": "[A-Za-z]",
        "wordSplitPattern": "[^\\p{L}'’-]+",
        "sentenceBoundaryPattern": "[.!?]+",
        "formulas": {"lix": {"enabled": True, "longWordThreshold": 6}},
    })


def _make_stats(**overrides: float | int | dict[int, int]) -> TextStatistics:
    defaults: dict = {
        "letter_count": 200, "word_count": 50, "sentence_count": 5,
        "syllable_count": 75, "polysyllable_count": 5,
        "average_syllables_per_word": 1.5, "average_words_per_sentence": 10.0,
        "long_word_count": 8,
        "syllable_histogram": {1: 30, 2: 15, 3: 5},
    }
    defaults.update(overrides)
    return TextStatistics(**defaults)  # type: ignore[arg-type]


class TestGunningFog:
    def test_calculation(self) -> None:
        formula = GunningFog()
        stats = _make_stats()
        result = formula.calculate(stats, _make_language())
        assert result.formula_name == "gunning_fog"
        assert result.score > 0.0
        assert result.grade_level is not None
        assert "asl" in result.inputs

    def test_zero_words(self) -> None:
        formula = GunningFog()
        stats = _make_stats(word_count=0, average_words_per_sentence=0.0)
        result = formula.calculate(stats, _make_language())
        assert result.score == 0.0


class TestSmogIndex:
    def test_calculation(self) -> None:
        formula = SmogIndex()
        result = formula.calculate(_make_stats(), _make_language())
        assert result.score > 0.0
        assert result.grade_level is not None


class TestColemanLiau:
    def test_calculation(self) -> None:
        formula = ColemanLiau()
        result = formula.calculate(_make_stats(), _make_language())
        assert result.score != 0.0
        assert "L" in result.inputs
        assert "S" in result.inputs


class TestARI:
    def test_calculation(self) -> None:
        formula = AutomatedReadabilityIndex()
        result = formula.calculate(_make_stats(), _make_language())
        assert result.score != 0.0


class TestLix:
    def test_calculation(self) -> None:
        formula = Lix()
        result = formula.calculate(_make_stats(), _make_language())
        assert result.score > 0.0
        assert "longWordPct" in result.inputs

    def test_custom_threshold(self) -> None:
        formula = Lix()
        lang = _make_language("pl")
        lang_data = {
            "code": "pl", "name": "Polish", "nativeName": "Polski",
            "script": "Latin",
            "hyphenMins": {"left": 2, "right": 2},
            "letterPattern": "[A-Za-z]",
            "wordSplitPattern": "[^\\p{L}]+",
            "sentenceBoundaryPattern": "[.!?]+",
            "formulas": {"lix": {"enabled": True, "longWordThreshold": 4}},
        }
        lang = Language.from_dict(lang_data)
        result = formula.calculate(_make_stats(), lang)
        assert result.inputs["threshold"] == 4
