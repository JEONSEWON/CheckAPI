---
name: AI 기능 Phase 3 계획
description: Phase 1/2 완료 후 논의된 Phase 3 AI 기능 로드맵
type: project
---

## 완료
- Phase 1: Anthropic SDK 도입 (commit: 693e0fe)
- Phase 2: Incident Analyzer — Claude Haiku + ai_analysis 컬럼 + 알림 템플릿 + UI 배지 (commit: 5124da5)

## Phase 3 계획 (미구현)

| 기능 | 특징 |
|------|------|
| Setup Wizard | 프론트+백엔드 독립적, 빠르게 완성 가능 |
| SLA Report | Celery Beat 스케줄 + 이메일 템플릿 |

**Why:** 사용자 온보딩 전환율 개선 (Setup Wizard) + Pro/Business 플랜 가치 강화 (SLA Report)
**How to apply:** Setup Wizard 먼저 → SLA Report 순서로 진행 예정
