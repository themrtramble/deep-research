# Phase Contracts

이 문서는 각 Phase의 입출력 JSON 스키마와 성공 기준을 정의합니다.
Phase의 목적과 프로세스는 SKILL.md를 참조하세요. 여기서는 "무엇을 넘겨받고, 무엇을 산출하고, 어떤 조건을 충족해야 다음 Phase로 넘어갈 수 있는가"만 다룹니다.

---

## Phase 1 → 2 넘김: 요구사항 정의

Phase 1이 끝나면 아래 구조의 요구사항을 Phase 2에 넘깁니다.
사용자가 AskUserQuestion으로 선택한 내용이 여기에 채워집니다.

```json
{
  "topic": "정제된 리서치 주제",
  "focus_areas": ["현재 상태와 트렌드", "기술 심층 분석"],
  "output_format": "comprehensive_report | modular",
  "scope": {
    "geographic": "Global",
    "temporal": "2024-현재",
    "exclusions": ["제외할 범위"]
  },
  "sources": {
    "preferred": ["academic", "official", "industry"],
    "min_quality": "B"
  },
  "special_requirements": []
}
```

**성공 기준**: 사용자가 범위를 확인했고, 모호한 부분이 없어야 합니다.

---

## Phase 2 → 3 넘김: 리서치 계획

Phase 2는 주제를 3-5개 서브토픽으로 분해하고, 각 서브토픽별 검색 전략을 세웁니다.

```json
{
  "subtopics": [
    {
      "name": "서브토픽 이름",
      "questions": ["이 서브토픽에서 답해야 할 질문들"],
      "search_queries": ["실제 WebSearch에 넣을 쿼리들 (연도 포함)"],
      "source_types": ["academic", "news", "official"],
      "analysis_framework": "comparison_matrix | trend_analysis | causal_chain",
      "priority": 1
    }
  ],
  "agent_assignments": [
    {
      "agent_type": "general-purpose",
      "subtopic": "서브토픽 이름",
      "focus": "current_state | challenges | comparative"
    }
  ]
}
```

**성공 기준**: 서브토픽 간 중복이 없고, 검색 쿼리가 구체적이며 현재 연도를 포함하고, 사용자가 계획을 승인해야 합니다.

---

## Phase 3 → 4 넘김: 수집된 소스

Phase 3에서 에이전트들이 수집한 소스는 sources.jsonl에 한 줄씩 저장됩니다.

```json
{
  "id": "src_001",
  "url": "https://...",
  "title": "출처 제목",
  "author": "저자/기관",
  "date": "2024-01-15",
  "domain": "example.com",
  "type": "academic | news | official | blog",
  "quality_rating": "A",
  "snippet": "관련 발췌문...",
  "subtopic": "해당 서브토픽",
  "claims": ["이 출처가 주장하는 내용들"]
}
```

**성공 기준**: 서브토픽당 최소 3개 이상의 소스가 있고, 소스 도메인이 다양해야 합니다.

---

## Phase 4 → 5 넘김: 검증된 주장

Phase 4는 소스들을 교차 검증하여 주장의 신뢰도를 평가합니다.

```json
{
  "verified_claims": [
    {
      "claim": "주장 내용",
      "sources": ["src_001", "src_003"],
      "confidence": "high | medium | low",
      "contradictions": []
    }
  ],
  "contradictions": [
    {
      "claim_a": "A 버전의 주장",
      "source_a": "src_002",
      "claim_b": "B 버전의 주장",
      "source_b": "src_005",
      "resolution": "해결 설명 또는 'unresolved'"
    }
  ]
}
```

**성공 기준**: 핵심 주장이 2개 이상의 독립 소스로 확인되었고, 모순이 문서화되었으며, E등급 소스가 최종 산출물에 포함되지 않아야 합니다.

---

## Phase 5 산출물: 보고서 초안

Phase 5는 리서치의 품질을 결정하는 핵심 단계입니다. 단순 요약이 아니라 분석적 글쓰기를 해야 합니다.

산출물 구조:
```
artifacts/drafts/
├── draft_subtopic_1.md
├── draft_subtopic_2.md
├── draft_subtopic_3.md
├── draft_cross_cutting_insights.md   ← 서브토픽을 가로지르는 통합 분석
└── draft_conclusion.md               ← 결론 + 권고사항 + 미해결 질문
```

