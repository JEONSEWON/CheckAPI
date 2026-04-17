FILE = r"C:\home\jeon\api-health-monitor\README.md"

content = r"""# CheckAPI — API Health Monitor

**APIs that never lie to you.**

[![Live Demo](https://img.shields.io/badge/demo-checkapi.io-green)](https://checkapi.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/JEONSEWON/CheckAPI/blob/main/LICENSE)
[![Built with FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Built with Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)](https://nextjs.org/)

[Live Demo](https://checkapi.io) · [Report Bug](https://github.com/JEONSEWON/CheckAPI/issues) · [Request Feature](https://github.com/JEONSEWON/CheckAPI/issues)

---

## 🚀 About CheckAPI

CheckAPI is a minimalist **API health monitoring service** built for solo founders and small teams. Monitor your APIs 24/7, catch silent failures before your users do, and get instant alerts across multiple channels.

> **Free for Commercial Use** — Unlike UptimeRobot (which restricted commercial use in late 2024), CheckAPI has zero commercial restrictions on all plans.

---

## ✨ Features

### Core Monitoring

- 🔍 **HTTP/HTTPS Monitoring** — GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- 💓 **Heartbeat / Cron Job Monitoring** — Monitor scheduled tasks. Get alerted if your job doesn't run on time.
- 🔑 **Custom Headers & Body** — Simulate real API requests
- ✅ **Status Code Validation** — Expected HTTP status code checking
- ⏱️ **Response Time Tracking** — Monitor performance in milliseconds
- 📊 **Response Time Percentiles** — p50 / p95 / p99 per monitor

### Silent Failure Detection

A 200 OK response doesn't always mean your API is healthy. CheckAPI goes deeper:

- 🔤 **Keyword Validation** — Check if a keyword is present or absent in the response body
- 🧠 **Regex Pattern Matching** — Validate response body with precision using regular expressions

```
# Status field must be "ok" or "healthy"
regex: "status":\s*"(ok|healthy)"

# Balance must be positive
regex: "balance":\s*[1-9]\d*

# Error field must be null
regex: "error":\s*null
```

- 🗂️ **JSON Path Assertions** — Up to 10 assertions per monitor with AND/OR logic

```
$.data.status == "ok"
$.data.balance > 0
$.error is null
$.items[*].active exists
```

Supported operators: `==`, `!=`, `>`, `>=`, `<`, `<=`, `contains`, `not_contains`, `is_null`, `is_not_null`, `exists`

- 🏷️ **Header Assertion** — Validate response headers (e.g. `Content-Type`, `X-Status`)
- 🔴 **Regex Live Tester** — Test patterns against real response bodies directly in the dashboard
- 🧪 **JSON Path Live Tester** — Paste sample JSON and verify assertions instantly

### Alert Channels

- 📧 Email
- 💬 Slack
- 📱 Telegram
- 🎮 Discord
- 🔗 Custom Webhook

All channels support **test alerts** before going live. Attach multiple channels per monitor.

### Analytics & Reporting

- Real-time monitor status dashboard
- Response time graphs (24h)
- Response time percentiles (p50 / p95 / p99)
- Incident history & timeline
- SLA reports (Pro / Business)
- Check history with pagination (30 / 90 / 365 days by plan)

### Public Status Pages

- Shareable `/status/{monitor_id}` — no login required
- 90-day uptime bar chart with hover tooltips
- 24h / 7d / 30d uptime stats
- Average response time & recent incidents

### Maintenance Windows

- Schedule recurring windows (daily / weekly / monthly / one-time)
- Alerts suppressed during active windows — checks still run
- Timezone-aware (Asia/Seoul, UTC, US timezones, etc.)
- Apply to specific monitors or all monitors

### Business Plan

- REST API access via API Keys (`X-API-Key` header)
- Programmatic monitor management
- 365-day check history

---

## 💰 Pricing

| Plan | Price | Monitors | Interval | History | Team |
|------|-------|----------|----------|---------|------|
| **Free** | $0/mo | 10 | 5 min | 30 days | — |
| **Starter** | $5/mo | 20 | 1 min | 30 days | Coming soon |
| **Pro** | $15/mo | 100 | 30 sec | 90 days | Coming soon |
| **Business** | $49/mo | Unlimited | 10 sec | 365 days | Coming soon |

Annual billing available at **20% discount** on all paid plans.

✅ No commercial restrictions on any plan
✅ No credit card required for free tier
✅ Cancel anytime

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Task Queue:** Celery + Celery Beat
- **Database:** PostgreSQL
- **Cache/Broker:** Redis
- **ORM:** SQLAlchemy
- **Auth:** JWT
- **Payment:** LemonSqueezy
- **Email:** Resend

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State:** Zustand

### Deployment
- **Backend:** Railway US West (FastAPI + Celery Worker + Redis + PostgreSQL)
- **Frontend:** Vercel
- **DNS:** Cloudflare
- **Domain:** checkapi.io

---

## 🔄 How It Works

```
User registers a monitor
        ↓
Celery Worker checks URL periodically
(Free: 5min / Starter: 1min / Pro: 30sec / Business: 10sec)
        ↓
Checks:
  1. HTTP status code
  2. Response body — keyword / regex / JSON Path / header assertion
  3. Response time (ms)
        ↓
Status: up / degraded / down
        ↓
Check maintenance window → Send alert if not in maintenance
(Email / Slack / Telegram / Discord / Webhook)
        ↓
Results saved to PostgreSQL
(Retained: 30 / 30 / 90 / 365 days by plan)
        ↓
Heartbeat monitors: Celery checks last_ping_at every minute
Daily 9AM → SSL certificate expiry check
Daily 3AM → Old data cleanup
```

---

## 🚦 Quick Start

### For Users

1. Sign up at [checkapi.io](https://checkapi.io)
2. Click **+ Add Monitor** — choose HTTP or Heartbeat/Cron
3. Add an alert channel (Email, Slack, Telegram, etc.)
4. Optionally add Silent Failure Detection (keyword, regex, JSON Path, or header assertion)
5. Get notified the moment something goes wrong

### Heartbeat / Cron Job Example

```bash
# Add to your cron job
0 3 * * * /scripts/backup.sh && curl https://checkapi.io/api/v1/heartbeat/YOUR_TOKEN
```

```python
# Or in your Python script
import requests
run_backup()
requests.get("https://checkapi.io/api/v1/heartbeat/YOUR_TOKEN")
```

### For Developers

```bash
git clone https://github.com/JEONSEWON/CheckAPI.git
cd CheckAPI/backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# In a separate terminal:
celery -A app.celery_app worker --beat --loglevel=info
```

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

---

## 📊 Current Status

- **Live at:** https://checkapi.io
- **Backend API:** https://api-health-monitor-production.up.railway.app
- **Stage:** Early users, payment system live

---

## 📬 Contact

- **Website:** [checkapi.io](https://checkapi.io)
- **Twitter:** [@imwon_dev](https://x.com/imwon_dev)
- **GitHub:** [@JEONSEWON](https://github.com/JEONSEWON)

---

## 📝 License

MIT License — free to use, fork, and learn from.

---

**Built by a solo dev from Seoul 🇰🇷**

[Get Started for Free →](https://checkapi.io)
"""

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!", len(content), "chars")
