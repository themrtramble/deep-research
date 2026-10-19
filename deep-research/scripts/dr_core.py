"""dr_core.py — shared helpers for the Deep Research skill scripts.

Self-contained, stdlib-only. Provides: secret patterns, JSONL I/O, ID
generation, URL normalization, and title similarity.

Attribution: secret-pattern scanning is adapted from
B143KC47/deep-research-skill (MIT) and jojocorse2b/deep-research-skill
(MIT, (c) 2026 Lan Zheng). URL normalization is adapted from
doryashar/deep-research-skill (MIT, (c) 2026 dyashar).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# ---------------------------------------------------------------------------
# Vocabulary (controlled enums)
# ---------------------------------------------------------------------------

EFFORT_MODES = ("quick", "standard", "deep", "exhaustive")
SOURCE_TYPES = ("primary", "secondary", "tertiary", "aggregator", "social")
HOP_MODES = ("seed", "expand", "verify", "contradict", "synthesize", "checkpoint")
HOP_STATUSES = ("done", "dead_end", "needs_followup", "blocked")
STANCES = ("supports", "contradicts", "neutral")
FRESHNESS = ("current", "recent", "dated", "unknown")
INDEPENDENCE = ("independent", "correlated", "unknown")
UNCERTAINTY = ("established", "likely", "contested", "weak", "unknown")
QUALITY_SCALE = (1, 2, 3, 4, 5)
IMPORTANCE_SCALE = (1, 2, 3, 4, 5)

# Budget defaults per mode: (max_hops, min_sources, min_source_classes)
EFFORT_DEFAULTS = {
    "quick": (4, 2, 2),
    "standard": (10, 5, 3),
    "deep": (16, 10, 4),
    "exhaustive": (24, 15, 5),
}

# ---------------------------------------------------------------------------
# Secret patterns — fail-closed scanning of research artifacts.
# ---------------------------------------------------------------------------

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),            # OpenAI-style keys
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),              # GitHub PAT
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),      # GitHub fine-grained
    re.compile(r"AKIA[0-9A-Z]{16}"),                  # AWS access key id
    re.compile(r"ASIA[0-9A-Z]{16}"),                  # AWS temp access key id
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{20,}", re.I),
    re.compile(r"(?:api[_-]?key|password|passwd|secret|token)\s*[=:]\s*\S+", re.I),
]

REDACTED = "[REDACTED]"


def scan_secrets(text: str) -> list[str]:
    """Return human-readable descriptions of secret-pattern hits in *text*."""
    hits = []
    for pattern in SECRET_PATTERNS:
        m = pattern.search(text)
        if m:
            snippet = m.group(0)
            snippet = snippet if len(snippet) <= 24 else snippet[:24] + "..."
            hits.append(f"potential secret ({pattern.pattern[:32]}...): {snippet}")
    return hits


def redact_secrets(text: str) -> str:
    """Replace secret-pattern matches with a redaction marker."""
    out = text
    for pattern in SECRET_PATTERNS:
        out = pattern.sub(REDACTED, out)
    return out


# ---------------------------------------------------------------------------
# JSONL I/O with strict validation
# ---------------------------------------------------------------------------


class JsonlError(ValueError):
    """Raised when a JSONL file contains a malformed line."""


def read_jsonl(path: Path) -> list[dict]:
    records = []
    if not path.exists():
        return records
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                raise JsonlError(f"{path.name}:{lineno}: malformed JSON ({exc})") from exc
            if not isinstance(rec, dict):
                raise JsonlError(f"{path.name}:{lineno}: record is not a JSON object")
            records.append(rec)
    return records


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


# ---------------------------------------------------------------------------
# IDs
# ---------------------------------------------------------------------------


def next_id(records: list[dict], prefix: str, key: str | None = None) -> str:
    """Return the next zero-padded id like S0001 given existing records."""
    n = 0
    for rec in records:
        rid = str(rec.get(key or f"{prefix.lower()}_id", ""))
        digits = rid.replace(prefix, "")
        if digits.isdigit():
            n = max(n, int(digits))
    return f"{prefix}{n + 1:04d}"


def short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------------------
# URL normalization + dedup helpers
# ---------------------------------------------------------------------------

_TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "mc_cid", "mc_eid", "ref", "ref_src", "igshid",
    "si", "feature", "fbp", "cmpid", "share_id",
}


def normalize_url(url: str) -> str:
    """Canonicalize a URL for dedup: force https, strip tracking params,
    drop fragments, collapse trailing slash and www prefix."""
    url = (url or "").strip()
    if not url:
        return ""
    parts = urlsplit(url)
    scheme = "https" if parts.scheme in ("http", "https") else parts.scheme
    host = (parts.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=False)
             if k.lower() not in _TRACKING_PARAMS]
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((scheme, host, path, urlencode(query), ""))


def domain_of(url: str) -> str:
    return (urlsplit(url).netloc or "").lower().removeprefix("www.")


def _strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(c))


def title_similarity(a: str, b: str) -> float:
    """Similarity ratio of two titles after accent/case/punctuation fold."""
    def norm(t: str) -> str:
        t = _strip_accents((t or "").lower())
        t = re.sub(r"[^a-z0-9 ]+", " ", t)
        return re.sub(r"\s+", " ", t).strip()
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def dedup_sources(sources: list[dict], title_threshold: float = 0.85) -> tuple[list[dict], list[dict]]:
    """Merge duplicate sources. Returns (deduped, merge_log).

    Two sources are duplicates when normalized URLs match, or when titles
    are >= threshold similar AND share a domain. Merged records keep the
    first occurrence and union their aliases.
    """
    deduped: list[dict] = []
    merge_log: list[dict] = []
    seen_norm: dict[str, int] = {}

    for src in sources:
        url = src.get("url", "")
        norm = normalize_url(url)
        title = src.get("title", "")
        dom = domain_of(url)
        dup_idx = None
        reason = None

        if norm and norm in seen_norm:
            dup_idx, reason = seen_norm[norm], "same-normalized-url"
        else:
            for idx, kept in enumerate(deduped):
                if dom and domain_of(kept.get("url", "")) == dom:
                    if title_similarity(title, kept.get("title", "")) >= title_threshold:
                        dup_idx, reason = idx, "near-identical-title-same-domain"
                        break
        if dup_idx is not None:
            kept = deduped[dup_idx]
            kept.setdefault("aliases", [])
            if title and title not in kept["aliases"] and title != kept.get("title"):
                kept["aliases"].append(title)
            merge_log.append({
                "merged_url": url,
                "into_source_id": kept.get("source_id"),
                "reason": reason,
            })
            continue

        if norm:
            seen_norm[norm] = len(deduped)
        deduped.append(src)
    return deduped, merge_log


# ---------------------------------------------------------------------------
# CLI plumbing
# ---------------------------------------------------------------------------


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def ok(msg: str) -> None:
    print(msg)
