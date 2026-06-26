"""
ReadSightPy - Interactive Demo
Usage: python demo.py [--compare] [--file=path] [--lang=code]
"""

from __future__ import annotations

import sys
from pathlib import Path

from readsight import ReadSight

MOBY_DICK = (
    "Call me Ishmael. Some years ago--never mind how long precisely--"
    "having little or no money in my purse, and nothing particular to "
    "interest me on shore, I thought I would sail about a little and "
    "see the watery part of the world. It is a way I have of driving "
    "off the spleen and regulating the circulation."
)


def demo_english() -> None:
    rs = ReadSight("en-us")

    print("=" * 60)
    print("  ReadSightPy Demo - English (US)")
    print("=" * 60)

    print("\n--- Syllable Breakdown ---")
    for word in ["banana", "hyphenation", "hello", "beautiful", "extraordinary"]:
        count = rs.syllable_count(word)
        parts = rs.split_word(word)
        print(f"  {word:15s}  syllables={count}  parts={parts}")

    print("\n--- Text Statistics ---")
    text = MOBY_DICK
    stats = rs.analyze(text)
    print(f"  Letters:     {stats.letter_count}")
    print(f"  Words:       {stats.word_count}")
    print(f"  Sentences:   {stats.sentence_count}")
    print(f"  Syllables:   {stats.syllable_count}")
    print(f"  Avg syllables/word: {stats.average_syllables_per_word:.2f}")
    print(f"  Avg words/sentence: {stats.average_words_per_sentence:.2f}")
    print(f"  Polysyllables:      {stats.polysyllable_count}")

    print("\n--- Readability Scores ---")
    formulas: list[tuple[str, str]] = [
        ("Flesch Reading Ease", "flesch_reading_ease"),
        ("FK Grade Level", "flesch_kincaid_grade_level"),
        ("Gunning Fog", "gunning_fog"),
        ("SMOG Index", "smog"),
        ("Coleman-Liau", "coleman_liau"),
        ("ARI", "ari"),
        ("LIX", "lix"),
        ("Dale-Chall", "dale_chall"),
        ("Spache", "spache"),
    ]
    for label, key in formulas:
        try:
            result = rs.score(key, text)
            grade = f"  grade={result.grade_level}" if result.grade_level is not None else ""
            print(f"  {label:25s} score={result.score:6.1f}{grade:20s}  {result.interpretation}")
        except Exception as e:
            print(f"  {label:25s} ERROR: {e}")


def demo_multilingual() -> None:
    print("\n" + "=" * 60)
    print("  Multilingual Comparison")
    print("=" * 60)

    lang_configs = [
        ("en-us", "English (US)", "The quick brown fox jumps over the lazy dog."),
        ("de-1996", "German", "Der schnelle braune Fuchs springt über den faulen Hund."),
        ("es", "Spanish", "El rápido zorro marrón salta sobre el perro perezoso."),
        ("fr", "French", "Le rapide renard brun saute par-dessus le chien paresseux."),
        ("it", "Italian", "La veloce volpe marrone salta sul cane pigro."),
        ("ru", "Russian", "Быстрая коричневая лиса прыгает через ленивую собаку."),
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
