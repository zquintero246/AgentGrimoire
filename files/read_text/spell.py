"""read_text — read a local text file, bounded by a size cap.

Input : path (str), max_bytes (int, default 65536), encoding (str, "utf-8")
Output: dict {"text": str, "truncated": bool, "size_bytes": int}

Side effects: reads from the filesystem (never writes). Undecodable bytes
are replaced rather than raising. Missing paths raise FileNotFoundError
with the path in the message.

Safety: this tool reads whatever path it is given. When exposing it to an
agent, restrict or validate paths at the orchestration layer (e.g. a
middleware that rejects paths outside a working directory).

Example:
    >>> read_text("notes.txt")["text"][:12]
    'First line...'
"""

from pathlib import Path


def read_text(path: str, max_bytes: int = 65536, encoding: str = "utf-8") -> dict:
    """Read up to `max_bytes` of the file at `path`."""
    target = Path(path)
    if not target.is_file():
        raise FileNotFoundError(f"No file at {target} (cwd: {Path.cwd()})")
    if max_bytes < 1:
        raise ValueError(f"max_bytes must be >= 1, got {max_bytes}")
    size = target.stat().st_size
    with target.open("rb") as handle:
        raw = handle.read(max_bytes)
    return {
        "text": raw.decode(encoding, errors="replace"),
        "truncated": size > max_bytes,
        "size_bytes": size,
    }
