from __future__ import annotations

from readsight.hyphenation.hyphenation_exceptions_collection import HyphenationExceptionsCollection
from readsight.hyphenation.hyphenation_override import HyphenationOverride
from readsight.hyphenation.liang_hyphenator import LiangHyphenator
from readsight.hyphenation.pattern import Pattern
from readsight.hyphenation.patterns_collection import PatternsCollection


def _make_minimal_patterns() -> PatternsCollection:
    """Build minimal patterns matching the hyph-en-minimal.pat.txt fixture."""
    pc = PatternsCollection()
    pc.add(Pattern([".", "a", "b"], [0, 0, 4, 0]))
    pc.add(Pattern(["a", "b", "a", "n"], [0, 5, 0, 0, 0]))
    pc.add(Pattern([".", "a", "b", "r"], [0, 0, 4, 0, 0]))
    pc.add(Pattern([".", "a", "b", "e"], [0, 0, 0, 2, 0]))
    pc.add(Pattern([".", "b", "e"], [0, 0, 3, 0]))
    pc.add(Pattern([".", "e", "d"], [0, 2, 0, 0]))
    pc.add(Pattern([".", "e", "d"], [0, 0, 4, 0]))  # note: last .e4d overrides .e2d
    pc.add(Pattern(["e", "d", "i"], [0, 2, 0, 0]))
    return pc


def _make_minimal_exceptions() -> HyphenationExceptionsCollection:
    ec = HyphenationExceptionsCollection()
    ec.add(HyphenationOverride("associate", "as-so-ci-ate"))
    ec.add(HyphenationOverride("table", "ta-ble"))
    ec.add(HyphenationOverride("recognize", "rec-og-nize"))
    return ec


class TestLiangHyphenator:
    def test_empty_word(self) -> None:
        h = LiangHyphenator(_make_minimal_patterns(), HyphenationExceptionsCollection())
        assert h.hyphenate("") == []
        assert h.count_syllables("") == 0

    def test_short_word_below_minimum(self) -> None:
        h = LiangHyphenator(_make_minimal_patterns(), HyphenationExceptionsCollection())
        assert h.hyphenate("ab") == ["ab"]

    def test_exception_word_associate(self) -> None:
        h = LiangHyphenator(PatternsCollection(), _make_minimal_exceptions())
        result = h.hyphenate("associate")
        assert result == ["as", "so", "ci", "ate"]
        assert h.count_syllables("associate") == 4

    def test_exception_word_table(self) -> None:
        h = LiangHyphenator(PatternsCollection(), _make_minimal_exceptions())
        result = h.hyphenate("table")
        assert result == ["ta", "ble"]

    def test_user_hyphenation_overrides(self) -> None:
        h = LiangHyphenator(_make_minimal_patterns(), HyphenationExceptionsCollection())
        h.add_hyphenations({"banana": "ba-na-na"})
        result = h.hyphenate("banana")
        assert result == ["ba", "na", "na"]

    def test_user_hyphenation_case_insensitive(self) -> None:
        h = LiangHyphenator(_make_minimal_patterns(), HyphenationExceptionsCollection())
        h.add_hyphenations({"Hello": "Hel-lo"})
        result = h.hyphenate("HELLO")
        assert len(result) == 2

    def test_single_syllable_word(self) -> None:
        h = LiangHyphenator(_make_minimal_patterns(), HyphenationExceptionsCollection())
        result = h.hyphenate("test")
        assert len(result) >= 1
        assert h.count_syllables("test") >= 1

    def test_counts_syllables(self) -> None:
        h = LiangHyphenator(PatternsCollection(), _make_minimal_exceptions())
        assert h.count_syllables("table") == 2
        assert h.count_syllables("associate") == 4
