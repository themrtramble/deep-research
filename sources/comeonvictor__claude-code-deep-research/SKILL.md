---
name: deep-research
description: Use when: "딥리서치", "심층 조사", "deep research", "종합 리서치" 요청 시. 병렬 전문 에이전트로 다차원 심층 조사 후 종합 리포트를 생성합니다 (Express/Standard/Full 3티어).
argument-hint: "[리서치 주제]"
---

# Deep Research (딥리서치)

병렬 전문 에이전트가 다차원으로 조사하고, 종합 에이전트가 고품질 리서치 리포트를 생성한다.

## Important

- 퀄리티가 속도보다 중요하다. 검증 단계를 생략하지 마라.
- 모든 에이전트는 반드시 출처 URL과 신뢰도를 포함해야 한다.
- 리포트 분량은 선택한 티어에 따른다 (Express 10K / Standard 25K / Full 50K+).
- **리포트는 수집한 자료에 기반하여 최대한 상세하게 작성한다.** 에이전트가 수집한 구체적 서비스명, 수치, 사례, 인용을 리포트에 빠짐없이 반영한다. 요약은 Executive Summary에서만 하고, 본문은 자료의 풍부함을 그대로 살린다.
- **읽기 쉽되 상세해야 한다.** 테이블, 비교표, 글머리 기호를 적극 활용하여 긴 본문도 스캔하기 쉽게 구성한다. "요약했으니 짧다"가 아니라 "상세하지만 읽기 쉽다"가 목표다.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

**DO NOT just display this documentation. EXECUTE the research flow immediately.**

1. Extract the topic from user's message
2. Start Phase 0 — Use `AskUserQuestion` tool for interactive scoping
3. After user responds: Create session folder `RESEARCH/{topic}_{timestamp}/`, init `state.json`, execute Phase 1-6, deliver report.

---

## Phase 0: Scope Interview (범위 인터뷰)

리서치 시작 전, **Research Director** 페르소나로 사용자에게 질문한다.

AskUserQuestion 도구를 사용하여 아래 항목을 확인한다. 사용자 입력 언어를 감지하여 동일 언어로 생성. See [references/question_scoping.md](references/question_scoping.md) for full AskUserQuestion JSON templates.

**확인 사항:**
1. **핵심 질문**: "이 리서치로 궁극적으로 답하고 싶은 질문은 무엇인가?"
2. **깊이 vs 범위**: 좁고 깊은 분석 vs 넓고 포괄적인 서베이
3. **시간 민감도**: 최신 데이터 중요 vs 신뢰도 더 중요
4. **타겟 독자**: 전문가용 / 일반 독자용 / 의사결정자용
5. **이미 알고 있는 것**: 사용자가 이미 파악한 내용
6. **리포트 티어**: Express(빠른 의사결정) / Standard(일반) / Full(심층)

사용자 답변을 바탕으로 **Research Brief**를 작성한다:

```
RESEARCH BRIEF
- Topic: [주제]
- Core Question: [핵심 질문]
- Tier: [Express / Standard / Full]
- Depth Profile: [Deep-Narrow / Broad-Survey / Balanced]
- Freshness Priority: [High-Recency / High-Reliability / Balanced]
- Audience: [Expert / General / Decision-maker]
- Known Context: [사용자가 이미 알고 있는 내용]
- Key Sub-questions: [세부 조사 질문 3-5개]
- Agent Allocation: [에이전트 배분 전략]
```

### 티어별 규격

| 항목 | Express | Standard | Full |
|------|---------|----------|------|
| 에이전트 수 | 2개 | 3개 | 4개+ |
| 목표 분량 | ~10,000자 | ~25,000자 | 50,000자+ |
| 인용 출처 | 10개+ | 20개+ | 30개+ |
| A등급 소스 비율 | 30%+ | 35%+ | 40%+ |
| Counter-Evidence | 500자+ | 1,000자+ | 2,000자+ |

### 적응형 에이전트 배분

4개 에이전트(A/B/C/D)를 주제 특성에 따라 배분한다.

