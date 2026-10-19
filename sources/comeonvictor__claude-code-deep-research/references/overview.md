# Deep Research Skill 개요

이 문서는 deep-research 스킬의 전체 구조와 각 파일의 역할을 설명합니다. 스킬을 처음 접하거나 수정할 때 참고하세요. 실제 실행 로직은 SKILL.md에, 각 Phase의 입출력 계약은 phase_contracts.md에 정의되어 있습니다.

---

## 스킬의 목적

deep-research는 주제를 입력받으면 웹 검색, 소스 검증, 교차 확인을 거쳐 인용이 달린 종합 리서치 보고서를 자동으로 생성하는 스킬입니다.

단순한 정보 수집이 아니라, 수집한 정보에서 패턴을 식별하고 인과관계를 분석하며 실행 가능한 권고를 도출하는 것이 핵심입니다. 보고서의 분량에 제한을 두지 않으며, 리서치 주제가 요구하는 만큼 충분한 맥락과 깊이를 제공합니다.

"조사해줘", "찾아봐"와 같은 가벼운 리서치 요청은 research-workflow 스킬이 처리합니다. deep-research는 "심층 리서치", "딥리서치", "/deep-research"처럼 명시적으로 깊은 분석을 요청할 때만 트리거됩니다.

---

## 파일 구조

```
.claude/skills/deep-research/
├── SKILL.md                          # 스킬 정의 본체 (Phase 0~7)
└── references/
    ├── overview.md                   # 이 파일 (전체 구조 설명)
    ├── agent-prompts.md              # A/B/C/D 에이전트별 프롬프트
    ├── report-template.md            # 티어별 리포트 + Claim DB 템플릿
    ├── source-evaluation.md          # A-E 5등급 소스 평가 + URL 검증
    ├── question_scoping.md           # AskUserQuestion 템플릿 (티어 포함)
    ├── phase_contracts.md            # Phase 간 입출력 계약
    ├── quality_rubric.md             # 소스 품질 A~E 등급 기준
    ├── citation_rules.md             # 인용 형식 가이드라인
    └── state_schema.md               # state.json/sources.jsonl 스키마
```

이 구조는 Claude의 Progressive Disclosure 원칙을 따릅니다. SKILL.md의 YAML frontmatter가 항상 로드되어 스킬 선택 판단에 사용되고, 스킬이 트리거되면 SKILL.md 본문이 로드됩니다. references/ 파일들은 해당 Phase를 실행할 때 필요한 시점에 온디맨드로 참조합니다.

---

## 각 파일의 역할

### SKILL.md

스킬의 핵심 파일입니다. 트리거 조건, 8 Phase 프로세스 정의, 멀티 에이전트 전략, 인용 규칙, 날짜 인식 검색 규칙, 상태 관리, 환각 방지 전략, 인사이트 기반 분석 프레임워크가 모두 여기에 있습니다. Claude가 스킬을 실행할 때 가장 먼저 읽는 파일이며, 대부분의 경우 이 파일만으로도 리서치 전체를 수행할 수 있습니다.

### references/phase_contracts.md

각 Phase가 무엇을 입력받고, 무엇을 산출하며, 어떤 조건을 충족해야 다음 Phase로 넘어갈 수 있는지를 JSON 스키마와 성공 기준으로 정의합니다. Phase의 목적이나 프로세스 설명은 SKILL.md에 있으므로, 이 문서는 순수하게 "계약(contract)" 역할만 합니다.

특히 Phase 5(지식 종합)의 계약이 중요합니다. 단순한 소스 요약이 아니라 테마 기반 구성, 인라인 인용, "So What?" 테스트, Cross-cutting Insights 식별 등 분석적 글쓰기의 기준을 정의하고 있습니다.

### references/quality_rubric.md

소스의 신뢰도를 A~E 등급으로 평가하는 상세 기준입니다. 등급별 판단 기준, 도메인별 조정 규칙(기술/의료/비즈니스/법률 분야마다 기준이 다름), 자동 등급 하락 조건(저자 없음, 날짜 없음, 철회된 논문 등)을 포함합니다. Phase 4(교차 검증) 시점에 참조합니다.

### references/citation_rules.md

인라인 인용 형식, 참고문헌 형식, 직접 인용과 간접 인용의 구분, 특수 케이스 처리(저자 없음/날짜 없음/복수 저자), 섹션별 인용 밀도 가이드라인을 정의합니다. Phase 5(보고서 작성)와 Phase 6(QA) 시점에 참조합니다.

### scripts/pipelines.py

에이전트 프롬프트 템플릿 라이브러리입니다. 서브토픽 분해 프롬프트, 6종의 에이전트 프롬프트 (현재 상태/과제/미래/비교/학술/검증), 지식 종합(Synthesis) 프롬프트, Cross-cutting Insights 프롬프트, Summary Context 생성 프롬프트, QA 체크리스트를 포함합니다.

