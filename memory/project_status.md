---
name: CheckAPI 구현 현황
description: 구현 완료 기능 전체 목록, 미구현 항목, 최근 작업 이력
type: project
---

## 구현 완료

### 모니터링 코어
- HTTP (GET/POST/PUT/DELETE/PATCH), Custom Headers/Body, 상태코드 검증
- 응답 시간 추적 (ms), 업타임 계산 (24h/7d/30d)
- SSL 인증서 만료 감지 (14일 전)
- Heartbeat / Cron 모니터링
- Silent Failure Detection: 키워드·정규식·JSON Path·헤더 어설션
- **N회 연속 실패 후 알림 (alert_threshold)** ← 2026-04-22 구현

### 알림 (전 플랜)
- Email (Resend), Slack, Telegram, Discord, Custom Webhook
- 알림 채널 Test 버튼 (UI) ← 2026-04-22 추가

### 대시보드 & 분석
- 모니터 목록, 상세 (차트·인시던트), Analytics, SLA Report (Pro/Business)
- Public Status Page (/status/{id}), Status Badge

### 팀 & 접근제어
- 이메일 초대, 팀원 관리, API Key (Business 전용)

### 결제
- LemonSqueezy 체크아웃·웹훅·취소, 중복 구독 upsert 처리

### 인프라
- JWT (Access+Refresh), Celery Worker+Beat, Maintenance Window
- 플랜별 제한 강제 (모니터 수·인터벌·히스토리 보관)

---

## 미구현 (확인된 것만)

| 항목 | 비고 |
|------|------|
| 온보딩 이메일 시퀀스 | 가입 후 활성화 이메일 없음 |
| 구독 취소/다운그레이드 UI | 백엔드만, 프론트 UX 불명확 |
| WebSocket 실시간 대시보드 | 현재 폴링 방식 |
| Multi-region 체크 | 미구현 |
| Zapier / Make 연동 | 미구현 |
| 팀 권한 세분화 | 단일 권한만 |

---

## 최근 작업 이력 (2026-04-22)

- `alert_threshold` / `consecutive_failures` DB 컬럼 추가 → migrate_alert_threshold.py 실행 필요
- tasks.py: threshold 도달 시에만 알림, 복구는 항상 즉시 알림
- CreateMonitorModal: 1/2/3/5회 드롭다운 UI 추가
- Alerts 페이지: 채널별 Test 버튼 추가 (FlaskConical 아이콘)
- lib/api.ts: monitorsAPI.create 타입에 누락 필드 추가 (TypeScript 빌드 오류 수정)

**Why:** alert_threshold는 플리커 다운으로 인한 알림 폭탄 방지 목적
**How to apply:** 신규 모니터는 기본값 1 (기존 동작 동일), DB 마이그레이션 필수
