# Question Scoping — AskUserQuestion Templates

Phase 0에서 사용자에게 리서치 범위를 확인할 때 사용하는 AskUserQuestion 템플릿입니다.

---

## 핵심 규칙

- **AskUserQuestion 도구를 즉시 호출**할 것. 텍스트 기반 번호 질문 출력 금지.
- 사용자 입력 언어를 감지하여, 모든 label/description을 **동일 언어**로 생성할 것.
- 1-4개 질문 그룹으로 조합하여 한 번에 호출.

---

## Korean Example (한국어 입력 시)

```json
{
  "questions": [
    {
      "question": "이 리서치로 궁극적으로 답하고 싶은 질문은 무엇인가요?",
      "header": "핵심 질문",
      "options": [
        {"label": "현재 상태와 트렌드", "description": "최신 동향, 시장 현황, 주요 플레이어"},
        {"label": "기술 심층 분석", "description": "아키텍처, 구현 방법, 기술 스택"},
        {"label": "시장 분석", "description": "시장 규모, 성장률, 경쟁 구도"},
        {"label": "모두 포함 (Recommended)", "description": "종합 리서치 - 모든 측면 분석"}
      ],
      "multiSelect": false
    },
    {
      "question": "리서치 규모를 선택해주세요.",
      "header": "티어",
      "options": [
        {"label": "Express (~10,000자)", "description": "에이전트 2개, 소스 10개+. 빠른 의사결정이 필요할 때"},
        {"label": "Standard (~25,000자) (Recommended)", "description": "에이전트 3개, 소스 20개+. 일반적인 리서치"},
        {"label": "Full (50,000자+)", "description": "에이전트 4개+, 소스 30개+. 심층 분석이 필요할 때"}
      ],
      "multiSelect": false
    },
    {
      "question": "어떤 소스를 우선시할까요?",
      "header": "소스 우선순위",
      "options": [
        {"label": "최신성 우선", "description": "최근 데이터가 중요 (시장 동향, 기술 트렌드)"},
        {"label": "신뢰도 우선", "description": "검증된 근거가 중요 (건강, 과학, 정책)"},
        {"label": "균형 (Recommended)", "description": "최신성과 신뢰도 균형"}
      ],
      "multiSelect": false
    }
  ]
}
```

## English Example

```json
{
  "questions": [
    {
      "question": "What aspects interest you most?",
      "header": "Focus",
      "options": [
        {"label": "Current state & trends", "description": "Latest developments, market status, key players"},
        {"label": "Technical deep-dive", "description": "Architecture, implementation, tech stack"},
        {"label": "Market analysis", "description": "Market size, growth rate, competition"},
        {"label": "All of the above (Recommended)", "description": "Comprehensive research - all aspects"}
      ],
      "multiSelect": false
    },
    {
      "question": "What research scale do you need?",
      "header": "Tier",
      "options": [
        {"label": "Express (~10K chars)", "description": "2 agents, 10+ sources. Quick decision-making"},
        {"label": "Standard (~25K chars) (Recommended)", "description": "3 agents, 20+ sources. General research"},
        {"label": "Full (50K+ chars)", "description": "4+ agents, 30+ sources. Deep analysis"}
      ],
      "multiSelect": false
    },
    {
      "question": "Any source preferences?",
      "header": "Sources",
      "options": [
        {"label": "Recency first", "description": "Latest data matters (market trends, tech)"},
        {"label": "Reliability first", "description": "Verified evidence matters (health, science, policy)"},
        {"label": "Balanced (Recommended)", "description": "Balance recency and reliability"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## After User Responds

1. Compose **Research Brief** (see SKILL.md Phase 0)
2. Determine **Agent Allocation** based on topic + tier
3. Create session folder: `RESEARCH/{topic}_{timestamp}/`
4. Initialize `state.json` with tier, allocation, requirements
5. Show Research Brief to user for final confirmation
6. Execute Phase 1-6 sequentially
