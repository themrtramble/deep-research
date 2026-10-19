# State Management Schemas

리서치 세션의 상태 추적과 소스 기록에 사용되는 JSON 스키마입니다.

---

## state.json Schema

```json
{
  "session_id": "Topic_Name_20260129_143000",
  "topic": "Research Topic",
  "created_at": "2026-01-29T14:30:00Z",
  "updated_at": "2026-01-29T15:45:00Z",
  "status": "PHASE_3_QUERYING",
  "current_phase": 3,
  "tier": "Express | Standard | Full",
  "agent_allocation": "A, B | A*2, B, C | A, B, C, D",
  "depth_profile": "Deep-Narrow | Broad-Survey | Balanced",
  "freshness_priority": "High-Recency | High-Reliability | Balanced",
  "audience": "Expert | General | Decision-maker",
  "requirements": {
    "focus": ["aspect1", "aspect2"],
    "output_format": "comprehensive_report",
    "scope": {"timeframe": {}, "geography": {}},
    "sources": {"required_types": [], "min_quality": "B"},
    "special_requirements": []
  },
  "plan": {
    "subtopics": [],
    "search_queries": {},
    "agent_assignments": []
  },
  "progress": {
    "phase_1": "completed",
    "phase_2": "completed",
    "phase_3": "in_progress",
    "phase_4": "pending",
    "phase_5": "pending",
    "phase_6": "pending",
    "phase_7": "pending"
  },
  "sources_count": 0,
  "artifacts": {},
  "errors": []
}
```

---

## sources.jsonl Schema (one JSON per line)

```json
{"id": "src_001", "url": "https://...", "title": "Article Title", "author": "Author", "date": "2024-06-15", "domain": "nature.com", "type": "academic", "quality_rating": "A", "snippet": "relevant excerpt...", "claims": ["claim1"], "verified": true}
```
