"""current_datetime — the current date and time as an ISO 8601 string.

Input : timezone (str, "utc" or "local"; default "utc")
Output: str — e.g. "2026-07-14T21:03:07+00:00"

Nondeterministic BY PURPOSE (it reads the clock); documented per the
repository's determinism guideline. No other side effects, stdlib only.
Models don't know today's date — give them this instead of letting them
guess.

Example:
    >>> current_datetime("utc")
    '2026-07-14T21:03:07+00:00'
"""

from datetime import datetime, timezone as _timezone


def current_datetime(timezone: str = "utc") -> str:
    """Return the current moment in the requested timezone."""
    if timezone == "utc":
        return datetime.now(_timezone.utc).isoformat(timespec="seconds")
    if timezone == "local":
        return datetime.now().astimezone().isoformat(timespec="seconds")
    raise ValueError(f"timezone must be 'utc' or 'local', got {timezone!r}")
