from __future__ import annotations

from readsight.syllable.heuristic_syllable_counter import HeuristicSyllableCounter

_EN_CONFIG: dict = {
    "vowelPattern": "[aeiouy]",
    "problemWords": {
        "banana": 3,
        "beautiful": 3,
    },
    "subtractPatterns": ["cial", "tia"],
    "addPatterns": ["ia", "io"],
    "prefixes": {"un": 1, "pre": 1},
    "suffixes": {"ly": 1, "ing": 1},
}


class TestHeuristicSyllableCounter:
    def test_problem_words(self) -> None:
        hc = HeuristicSyllableCounter(_EN_CONFIG)
        assert hc.count_syllables("banana") == 3
        assert hc.count_syllables("beautiful") == 3

    def test_prefix_count(self) -> None:
        hc = HeuristicSyllableCounter(_EN_CONFIG)
        assert hc.count_syllables("unfair") >= 2

    def test_suffix_count(self) -> None:
        hc = HeuristicSyllableCounter(_EN_CONFIG)
        assert hc.count_syllables("kindly") >= 2

    def test_empty_word(self) -> None:
        hc = HeuristicSyllableCounter(_EN_CONFIG)
        assert hc.count_syllables("") == 0
        assert hc.count_syllables("   ") == 0

    def test_has_rules(self) -> None:
        hc = HeuristicSyllableCounter(_EN_CONFIG)
        assert hc.has_rules() is True

    def test_no_rules(self) -> None:
        hc = HeuristicSyllableCounter(None)
        assert hc.has_rules() is False

    def test_has_word(self) -> None:
        hc = HeuristicSyllableCounter(_EN_CONFIG)
        assert hc.has_word("banana") is True
        assert hc.has_word("unknownword") is False

    def test_split_syllables(self) -> None:
        hc = HeuristicSyllableCounter(_EN_CONFIG)
        parts = hc.split_syllables("banana")
        assert len(parts) == 3
        assert "".join(parts) == "banana"

    def test_split_single_syllable(self) -> None:
        hc = HeuristicSyllableCounter(None)
        parts = hc.split_syllables("cat")
        assert parts == ["cat"]

    def test_minimum_one_syllable(self) -> None:
        hc = HeuristicSyllableCounter(None)
        assert hc.count_syllables("bcdfg") == 1