| 주제 특성 | 추천 배분 | 이유 |
|----------|----------|------|
| 건강·의학 | B×2, A, C, D | 학술 근거 핵심 |
| 기술·시장 | A×2, B, C, D | 최신 트렌드 핵심 |
| 정책·규제 | C×2, A, B, D | 기관 데이터 핵심 |
| 논쟁적 주제 | D×2, A, B, C | 다양한 관점 핵심 |
| 범용 | A, B, C, D | 균형 배분 (기본값) |

Express: 핵심 2개만 / Standard: 핵심+보조 2개(총 3개) / Full: 전체(4개+, 핵심 2배 가능)

Research Brief를 사용자에게 보여주고 확인받은 후 진행한다.

---

## Phase 1: Retrieval Planning (리서치 계획)

주제를 3-5개 서브토픽으로 분해하고, 각 서브토픽별 검색 전략을 세운다.

**Date-Aware Query Rules (필수):**
- 모든 검색 쿼리에 현재 연도 포함: BAD "AI agents market" → GOOD "AI agents market 2026"
- 시간 필터: "after:2025", "2025..2026"
- 최신성 키워드: "latest", "recent", "current"
- 한국어도 동일: "AI 에이전트 시장 2026 최신 동향"

검색 전략 수립 후 사용자에게 간략 보고하고 승인받은 후 Phase 2 진행.

---

## Phase 2: Parallel Expert Research (병렬 전문 리서치)

Agent 도구로 Research Brief의 Agent Allocation에 따라 에이전트를 **동시에** 병렬 실행한다.

각 에이전트의 상세 프롬프트는 [references/agent-prompts.md](references/agent-prompts.md)를 참조한다.

#### Agent A: Web Intelligence (웹 인텔리전스)
- 최신 뉴스, 산업 보고서, 트렌드 분석
- WebSearch, WebFetch / 최신성(Recency) 가중

#### Agent B: Academic & Scientific (학술·과학)
- 학술 논문, 메타분석, 체계적 리뷰
- WebSearch (site:pubmed, scholar 등), WebFetch / 신뢰도(Reliability) 가중

#### Agent C: Institutional & Data (기관·데이터)
- 정부 기관, 국제기구, 공식 통계, 가이드라인
- WebSearch, WebFetch / 권위성(Authority) 가중

#### Agent D: Counter-Evidence & Expert (반론·전문가)
- 반대 의견, 한계점, 논쟁, 비판적 분석
- WebSearch, WebFetch / 다양성(Diversity) 가중

**에이전트 공통 요구 (agent-prompts.md에 포함):**
- 이중 언어 검색 (영어 + 한국어)
- 모든 정보에 출처 + 신뢰도 등급
- 패턴 분석: CONSENSUS vs CONTESTED 구분
- 정보 공백(GAP) 식별
- 놀라운 발견(SURPRISING) 하이라이트

---

## Phase 3: Cross-Validation + URL Verification (교차 검증) — MUST EXECUTE

모든 에이전트 결과를 수집한 후 **반드시 실행**한다. 이 Phase를 생략하면 안 된다.

### 3-1. Claim Mapping
주요 주장별 지지 소스 수를 매핑한다.

### 3-2. Contradiction Detection
에이전트 간 상충 정보를 식별한다.

### 3-3. Gap Analysis
조사 불충분 영역을 식별한다.

### 3-4. Reliability Scoring
[references/source-evaluation.md](references/source-evaluation.md) + [references/quality_rubric.md](references/quality_rubric.md) 기준 A-E 등급 부여.

### 3-5. URL Verification (필수 실행)

에이전트가 수집한 **핵심 URL(A/B등급 소스 전체 + 핵심 주장의 C등급 소스)**에 WebFetch로 접근 확인한다.

**실행 방법:**
1. 에이전트 결과에서 모든 URL을 추출한다
2. A/B등급 소스 URL + 핵심 주장 뒷받침 URL을 선별한다 (최소 10개, 최대 20개)
3. WebFetch로 각 URL에 접근하여 상태를 확인한다
4. 결과를 태그로 기록한다:
   - `[Accessible]`: 정상 접근 가능
   - `[Paywall]`: 유료 컨텐츠 (제목/초록만 확인 가능)
   - `[URL unavailable]`: 접근 불가 (404, 서버 오류 등)
   - `[Redirect]`: 다른 URL로 리다이렉트
