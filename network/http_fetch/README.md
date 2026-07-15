# http_fetch

Fetch a public HTTP(S) URL with GET, bounded by size and time.

- **Input**: `url` (string), `max_bytes` (int, default 250000),
  `timeout` (seconds, default 10)
- **Output**: `{"status": int, "content_type": str, "truncated": bool,
  "text": str}`; HTTP error statuses are returned, not raised
- **Side effects**: one outbound GET request. Nondeterministic by nature
  (remote content changes).
- **Safety**: only `http/https`; hosts resolving to private, loopback,
  link-local, or reserved addresses are **rejected** so an
  agent-controlled URL can't probe your internal network (SSRF). The
  check is best-effort (DNS TOCTOU applies) — isolate at the network
  layer for hard guarantees. `allow_private=True` exists in code only,
  deliberately not in the manifest.

## Example

```python
from spell import http_fetch

page = http_fetch("https://example.com", max_bytes=4096)
page["status"], page["truncated"]
```
