"""list_directory — list the entries of a local directory.

Input : path (str, default "."), max_entries (int, default 100)
Output: list[dict] — one {"name", "type", "size_bytes"} per entry, sorted
        by name ("type" is "file" or "directory"; size is null for
        directories), capped at max_entries.

Side effects: reads the filesystem (never writes). Missing directories
raise ValueError with the path in the message.

Safety: same caveat as read_text — restrict paths at the orchestration
layer before exposing it to an agent.

Example:
    >>> list_directory(".")[0]
    {'name': 'README.md', 'type': 'file', 'size_bytes': 1024}
"""

from pathlib import Path


def list_directory(path: str = ".", max_entries: int = 100) -> list:
    """List up to `max_entries` entries of the directory at `path`."""
    target = Path(path)
    if not target.is_dir():
        raise ValueError(f"No directory at {target} (cwd: {Path.cwd()})")
    if max_entries < 1:
        raise ValueError(f"max_entries must be >= 1, got {max_entries}")
    entries = []
    for entry in sorted(target.iterdir(), key=lambda item: item.name.lower()):
        entries.append(
            {
                "name": entry.name,
                "type": "directory" if entry.is_dir() else "file",
                "size_bytes": entry.stat().st_size if entry.is_file() else None,
            }
        )
        if len(entries) >= max_entries:
            break
    return entries
