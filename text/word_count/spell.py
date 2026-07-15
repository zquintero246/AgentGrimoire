"""word_count — count the words, characters, and lines in a text.

Input : text (str)
Output: dict {"words": int, "characters": int, "lines": int}

Deterministic, no side effects, stdlib only. Words are whitespace-separated
tokens; characters include whitespace; lines are newline-separated (a
trailing newline does not add an empty line).

Example:
    >>> word_count("lux aeterna")
    {'words': 2, 'characters': 11, 'lines': 1}
"""


def word_count(text: str) -> dict:
    """Count words, characters, and lines in `text`."""
    return {
        "words": len(text.split()),
        "characters": len(text),
        "lines": len(text.splitlines()) if text else 0,
    }