**각 초안의 필수 요소**:
- 테마 기반 구성 (출처별 나열이 아닌 주제별 분석)
- 모든 주장에 인라인 인용
- 3개 이상 비교 시 비교표 활용
- 각 주요 섹션 말미에 "왜 이것이 중요한가" 설명
- 결론의 신뢰도 표기

**Insight Quality Levels** (SKILL.md 참조):
- L1 서술적: 사실 나열 → 최소 기준 미달
- L2 비교적: 구조화된 비교 → 최소 기준
- L3 분석적: 패턴 + 인과관계 → 목표 수준
- L4 전략적: 종합 + 권고 → 결론/권고 섹션

**성공 기준**:
- 모든 서브토픽이 테마 기반으로 구성되었는가
- 모든 주장에 인용이 있는가
- 모든 섹션이 "So What?" 테스트를 통과하는가
- Cross-cutting insights가 식별되었는가 (서브토픽별 요약이 아닌)
- 비교 프레임워크가 적절히 사용되었는가
- 인과 추론이 명시적인가 (상관관계와 혼동하지 않는가)
- 권고가 구체적이고 근거에 기반하는가

---

## Phase 6 산출물: QA 결과

Phase 6은 소스 품질, 분석 품질, 보고서 품질을 모두 검증합니다.
QA 체크리스트는 pipelines.py의 `QA_CHECKLIST`와 SKILL.md의 Quality Checklist를 참조합니다.

실패 시 Phase 5로 돌아가 해당 부분을 수정합니다.

---

## Phase 7 산출물: 최종 패키지

템플릿 참조: `assets/templates/executive_summary.md`, `assets/templates/full_report_section.md`

```
outputs/
├── full_report/
│   ├── 01_introduction.md
│   ├── 02_{subtopic_1}.md
│   ├── ...
│   ├── {N}_cross_cutting_insights.md
│   └── {N+1}_conclusions_and_recommendations.md
├── summary_context.md    ← 향후 요약 생성용 맥락 파일
├── appendices/
│   ├── bibliography.md
│   └── methodology.md
└── comparison_data.json  ← 시각화용 데이터

sources/
└── bibliography.md
```

**성공 기준**: 보고서가 필요한 모든 맥락을 빠짐없이 담고 있으며, summary_context.md가 핵심 발견과 뉘앙스를 보존하고 있어야 합니다.

---

## Phase 6 산출물: Claim DB (YAML)

리포트와 별도로 수집된 모든 Claim을 구조화된 YAML로 저장한다. 후속 리서치에서 재활용.

```yaml
meta:
  topic: "[주제]"
  date: "YYYY-MM-DD"
  tier: "[Express/Standard/Full]"
  total_claims: N
  total_sources: N

claims:
  - id: "C001"
    claim: "[주장 내용]"
    domain: "[health/tech/policy/market]"
    sources:
      - author: "[저자/기관]"
        title: "[제목]"
        url: "[URL]"
        reliability: "A"
        year: YYYY
        accessible: true
    counter_claims: ["C012"]
    confidence: "high"
    tags: ["keyword1"]
```

---

## 상태 전이

```
INIT -> Phase 0 -> Phase 1 -> Phase 2 -> Phase 3 (URL검증 필수) -> Phase 3.5 -> Phase 4 -> Phase 5 (스코어링) -> Phase 6 -> COMPLETED
                                                  (Express skip)                    |              |
                                                                                    +<-------------+ (스코어 미달, 최대 2회)
```

- Phase 3: URL 검증은 생략 불가. 핵심 URL 10-20개에 WebFetch 접근 확인 필수
- Phase 3.5: Express 티어에서는 생략, Standard/Full에서만 Gap 기반 자동 실행 (최대 1회)
- Phase 5: 5차원 스코어링(상세성/가독성/분석수준/출처품질/실행가능성). 티어별 합격 기준 미달 시 Phase 4로 회귀 (최대 2회 루프)
- 세션은 어느 Phase에서든 중단 후 재개 가능 (state.json)
