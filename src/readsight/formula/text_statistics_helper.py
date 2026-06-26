from __future__ import annotations

from ..text.text_statistics import TextStatistics


class TextStatisticsHelper:
    @staticmethod
    def estimate_difficult_percentage(stats: TextStatistics) -> float:
        if stats.word_count == 0:
            return 0.0

        easy_word_count = stats.syllable_histogram.get(1, 0)
        difficult_count = stats.word_count - easy_word_count

        if difficult_count < 0:
            difficult_count = 0

        return (difficult_count / stats.word_count) * 100.0
