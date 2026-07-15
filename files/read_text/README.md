# read_text

Read a local text file, bounded by a size cap.

- **Input**: `path` (string), `max_bytes` (int, default 65536),
  `encoding` (string, default `utf-8`)
- **Output**: `{"text": str, "truncated": bool, "size_bytes": int}`
- **Side effects**: reads the filesystem; never writes.
- **Safety**: reads whatever path it is given — restrict or validate
  paths at the orchestration layer before exposing it to an agent (e.g.
  reject paths outside a working directory).

## Example

```python
from spell import read_text

result = read_text("notes.txt", max_bytes=4096)
result["truncated"]   # True if the file was larger than the cap
```
