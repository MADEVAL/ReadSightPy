from __future__ import annotations

from ..exceptions import EmptyTextException
from ..hyphenation.hyphenator import Hyphenator
from ..hyphenation.liang_hyphenator import LiangHyphenator
from ..language.language import Language
from ..syllable.syllable_counter import SyllableCounter
from .text_splitter import TextSplitter
from .text_statistics import TextStatistics


class TextAnalyzer:
    def __init__(
        self,
        hyphenator: Hyphenator,
        syllable_counter: SyllableCounter,
        text_splitter: TextSplitter,
        language: Language,
    ) -> None:
        self._hyphenator = hyphenator
        self._syllable_counter = syllable_counter
        self._text_splitter = text_splitter
        self._language = language

    def split_word(self, word: str) -> list[str]:
        return self._hyphenator.hyphenate(word)

    def split_syllables(self, word: str) -> list[str]:
        return self._syllable_counter.split_syllables(word)

    def syllable_count(self, word: str) -> int:
        return self._syllable_counter.count_syllables(word)

    def word_count(self, text: str) -> int:
        return self._text_splitter.count_words(text)

    def sentence_count(self, text: str) -> int:
        return self._text_splitter.count_sentences(text)

    def letter_count(self, text: str) -> int:
        return self._text_splitter.count_letters(text)

    def total_syllables(self, text: str) -> int:
        words = self._text_splitter.split_words(text)
        return sum(self._syllable_counter.count_syllables(w) for w in words)

    def average_syllables_per_word(self, text: str) -> float:
        words = self._text_splitter.split_words(text)
        word_count = len(words)
        if word_count == 0:
            return 0.0
        total = sum(self._syllable_counter.count_syllables(w) for w in words)
        return total / word_count

    def average_words_per_sentence(self, text: str) -> float:
        word_count = self._text_splitter.count_words(text)
        sentence_count = self._text_splitter.count_sentences(text)
        if sentence_count == 0:
            return float(word_count)
        return word_count / sentence_count

    def words_with_more_than_n_syllables(
        self, text: str, n: int, count_proper_nouns: bool = True
    ) -> int:
        words = self._text_splitter.split_words(text)
        count = 0
        for word in words:
            if self._syllable_counter.count_syllables(word) > n:
                if count_proper_nouns:
                    count += 1
                else:
                    first_letter = word[0]
                    if first_letter != first_letter.upper():
                        count += 1
        return count

    def polysyllable_count(self, text: str, count_proper_nouns: bool = True) -> int:
        return self.words_with_more_than_n_syllables(text, 2, count_proper_nouns)

    def histogram_syllables(self, text: str) -> dict[int, int]:
        words = self._text_splitter.split_words(text)
        histogram: dict[int, int] = {}
        for word in words:
            syllables = self._syllable_counter.count_syllables(word)
            if syllables == 0:
                continue
            histogram[syllables] = histogram.get(syllables, 0) + 1
        return dict(sorted(histogram.items()))

    def analyze(self, text: str) -> TextStatistics:
        text = text.strip()
        words = self._text_splitter.split_words(text)
        word_count = len(words)

        if word_count == 0:
            raise EmptyTextException.create()

        letter_count = self._text_splitter.count_letters(text)
        sentence_count = self._text_splitter.count_sentences(text)

        total_syllables = 0
        polysyllable_count = 0
        histogram: dict[int, int] = {}

        for word in words:
            syllables = self._syllable_counter.count_syllables(word)
            total_syllables += syllables

            if syllables > 2:
                polysyllable_count += 1

            if syllables > 0:
                histogram[syllables] = histogram.get(syllables, 0) + 1

        sentence_count_for_average = sentence_count if sentence_count > 0 else 1

        histogram = dict(sorted(histogram.items()))

        lix_config = self._language.get_formula_config("lix")
        long_word_threshold: int = 6
        if lix_config is not None and isinstance(lix_config, dict):
            threshold = lix_config.get("longWordThreshold")
            if isinstance(threshold, (int, float)):
                long_word_threshold = int(threshold)

        long_word_count = self._text_splitter.count_long_words(text, long_word_threshold)

        return TextStatistics(
            letter_count=letter_count,
            word_count=word_count,
            sentence_count=sentence_count,
            syllable_count=total_syllables,
            polysyllable_count=polysyllable_count,
            average_syllables_per_word=total_syllables / word_count,
            average_words_per_sentence=word_count / sentence_count_for_average,
            long_word_count=long_word_count,
            syllable_histogram=histogram,
        )

    def add_hyphenations(self, hyphenations: dict[str, str]) -> None:
        if isinstance(self._hyphenator, LiangHyphenator):
            self._hyphenator.add_hyphenations(hyphenations)
