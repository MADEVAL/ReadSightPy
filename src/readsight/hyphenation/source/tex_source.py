from __future__ import annotations

from pathlib import Path
from typing import Any

import regex  # type: ignore[import-untyped]

from ...exceptions import PatternFileNotFoundException, PatternParseException
from ..hyphenation_exceptions_collection import HyphenationExceptionsCollection
from ..hyphenation_override import HyphenationOverride
from ..pattern import Pattern
from ..patterns_collection import PatternsCollection
from .pattern_source import PatternSource


class TexSource(PatternSource):
    def __init__(self, tex_file_path: str) -> None:
        self._tex_file_path = tex_file_path

    def load(self) -> dict[str, Any]:
        path = Path(self._tex_file_path)
        if not path.is_file():
            raise PatternFileNotFoundException.for_file(self._tex_file_path)

        lines = path.read_text(encoding="utf-8").splitlines()
        patterns = PatternsCollection()
        exceptions = HyphenationExceptionsCollection()
        line_number = 0

        command: str | None = None
        in_braces = False

        for line in lines:
            line_number += 1
            offset = 0
            strlen = len(line)

            while offset < strlen:
                char = line[offset]

                if char == "%" and not in_braces:
                    break

                if char == "\\" and not in_braces:
                    m = regex.match(r"\\([a-zA-Z]+)", line[offset:])
                    if m:
                        command = m.group(1)
                        offset += len(m.group(0))
                        continue
                    offset += 1
                    continue

                if char == "{":
                    if command is not None:
                        in_braces = True
                    offset += 1
                    continue

                if char == "}" and in_braces:
                    in_braces = False
                    command = None
                    offset += 1
                    continue

                if in_braces:
                    if command == "patterns":
                        m = regex.match(r"(\S+)", line[offset:])
                        if m:
                            token = m.group(0)
                            pattern = self._parse_pattern_token(token, line_number)
                            if pattern is not None:
                                patterns.add(pattern)
                            offset += len(m.group(0))
                            continue
                    elif command == "hyphenation":
                        m = regex.match(r"(\S+)", line[offset:])
                        if m:
                            token = m.group(0)
                            word = token.replace("-", "").lower()
                            hyphenated = token.lower()
                            exceptions.add(HyphenationOverride(word, hyphenated))
                            offset += len(m.group(0))
                            continue

                offset += 1

        return {
            "patterns": patterns,
            "exceptions": exceptions,
            "maxPatternLength": patterns.max_length(),
        }

    def _parse_pattern_token(self, token: str, line_number: int) -> Pattern | None:
        chars: list[str] = []
        numbers_parts: list[str] = []
        expect_number = True
        has_digit = False

        segments = regex.findall(r"\d+|\D", token)
        if not segments:
            raise PatternParseException.with_line(token, line_number, self._tex_file_path)

        for char in segments:
            if char.isdigit():
                numbers_parts.append(char)
                has_digit = True
                expect_number = False
            else:
                if expect_number:
                    numbers_parts.append("0")
                chars.append(char)
                expect_number = True

        if expect_number:
            numbers_parts.append("0")

        if not chars or not has_digit:
            return None

        numbers_str = "".join(numbers_parts)
        weights = [int(d) for d in numbers_str]

        return Pattern(chars, weights)
