"""http_fetch — fetch a public HTTP(S) URL with GET, bounded by size and time.

Input : url (str), max_bytes (int, default 250000), timeout (float, 10s),
        allow_private (bool, default False — not exposed in the manifest)
Output: dict {"status": int, "content_type": str, "truncated": bool,
              "text": str}

Side effects: one outbound GET request. Local-safe by design:

- only http:// and https:// schemes are accepted;
- hosts resolving to private, loopback, link-local, or reserved addresses
  are REJECTED unless allow_private=True is passed explicitly in code —
  an agent-controlled URL must not be able to probe your internal network
  (SSRF). Note: the check runs before the request; a hostile DNS server
  could still change answers between check and request (classic TOCTOU) —
  for hard guarantees, isolate at the network layer;
- the body read is capped at max_bytes; undecodable bytes are replaced.

Nondeterministic by nature (remote content changes). Stdlib only.

Example:
    >>> http_fetch("https://example.com")["status"]
    200
"""

import ipaddress
import socket
import urllib.error
import urllib.request
from urllib.parse import urlparse

_USER_AGENT = "AgentGrimoire-http-fetch/1.0"


def http_fetch(
    url: str,
    max_bytes: int = 250_000,
    timeout: float = 10.0,
    allow_private: bool = False,
) -> dict:
    """GET `url` and return status, content type, and (capped) body text."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Only http:// and https:// URLs are allowed, got {url!r}"
        )
    if not parsed.hostname:
        raise ValueError(f"URL has no host: {url!r}")
    if max_bytes < 1:
        raise ValueError(f"max_bytes must be >= 1, got {max_bytes}")
    if not allow_private and _resolves_to_private(parsed.hostname):
        raise ValueError(
            f"Host {parsed.hostname!r} resolves to a private/loopback "
            "address; refusing to fetch it (pass allow_private=True in "
            "code if this is intentional)."
        )

    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(max_bytes + 1)
            return {
                "status": response.status,
                "content_type": response.headers.get("Content-Type", ""),
                "truncated": len(body) > max_bytes,
                "text": body[:max_bytes].decode("utf-8", errors="replace"),
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(max_bytes) if exc.fp else b""
        return {
            "status": exc.code,
            "content_type": exc.headers.get("Content-Type", "") if exc.headers else "",
            "truncated": False,
            "text": body.decode("utf-8", errors="replace"),
        }
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ValueError(f"Could not fetch {url!r}: {exc}") from None


def _resolves_to_private(host: str) -> bool:
    """True when any resolved address of `host` is non-public."""
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Cannot resolve host {host!r}: {exc}") from None
    for info in infos:
        address = ipaddress.ip_address(info[4][0])
        if (
            address.is_private
            or address.is_loopback
            or address.is_link_local
            or address.is_reserved
            or address.is_multicast
        ):
            return True
    return False
