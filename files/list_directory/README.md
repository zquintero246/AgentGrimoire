# list_directory

List the entries of a local directory with type and size.

- **Input**: `path` (string, default `.`), `max_entries` (int, default 100)
- **Output**: `list[{"name", "type", "size_bytes"}]`, sorted by name;
  `size_bytes` is `null` for directories
- **Side effects**: reads the filesystem; never writes.
- **Safety**: restrict paths at the orchestration layer before exposing
  it to an agent.

## Example

```python
from spell import list_directory

list_directory(".", max_entries=5)
```
