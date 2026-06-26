from __future__ import annotations

from readsight.formula.grade_level_interpretation import GradeLevelInterpretation
from readsight.formula.text_statistics_helper import TextStatisticsHelper
from readsight.text.text_statistics import TextStatistics


class TestGradeLevelInterpretation:
    def test_kindergarten(self) -> None:
        assert GradeLevelInterpretation.for_score(0.5) == "Kindergarten"
        assert GradeLevelInterpretation.for_score(1.0) == "Kindergarten"

    def test_grades(self) -> None:
        assert GradeLevelInterpretation.for_score(3.5) == "3rd Grade"
        assert GradeLevelInterpretation.for_score(7.0) == "6th Grade"
        assert GradeLevelInterpretation.for_score(9.0) == "8th Grade"
        assert GradeLevelInterpretation.for_score(12.0) == "11th Grade"
        assert GradeLevelInterpretation.for_score(13.0) == "12th Grade"

    def test_college(self) -> None:
        assert GradeLevelInterpretation.for_score(16.0) == "College"

    def test_graduate(self) -> None:
        assert GradeLevelInterpretation.for_score(17.0) == "Graduate"


class TestTextStatisticsHelper:
    def test_estimate_difficult_percentage(self) -> None:
        stats = TextStatistics(
            letter_count=10,
            word_count=10,
            sentence_count=1,
            syllable_count=15,
            polysyllable_count=3,
            average_syllables_per_word=1.5,
            average_words_per_sentence=10.0,
            long_word_count=2,
            syllable_histogram={1: 5, 2: 3, 3: 2},
        )
        pct = TextStatisticsHelper.estimate_difficult_percentage(stats)
        assert pct == 50.0  # 5 easy out of 10 = 50% difficult

    def test_estimate_difficult_all_easy(self) -> None:
        stats = TextStatistics(
            letter_count=5, word_count=5, sentence_count=1,
            syllable_count=5, polysyllable_count=0,
            average_syllables_per_word=1.0, average_words_per_sentence=5.0,
            long_word_count=0,
            syllable_histogram={1: 5},
        )
        pct = TextStatisticsHelper.estimate_difficult_percentage(stats)
        assert pct == 0.0

    def test_estimate_difficult_zero_words(self) -> None:
        stats = TextStatistics(
            letter_count=0, word_count=0, sentence_count=0,
            syllable_count=0, polysyllable_count=0,
            average_syllables_per_word=0.0, average_words_per_sentence=0.0,
            long_word_count=0,
            syllable_histogram={},
        )
        pct = TextStatisticsHelper.estimate_difficult_percentage(stats)
        assert pct == 0.0
