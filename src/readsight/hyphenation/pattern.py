from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pattern:
    chars: list[str]
    weights: list[int]
    length: int

    def __init__(self, chars: list[str], weights: list[int]) -> None:
        object.__setattr__(self, "chars", chars)
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "length", len(chars))