5. 접근 불가 URL: archive.org 검색 시도. 실패 시 `[URL unavailable - no archive]` 태그
6. **검증 결과를 state.json에 기록**하고, 리포트 참고문헌에 태그를 반영한다

**URL 검증 기준:**
- A/B등급 소스 중 접근 불가 비율이 30% 이상이면 Phase 3.5 보충 리서치 트리거
- 핵심 주장의 유일한 출처가 접근 불가이면 해당 주장에 `[Source unverified]` 표시

**Freshness vs Reliability 가중치:**
- High-Recency: 최근 2년 내 1.5x, 5년+ 0.5x
- High-Reliability: A등급 2x, C등급 이하 0.5x
- Balanced: 동일 가중, 최근 자료 약간 우대

---

## Phase 3.5: Supplementary Research (보충 리서치)

Phase 3의 Gap Analysis에 따라 **자동으로** 보충 리서치를 실행한다.

**트리거 조건** (하나라도 해당 시):
- Sub-question 중 A/B등급 소스가 1개 미만인 영역 존재
- 핵심 주장에 2개 미만의 독립 소스만 확보
- URL 검증에서 핵심 출처 30%+ 접근 불가

**제한**: 최대 1회, Express 티어에서는 생략, 보충 후에도 갭 남으면 "추가 조사 필요" 표시.

---

## Phase 4: Knowledge Synthesis (지식 종합) — CRITICAL FOR QUALITY

이 Phase가 리포트 품질을 결정한다. 단순 요약이 아닌 분석적 글쓰기를 해야 한다.

**Synthesis Requirements:**
1. **Analyze, don't summarize** — 패턴, 인과관계, 시사점 추출
2. **"So What?" test** — 모든 섹션이 "왜 중요한가"에 답해야 함
3. **Cross-cutting insights** — 서브토픽을 관통하는 통합 분석
4. **Evidence hierarchy** — 강한 근거 우선, 약한 근거는 한정어 사용
5. **Narrative arc** — 맥락 → 발견 → 분석 → 시사점 → 권고

**Insight Quality Levels:**
- L1 서술적: "X사는 Y 기능을 제공한다" → 최소 미달
- L2 비교적: "X의 접근은 Y와 3가지 차이가 있다" → 최소 기준
- L3 분석적: "X→Y 전환은 Z 트렌드를 반영한다" → **목표 수준**
- L4 전략적: "A/B/C 트렌드 수렴을 고려하면..." → **결론 섹션 수준**

**모든 섹션 L3 이상, 결론·권고 섹션 L4 도달 필수.**

**Analysis Frameworks** (주제에 맞게 선택):
| Framework | When | Output |
|-----------|------|--------|
| Comparison Matrix | 복수 플레이어/솔루션 비교 | 기능/역량 테이블 |
| Trend Analysis | 시장 진화, 기술 궤적 | 타임라인 + 방향 + 동인 |
| Causal Chain | 원인-결과 이해 | 원인→메커니즘→결과→시사점 |
| Stakeholder Impact | 기능/정책 분석 | 이해관계자별 영향 |
| Gap Analysis | 현재 vs 목표 | 존재→부족→대응 |
| SWOT | 전략적 평가 | 강점/약점/기회/위협 |

See [references/phase_contracts.md](references/phase_contracts.md) for Phase 4 contract details.

---

## Phase 5: Quality Assurance — Scoring Loop (품질 검증 루프)

리포트 작성 후 **반드시** 아래 5개 차원을 스코어링(1-5점)한다. 총점 기준 미달 시 Phase 4로 회귀하여 수정한다. **최대 2회까지 루프.**

### 스코어링 전제조건

**리포트 전체를 처음부터 끝까지 통독한 후 스코어링한다.** 구조만 보거나 일부 섹션만 읽고 점수를 매기면 안 된다. 통독하면서 아래를 체크한다:
- 출처 블록 중복이나 누락
- 메타데이터(출처 수, 등급 비율 등)와 실제 참고문헌의 불일치
- 깨진 문자 (python3으로 \ufffd 검색)
- 섹션 간 내용 반복이나 모순

