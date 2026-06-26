from __future__ import annotations

from readsight.hyphenation.hyphenation_exceptions_collection import HyphenationExceptionsCollection
from readsight.hyphenation.liang_hyphenator import LiangHyphenator
from readsight.hyphenation.pattern import Pattern
from readsight.hyphenation.patterns_collection import PatternsCollection
from readsight.syllable.composite_syllable_counter import CompositeSyllableCounter
from readsight.syllable.heuristic_syllable_counter import HeuristicSyllableCounter
from readsight.syllable.tex_syllable_counter import TexSyllableCounter


def _make_tex_counter() -> TexSyllableCounter:
    pc = PatternsCollection()
    pc.add(Pattern([".", "a", "b"], [0, 0, 4, 0]))
    lh = LiangHyphenator(pc, HyphenationExceptionsCollection())
    return TexSyllableCounter(lh)


class TestCompositeSyllableCounter:
    def test_uses_heuristic_when_has_rules(self) -> None:
        hc = HeuristicSyllableCounter({"vowelPattern": "[aeiouy]", "problemWords": {"test": 5}})
        tc = _make_tex_counter()
        composite = CompositeSyllableCounter([hc, tc])
        assert composite.count_syllables("test") == 5

    def test_falls_back_to_tex(self) -> None:
        hc = HeuristicSyllableCounter(None)
        tc = _make_tex_counter()
        composite = CompositeSyllableCounter([hc, tc])
        assert composite.count_syllables("test") >= 1

    def test_split_syllables_heuristic(self) -> None:
        hc = HeuristicSyllableCounter({"vowelPattern": "[aeiouy]", "problemWords": {"banana": 3}})
        tc = _make_tex_counter()
        composite = CompositeSyllableCounter([hc, tc])
        parts = composite.split_syllables("banana")
        assert len(parts) == 3

    def test_split_syllables_fallback(self) -> None:
        hc = HeuristicSyllableCounter(None)
        tc = _make_tex_counter()
        composite = CompositeSyllableCounter([hc, tc])
        parts = composite.split_syllables("test")
        assert len(parts) >= 1
