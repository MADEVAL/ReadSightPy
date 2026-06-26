from __future__ import annotations


class ReadabilityEngineException(RuntimeError):  # noqa: N818
    """Base exception for all readability engine errors."""


class EmptyTextException(ReadabilityEngineException):
    @classmethod
    def create(cls) -> EmptyTextException:
        return cls("Text must contain at least one letter.")


class PatternFileNotFoundException(ReadabilityEngineException):
    @classmethod
    def for_file(cls, file_path: str) -> PatternFileNotFoundException:
        return cls(f'Pattern file "{file_path}" not found.')


class PatternParseException(ReadabilityEngineException):
    @classmethod
    def with_line(cls, token: str, line_number: int, file_path: str) -> PatternParseException:
        return cls(f'Failed to parse pattern token "{token}" at line {line_number} in "{file_path}".')


class UnsupportedFormulaException(ReadabilityEngineException):
    @classmethod
    def for_language(cls, formula_name: str, language_code: str) -> UnsupportedFormulaException:
        return cls(f'Formula "{formula_name}" is not supported for language "{language_code}".')


class UnsupportedLanguageException(ReadabilityEngineException):
    @classmethod
    def with_code(cls, language_code: str) -> UnsupportedLanguageException:
        return cls(f'Language "{language_code}" is not supported.')