### 스코어링 기준 (각 1-5점, 총 25점 만점)

**1. 상세성 (Detail) — "에이전트가 수집한 데이터가 빠짐없이 반영되었는가?"**
- 5: 에이전트 수집 서비스명, 수치, 사례가 95%+ 반영. 각 영역에 구체적 예시 3개+
- 4: 80%+ 반영. 일부 영역에 예시 부족
- 3: 60%+ 반영. 요약 수준의 섹션이 절반
- 2: 40% 미만. 대부분 요약
- 1: 에이전트 데이터 거의 미반영

**2. 가독성 (Readability) — "긴 내용이지만 스캔하기 쉬운가?"**
- 5: 테이블/비교표/글머리 적극 사용. 각 섹션에 핵심 인사이트 1줄 볼드. 시각적 계층 명확
- 4: 대부분 구조화되어 있으나 일부 장문 단락
- 3: 구조화 보통. 일부 섹션이 벽처럼 느껴짐
- 2: 대부분 장문 단락. 스캔 어려움
- 1: 구조 없는 텍스트 덩어리

**3. 분석 수준 (Insight Level) — "L3(분석적) 이상인가?"**
- 5: 대부분 L3-L4. 패턴, 인과관계, 전략적 시사점 풍부. 결론이 L4
- 4: L3 수준. 일부 L2(비교적) 섹션 존재
- 3: L2-L3 혼재. 결론은 L3
- 2: 대부분 L2(비교 나열). 인과 분석 부족
- 1: L1(사실 나열) 수준

**4. 출처 품질 (Source Quality) — "신뢰할 수 있는 근거에 기반하는가?"**
- 5: A등급 40%+. 핵심 주장에 2개+ 독립 소스. 상충 정보 인정. URL 검증 완료
- 4: A등급 30%+. 대부분 주장에 출처. 일부 단독 소스
- 3: A등급 20%+. 출처 있으나 일부 주장이 근거 부족
- 2: 출처 불충분. 많은 주장이 단독 소스
- 1: 출처 거의 없음

**5. 실행 가능성 (Actionability) — "읽고 나서 무엇을 해야 하는지 알 수 있는가?"**
- 5: 우선순위 매트릭스 + 구체적 벤치마크 + next steps 명확. 의사결정에 바로 사용 가능
- 4: 권고가 구체적이나 일부 추상적
- 3: 권고는 있으나 우선순위/구체성 부족
- 2: 정보 전달에 그침. "그래서 어쩌라는 건지" 불명확
- 1: 실행 가능한 제안 없음

### 합격 기준 (티어별)

| 티어 | 최소 총점 | 개별 최소 | 상세성 최소 |
|------|---------|---------|-----------|
| Express | 15/25 | 각 2+ | 3+ |
| Standard | 18/25 | 각 3+ | 4+ |
| Full | 20/25 | 각 3+ | 4+ |

### 루프 프로세스

1. 리포트 작성 완료 (Phase 4)
2. 5개 차원 스코어링 실행
3. **합격**: Phase 6으로 진행
4. **불합격**: 가장 낮은 점수의 차원을 식별하고, 해당 부분만 Phase 4에서 보강
5. 재스코어링 (2차)
6. 2차에서도 불합격이면: 사용자에게 현재 점수와 부족한 영역을 보고하고, 추가 리서치 여부 확인
7. 스코어링 결과를 state.json에 기록하고, 리포트 끝에 QA Score 섹션으로 포함

### 스코어링 출력 형식

```
QA SCORECARD (Attempt N/2)
- Detail:       [N]/5 - [한 줄 사유]
- Readability:  [N]/5 - [한 줄 사유]
- Insight:      [N]/5 - [한 줄 사유]
- Source:       [N]/5 - [한 줄 사유]
- Actionability:[N]/5 - [한 줄 사유]
- TOTAL:        [N]/25
- VERDICT:      PASS / FAIL (재작성 필요: [차원명])
```

