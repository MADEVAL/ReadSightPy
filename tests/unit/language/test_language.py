from __future__ import annotations

from readsight.language.language import Language
from readsight.language.script import Script


class TestLanguage:
    @staticmethod
    def _make_en_us_data() -> dict:
        return {
            "code": "en-us",
            "name": "English (US)",
            "nativeName": "English (US)",
            "script": "Latin",
            "hyphenMins": {"left": 2, "right": 2},
            "letterPattern": "[A-Za-z]",
            "wordSplitPattern": "[^\\p{L}]+",
            "sentenceBoundaryPattern": "[.!?]+",
            "formulas": {
                "gunning_fog": {"enabled": True},
                "flesch_reading_ease": {"enabled": True, "base": 206.835},
            },
            "syllableMode": "composite",
            "syllableHeuristics": {"vowelPattern": "[aeiouy]"},
        }

    def test_from_dict_basic(self) -> None:
        lang = Language.from_dict(self._make_en_us_data())
        assert lang.code == "en-us"
        assert lang.name == "English (US)"
        assert lang.script == Script.Latin
        assert lang.min_hyphen_left == 2
        assert lang.min_hyphen_right == 2
        assert lang.syllable_mode == "composite"

    def test_supports_formula(self) -> None:
        lang = Language.from_dict(self._make_en_us_data())
        assert lang.supports_formula("gunning_fog") is True
        assert lang.supports_formula("nonsense") is False

    def test_get_formula_config(self) -> None:
        lang = Language.from_dict(self._make_en_us_data())
        config = lang.get_formula_config("flesch_reading_ease")
        assert config is not None
        assert config["base"] == 206.835

    def test_get_formula_config_missing(self) -> None:
        lang = Language.from_dict(self._make_en_us_data())
        assert lang.get_formula_config("nonexistent") is None

    def test_get_supported_formulas(self) -> None:
        lang = Language.from_dict(self._make_en_us_data())
        formulas = lang.get_supported_formulas()
        assert "gunning_fog" in formulas
        assert "flesch_reading_ease" in formulas

    def test_default_syllable_mode(self) -> None:
        data = self._make_en_us_data()
        del data["syllableMode"]
        lang = Language.from_dict(data)
        assert lang.syllable_mode == "tex"

    def test_no_heuristics(self) -> None:
        data = self._make_en_us_data()
        del data["syllableHeuristics"]
        lang = Language.from_dict(data)
        assert lang.syllable_heuristics is None
