# regex_extract

Extract every match of a regular expression from a text.

- **Input**: `pattern` (Python regex), `text` (string), `max_matches`
  (int, default 20)
- **Output**: `list[str]` — full match of each occurrence, in order,
  capped at `max_matches`
- **Side effects**: none. Deterministic. Stdlib only.
- **Errors**: invalid patterns raise `ValueError` carrying the regex
  error, so agents can self-correct.

## Example

```python
from spell import regex_extract

regex_extract(r"\d+", "born 1877, died 1907")
# ['1877', '1907']
```
