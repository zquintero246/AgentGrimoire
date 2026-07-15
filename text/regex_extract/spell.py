"""regex_extract — extract every match of a regular expression from a text.

Input : pattern (str, Python regex), text (str), max_matches (int, default 20)
Output: list[str] — the full match (group 0) of each occurrence, in order,
        capped at max_matches.

Deterministic, no side effects, stdlib only. An invalid pattern raises
ValueError with the regex error message, so an agent can correct itself.

Example:
    >>> regex_extract(r"\\d+", "born 1877, died 1907")
    ['1877', '1907']
"""

import re


def regex_extract(pattern: str, text: str, max_matches: int = 20) -> list:
    """Return up to `max_matches` occurrences of `pattern` in `text`."""
    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        raise ValueError(f"Invalid regular expression {pattern!r}: {exc}") from None
    if max_matches < 1:
        raise ValueError(f"max_matches must be >= 1, got {max_matches}")
    matches = []
    for found in compiled.finditer(text):
        matches.append(found.group(0))
        if len(matches) >= max_matches:
            break
    return matches
