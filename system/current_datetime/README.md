# current_datetime

Return the current date and time as an ISO 8601 string. Models don't know
today's date — give them this instead of letting them guess.

- **Input**: `timezone` (`"utc"` or `"local"`, default `"utc"`)
- **Output**: string, e.g. `"2026-07-14T21:03:07+00:00"`
- **Side effects**: none. **Nondeterministic by purpose** (reads the
  clock), per the repository's determinism guideline.

## Example

```python
from spell import current_datetime

current_datetime("local")
```
