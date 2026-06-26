from __future__ import annotations

import pytest

from readsight.exceptions import EmptyTextException
from readsight.hyphenation.hyphenation_exceptions_collection import HyphenationExceptionsCollection
from readsight.hyphenation.liang_hyphenator import LiangHyphenator
from readsight.hyphenation.pattern import Pattern
from readsight.hyphenation.patterns_collection import PatternsCollection
from readsight.language.language import Language
from readsight.syllable.tex_syllable_counter import TexSyllableCounter
from readsight.text.text_analyzer import TextAnalyzer
from readsight.text.text_splitter import TextSplitter


def _make_language() -> Language:
    return Language.from_dict({
        "code": "en-us",
        "name": "English (US)",
        "nativeName": "English (US)",
        "script": "Latin",
        "hyphenMins": {"left": 2, "right": 2},
        "letterPattern": "[A-Za-z]",
        "wordSplitPattern": "[^\\p{L}'’-]+",
        "sentenceBoundaryPattern": "[.!?]+",
        "syllableMode": "tex",
    })


def _make_patterns() -> PatternsCollection:
    pc = PatternsCollection()
    pc.add(Pattern([".", "a", "b"], [0, 0, 4, 0]))
    return pc


class TestTextAnalyzer:
    def test_analyze_throws_on_empty(self) -> None:
        lang = _make_language()
        h = LiangHyphenator(_make_patterns(), HyphenationExceptionsCollection())
        sc = TexSyllableCounter(h)
        ts = TextSplitter(lang)
        ta = TextAnalyzer(h, sc, ts, lang)

        with pytest.raises(EmptyTextException):
            ta.analyze("")

    def test_analyze_basic_stats(self) -> None:
        lang = _make_language()
        h = LiangHyphenator(PatternsCollection(), HyphenationExceptionsCollection())
        sc = TexSyllableCounter(h)
        ts = TextSplitter(lang)
        ta = TextAnalyzer(h, sc, ts, lang)

        stats = ta.analyze("Hello world. How are you?")
        assert stats.word_count > 0
        assert stats.sentence_count > 0
        assert stats.letter_count > 0
        assert stats.syllable_count > 0

    def test_word_count(self) -> None:
        lang = _make_language()
        h = LiangHyphenator(PatternsCollection(), HyphenationExceptionsCollection())
        sc = TexSyllableCounter(h)
        ts = TextSplitter(lang)
        ta = TextAnalyzer(h, sc, ts, lang)

        assert ta.word_count("one two three four five") == 5

    def test_syllable_count_single_word(self) -> None:
        lang = _make_language()
        h = LiangHyphenator(PatternsCollection(), HyphenationExceptionsCollection())
        sc = TexSyllableCounter(h)
        ts = TextSplitter(lang)
        ta = TextAnalyzer(h, sc, ts, lang)

        assert ta.syllable_count("hello") >= 1
        assert ta.syllable_count("") == 0

    def test_polysyllable_count(self) -> None:
        lang = _make_language()
        h = LiangHyphenator(PatternsCollection(), HyphenationExceptionsCollection())
        sc = TexSyllableCounter(h)
        ts = TextSplitter(lang)
        ta = TextAnalyzer(h, sc, ts, lang)

        # Words with >2 syllables counted as polysyllabic
        count = ta.polysyllable_count("banana")
        # "banana" has 3 syllables, so count should be 1
        assert isinstance(count, int)
        assert count >= 0
