# CheckAPI — API Health Monitor

**Monitor Your APIs 24/7 with Instant Alerts**

[![Live Demo](https://img.shields.io/badge/demo-checkapi.io-green)](https://checkapi.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/JEONSEWON/CheckAPI/blob/main/LICENSE)
[![Built with FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Built with Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)](https://nextjs.org/)

[Live Demo](https://checkapi.io) · [Report Bug](https://github.com/JEONSEWON/CheckAPI/issues) · [Request Feature](https://github.com/JEONSEWON/CheckAPI/issues)

---

## 🚀 About CheckAPI

CheckAPI is a minimalist **API health monitoring service** built for solo founders and small teams. Monitor your APIs 24/7, catch silent failures before your users do, and get instant alerts across multiple channels.

Built after getting tired of enterprise tools that are too bloated and free tools with too many restrictions. CheckAPI does one thing well — **tells you when your API is broken, before anyone else finds out.**

> **Free for Commercial Use** — Unlike UptimeRobot (which restricted commercial use on free plans in late 2024), CheckAPI has zero commercial restrictions on all plans.

---

## ✨ Features

### Core Monitoring

- 🔍 **HTTP/HTTPS Monitoring** — GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- 🔑 **Custom Headers & Body** — Simulate real API requests
- ✅ **Status Code Validation** — Expected HTTP status code checking
- 🧠 **Silent Failure Detection** — Your API returns 200 OK but the body says "error"? CheckAPI catches it via keyword or **Regex pattern** matching
- ⏱️ **Response Time Tracking** — Monitor performance in milliseconds
- 📊 **Uptime Calculation** — 24h / 7d / 30d uptime %

### Alert Channels

- 📧 Email
- 💬 Slack
- 📱 Telegram
- 🎮 Discord
- 🔗 Custom Webhook

All channels support **test alerts** before going live.

### Analytics & Reporting

- Real-time monitor status dashboard
- Response time graphs
- Incident history & timeline
- SLA reports (Pro / Business)
- CSV export of check history

### Public Status Pages

- Shareable `/status/{monitor_id}` page — no login required
- 90-day uptime bar chart with hover tooltips
- 24h / 7d / 30d uptime stats
- Average response time & recent incidents
- "Powered by CheckAPI" backlink

### Maintenance Windows

- Schedule recurring maintenance windows (daily / weekly / monthly / one-time)
- Alerts are suppressed during active windows — checks still run
- Timezone-aware
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
- **Backend:** Railway (FastAPI + Celery Worker + Redis + PostgreSQL)
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
  2. Response body — keyword or regex match (Silent Failure Detection)
  3. Response time (ms)
        ↓
Status: up / degraded / down
        ↓
Status change → Check maintenance window → Send alert if not in maintenance
(Email / Slack / Telegram / Discord / Webhook)
        ↓
Results saved to PostgreSQL
(Retained: 30 / 30 / 90 / 365 days by plan)
        ↓
Daily 9AM → SSL certificate expiry check
Daily 3AM → Old data cleanup
```

---

## 🚦 Quick Start

### For Users

1. Sign up at [checkapi.io](https://checkapi.io)
2. Click **+ Add Monitor** — enter URL, method, interval
3. Add an alert channel (Email, Slack, Telegram, etc.)
4. Optionally add Silent Failure Detection keyword or regex
5. Get notified the moment something goes wrong

### For Developers

#### Backend Setup

```bash
git clone https://github.com/JEONSEWON/CheckAPI.git
cd CheckAPI/backend

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials

uvicorn app.main:app --reload

# In a separate terminal:
celery -A app.celery_app worker --beat --loglevel=info
```

#### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local
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