모든 프롬프트는 `{current_date}`, `{current_year}` 변수를 사용하여 하드코딩된 연도 없이 동작합니다. 각 에이전트 프롬프트는 단순 수집이 아니라 패턴 분석, 합의/논쟁 구분, 정보 공백 식별을 요구하도록 설계되어 있습니다.

### assets/templates/summary_context.md

Phase 7에서 자동 생성되는 요약 맥락 파일의 템플릿입니다. 전체 보고서를 다시 읽지 않고도 핵심 맥락을 보존한 요약을 만들 수 있도록, 핵심 발견(중요도순), 요약 시 잃으면 안 되는 뉘앙스, Cross-cutting Insights, 핵심 데이터 포인트, 한계와 미해결 질문을 구조화합니다.

보고서 완성 후 사용자가 요약을 요청하면(Phase 8), 이 파일과 본 보고서를 함께 참조하여 깊이 있는 요약을 생성합니다.

### assets/templates/bibliography.md

참고문헌 목록의 포맷 템플릿입니다. 학술/업계/공식/뉴스/온라인 카테고리별 분류, 소스 품질 분포 시각화, 방법론 노트 구조를 정의합니다.

### assets/templates/readme_research.md

리서치 결과 폴더(`RESEARCH/{주제}_{timestamp}/`)에 생성되는 README의 템플릿입니다. 네비게이션 가이드, 핵심 발견 요약, 폴더 구조 설명, Phase별 진행 상태를 포함합니다.

### assets/templates/website_template.html

리서치 결과를 시각적으로 표현하는 웹페이지 템플릿입니다. 탭 UI, Chart.js 기반 차트, 소스 품질 테이블, 반응형 디자인을 포함합니다. 선택적으로 생성됩니다.

---

## 리서치 프로세스 요약

스킬은 8단계로 동작합니다. Phase 1~7은 순차적으로 실행되며, Phase 8은 보고서 완성 후 사용자가 요약을 요청할 때만 실행됩니다.

Phase 1에서 사용자와 리서치 범위를 확정한 뒤, Phase 2에서 주제를 3~5개 서브토픽으로 분해하고 검색 전략을 세웁니다. Phase 3에서 병렬 에이전트가 WebSearch와 WebFetch를 사용해 정보를 수집하고, Phase 4에서 수집된 소스를 교차 검증하여 신뢰도를 평가합니다.

Phase 5가 보고서 품질을 결정하는 핵심 단계입니다. 단순히 소스를 나열하는 것이 아니라, 패턴을 식별하고 인과관계를 분석하며 서브토픽을 관통하는 통합 인사이트를 도출합니다. Phase 6에서 QA 체크리스트로 품질을 검증하고(실패 시 Phase 5로 회귀), Phase 7에서 최종 포맷팅과 summary_context.md 생성을 수행합니다.

Phase 6에서 QA가 실패하면 Phase 5로 돌아가 해당 부분을 수정하는 루프가 있으며, 전체 진행 상태는 state.json에 실시간으로 저장되어 어느 Phase에서든 중단 후 재개할 수 있습니다.

---

## research-workflow와의 구분

| 항목 | deep-research (이 스킬) | research-workflow |
|------|------------------------|-------------------|
| 도구 | 병렬 서브 에이전트 (Task tool) | WebSearch/WebFetch 직접 사용 |
| 규모 | 10개 이상 출처, 분량 제한 없음 | 3~10개 출처, 2~5페이지 |
| 소요 시간 | 오래 걸림 (토큰 집약적) | 빠름 (단일 세션) |
| 트리거 | "심층 리서치", "딥리서치", "/deep-research" | "조사해줘", "찾아봐", "비교해줘" |
| 체크포인트 | state.json 기반 Phase 관리 | 단계별 파일 저장 |

---

## 최종 산출물 구조

```
RESEARCH/{주제}_{timestamp}/
├── state.json                    # 세션 상태 (재개용)
├── README.md                     # 네비게이션 가이드
├── sources/
│   ├── sources.jsonl            # 수집된 소스 (1줄 = 1 JSON)
│   ├── bibliography.md          # 정리된 참고문헌
│   └── quality_report.md        # 소스 품질 분석
├── artifacts/
│   ├── research_plan.json       # 리서치 계획
│   ├── agent_results/           # 에이전트별 수집 결과
│   └── drafts/                  # 보고서 초안
├── outputs/
│   ├── full_report/
│   │   ├── 01_introduction.md
│   │   ├── 02_{서브토픽1}.md
│   │   ├── ...
│   │   ├── {N}_cross_cutting_insights.md
│   │   └── {N+1}_conclusions_and_recommendations.md
│   ├── summary_context.md       # 요약 생성용 맥락 파일
│   ├── appendices/
│   └── comparison_data.json
└── website/                     # (선택) 시각화 웹페이지
    └── index.html
```
