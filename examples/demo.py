"""
ReadSightPy - Interactive Demo
Usage: python demo.py [--compare] [--file=path] [--lang=code]
"""

from __future__ import annotations

import sys
from pathlib import Path

from readsight import ReadSight

_SAMPLE_TEXT = (
    "Reading is one of the most important skills a person can learn. "
    "Books open doors to new worlds and ideas. "
    "They allow us to travel through time and space without ever leaving our chair. "
    "A good book can change the way we think about life."
)

_SAMPLE_WORDS = [
    "banana", "character", "communication", "incredible",
    "information", "automatic", "extraordinary", "university", "readability",
]


def demo_english() -> None:
    rs = ReadSight("en-us")

    print("=" * 60)
    print("  ReadSightPy Demo - English (US)")
    print("=" * 60)

    print(f"\n  Source: built-in sample text")
    print(f'  Text:  "{_SAMPLE_TEXT[:80]}..."')
    print(f"\n  Language: {rs.language.name} ({rs.language.native_name})")
    print(f"  Script:   {rs.language.script.value}")
    print(f"  Formulas: {len(rs.get_supported_formulas())} available")

    print("\n" + "-" * 60)
    print("  Syllable Analysis")
    print("-" * 60)

    print(f"\n  {'Word':15s}  {'Syllables':9s}  Split")
    sep1 = "-" * 15
    sep2 = "-" * 9
    sep3 = "-" * 30
    print(f"  {sep1}  {sep2}  {sep3}")
    for word in _SAMPLE_WORDS:
        count = rs.syllable_count(word)
        parts = rs.split_syllables(word)
        parts_str = " - ".join(parts)
        print(f"  {word:15s}  {count:<9d}  {parts_str}")

    print("\n" + "-" * 60)
    print("  Text Statistics")
    print("-" * 60)

    text = _SAMPLE_TEXT
    stats = rs.analyze(text)

    lines = [
        ("Letters", str(stats.letter_count)),
        ("Words", str(stats.word_count)),
        ("Sentences", str(stats.sentence_count)),
        ("Syllables (total)", str(stats.syllable_count)),
        ("Avg syllables/word", f"{stats.average_syllables_per_word:.2f}"),
        ("Avg words/sentence", f"{stats.average_words_per_sentence:.2f}"),
        ("Polysyllables (>2)", str(stats.polysyllable_count)),
    ]
    for label, value in lines:
        print(f"  {label + ':':22s} {value}")

    if stats.syllable_histogram:
        print(f"\n  Syllable distribution:")
        max_count = max(stats.syllable_histogram.values())
        for n, count in sorted(stats.syllable_histogram.items()):
            bar_len = round(count / max_count * 20)
            bar = "#" * bar_len
            print(f"  {n}-syl: {bar} {count}")

    print("\n" + "-" * 60)
    print("  Readability Formulas")
    print("-" * 60)

    formula_display = [
        ("flesch_reading_ease", "Flesch Reading Ease"),
        ("flesch_kincaid_grade_level", "FK Grade Level"),
        ("gunning_fog", "Gunning Fog"),
        ("smog", "SMOG Index"),
        ("coleman_liau", "Coleman-Liau"),
        ("ari", "ARI"),
        ("lix", "LIX"),
        ("dale_chall", "Dale-Chall"),
        ("spache", "Spache"),
    ]
    for key, label in formula_display:
        try:
            result = rs.score(key, text)
            grade = f" (grade {result.grade_level})" if result.grade_level is not None else ""
            print(f"  {label:25s}  score={result.score:6.1f}{grade:18s}  {result.interpretation}")
        except Exception as e:
            print(f"  {label:25s}  ERROR: {e}")


def demo_multilingual() -> None:
    print("\n" + "=" * 60)
    print("  Multilingual Comparison")
    print("=" * 60)

    lang_configs = [
        ("en-us", "English (US)", "The quick brown fox jumps over the lazy dog."),
        ("de-1996", "German", "Der schnelle braune Fuchs springt \u00fcber den faulen Hund."),
        ("es", "Spanish", "El r\u00e1pido zorro marr\u00f3n salta sobre el perro perezoso."),
        ("fr", "French", "Le rapide renard brun saute par-dessus le chien paresseux."),
        ("it", "Italian", "La veloce volpe marrone salta sul cane pigro."),
        ("ru", "Russian", "\u0411\u044b\u0441\u0442\u0440\u0430\u044f \u043a\u043e\u0440\u0438\u0447\u043d\u0435\u0432\u0430\u044f \u043b\u0438\u0441\u0430 \u043f\u0440\u044b\u0433\u0430\u0435\u0442 \u0447\u0435\u0440\u0435\u0437 \u043b\u0435\u043d\u0438\u0432\u0443\u044e \u0441\u043e\u0431\u0430\u043a\u0443."),
    ]

    for code, name, text in lang_configs:
        try:
            rs = ReadSight(code)
            stats = rs.analyze(text)
            fre = rs.flesch_reading_ease(text)
            print(f"\n  {name} ({code})")
            print(f"    Words: {stats.word_count}, Sentences: {stats.sentence_count}")
            print(f"    FRE: {fre.score:.1f} - {fre.interpretation}")
        except Exception as e:
            print(f"  {name} ({code}): ERROR - {e}")


if __name__ == "__main__":
    demo_english()
    demo_multilingual()
