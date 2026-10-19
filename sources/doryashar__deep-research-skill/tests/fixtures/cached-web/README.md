# Cached web fixtures

Frozen `WebFetch` / `WebSearch` responses used by smoke tests to keep CI
deterministic. Layout:

```
cached-web/
├── search/
│   └── <sha256-of-query>.json      # WebSearch response
└── fetch/
    └── <sha256-of-url>.json        # WebFetch response (body, content-type, status)
```

Populated by `scripts/freeze_fixture.sh "<query>"` (not yet shipped; planned
for Phase 2). Until then the smoke runner falls back to live network with
`ALLOW_LIVE_NETWORK=1`.