---

## Phase 6: Output & Packaging (최종 산출물)

[references/report-template.md](references/report-template.md)의 티어별 구조를 따라 최종 리포트를 작성한다.

**산출물:**
1. **리포트**: `{output-dir}/{topic-slug}_deep-research_v1.md`
2. **Claim DB**: `{output-dir}/{topic-slug}_claims_v1.yaml` — 후속 리서치 재활용용
3. **summary_context.md**: 요약 생성용 맥락 파일 (핵심 발견, 뉘앙스, 미해결 질문)
4. output-dir 기본값: `RESEARCH/{topic}_{timestamp}/outputs/`

리포트 완성 후 사용자에게 보고:
1. 파일 경로 (리포트 + Claim DB)
2. 총 분량 / 티어
3. 인용 출처 수 (접근 가능/불가 비율)
4. 핵심 발견 3-5개 요약
5. 추가 조사 필요 영역

---

## Phase 7: Summary on Demand (POST-COMPLETION)

리포트 완성 후 사용자가 요약을 요청할 때만 실행.

1. 전체 리포트 + summary_context.md를 읽음
2. 요청된 깊이로 요약 생성 (핵심 맥락 보존)

summary_context.md에는: 핵심 발견(중요도순), 요약 시 잃으면 안 되는 뉘앙스, Cross-cutting Insights, 한계와 미해결 질문이 포함됨.

---

## Gotchas

1. **리포트 요약 과다**: 에이전트가 수집한 상세 데이터(서비스명, 수치, 사례)를 종합 리포트에서 빠뜨리는 실수가 빈번. Phase 5 상세성(Detail) 스코어로 방지
2. **Phase 3 URL 검증 생략**: 시간이 오래 걸린다는 이유로 URL 검증을 건너뛰는 경향. 핵심 URL 10-20개는 반드시 WebFetch로 확인해야 함
3. **Phase 5 스코어링 자체를 생략**: 리포트 작성 후 바로 사용자에게 전달하려는 경향. 반드시 5차원 스코어링을 거쳐야 함
4. **글자 깨짐**: 한글+특수문자(별표, 동그라미 등) 혼합 시 UTF-8 인코딩 문제 발생 가능. 리포트 작성 후 깨진 문자 검사 필수 (python3으로 \ufffd 검색)
5. **에이전트 결과 JSON 형식**: 서브 에이전트의 output이 JSON 로그 형태일 수 있음. 실제 텍스트 내용을 추출해서 읽어야 함

---

## Hallucination Prevention

1. 모든 주장에 검증 가능한 출처 필수. 불확실하면 "Source needed"
2. 핵심 주장에 Chain-of-Verification 적용
3. 핵심 발견에 2개+ 독립 소스 교차 확인
4. "According to [source]..." 형식. "Studies show..." 금지

---

## State Management & Resume

See [references/state_schema.md](references/state_schema.md) for `state.json` schema.

`/research-resume [session_id]` 호출 시:
1. `RESEARCH/*/state.json` 목록에서 세션 선택
2. `progress` 객체에서 마지막 완료 Phase 확인
3. 다음 pending Phase부터 재개

---

## Error Handling

### Phase Failures
1. state.json errors 배열에 기록 → phase를 `failed`로 표시 → 사용자에게 알림
2. 제안: Retry / Skip / Abort

### Agent Failures
- WebSearch 권한 문제: 메인 컨텍스트에서 직접 실행으로 폴백
- 소스 부족: 검색 키워드 확장 후 재시도
- 상충 결과: Phase 3 교차 검증으로 플래그

---

## Output Structure

See [references/overview.md](references/overview.md) for full output directory tree.

```
RESEARCH/{topic}_{timestamp}/
├── state.json
├── sources/
│   ├── sources.jsonl
│   └── bibliography.md
├── outputs/
│   ├── {topic}_deep-research_v1.md     # 최종 리포트
│   ├── {topic}_claims_v1.yaml          # Claim DB
│   └── summary_context.md
└── artifacts/
    ├── research_plan.json
    └── agent_results/
```
