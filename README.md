# CheckAPI - API Health Monitor

**Monitor Your APIs 24/7 with Instant Alerts**

[![Live Demo](https://img.shields.io/badge/demo-checkapi.io-green)](https://checkapi.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Built with FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Built with Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)](https://nextjs.org/)

[Live Demo](https://checkapi.io) · [Report Bug](https://github.com/JEONSEWON/api-health-monitor/issues) · [Request Feature](https://github.com/JEONSEWON/api-health-monitor/issues)

---

## 🚀 About CheckAPI

CheckAPI is a powerful yet simple **API health monitoring service** that tracks your APIs and websites 24/7. Get **instant alerts** via multiple channels when your services go down.

Built for developers who are tired of paying $75/mo for basic monitoring — CheckAPI offers a generous free tier with **no commercial restrictions**.

---

## ✨ Features

### Core Monitoring
- 🔍 **HTTP/HTTPS Monitoring** — GET, POST, PUT, DELETE, PATCH support
- 🔑 **Custom Headers & Body** — Simulate real API requests
- ✅ **Status Code Validation** — Expected status code checking
- 📝 **Response Body Keyword Validation** — Check if a keyword is present or absent in the response body (e.g. `"status":"ok"`)
- 🔒 **SSL Certificate Expiry Alerts** — Get notified 14 days before your cert expires
- ⏱️ **Response Time Tracking** — Monitor API performance in ms
- 📊 **Uptime Calculation** — 24h / 7d / 30d uptime %

### Alert Channels (5 Options)
- 📧 **Email**
- 💬 **Slack**
- 📱 **Telegram**
- 🎮 **Discord**
- 🔗 **Custom Webhook**

### Analytics & Dashboard
- Real-time monitor status dashboard
- Response time charts
- Incident history & timeline
- Public Status Page (shareable link)

### Team Collaboration
- Invite team members via email
- Members can view and manage owner's monitors
- Pro plan: up to 5 members / Business: unlimited

---

## 💰 Pricing

| Plan | Price | Monitors | Interval | History | Team |
|---|---|---|---|---|---|
| **Free** | $0/mo | 10 | 5 min | 7 days | ❌ |
| **Starter** | $5/mo | 20 | 1 min | 30 days | ❌ |
| **Pro** | $15/mo | 100 | 30 sec | 90 days | ✅ (5명) |
| **Business** | $49/mo | Unlimited | 10 sec | 1 year | ✅ (무제한) |

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
- **HTTP:** Axios

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
  2. Response body keyword (if set)
  3. Response time (ms)
        ↓
Status: up / degraded / down
        ↓
Status change → Alert sent
(Email / Slack / Telegram / Discord / Webhook)
        ↓
Results saved to PostgreSQL
(Retained: 7 / 30 / 90 / 365 days by plan)
        ↓
Daily 9AM → SSL certificate expiry check
Daily 3AM → Old data cleanup
```

---

## 🚦 Quick Start

### For Users
1. Sign up at [checkapi.io](https://checkapi.io)
2. Create a monitor (URL, method, interval, expected status)
3. Add an alert channel (Email, Slack, Telegram, etc.)
4. Get notified when something goes wrong

### For Developers

#### Backend Setup
```bash
git clone https://github.com/JEONSEWON/api-health-monitor.git
cd api-health-monitor/backend

pip install -r requirements.txt
cp .env.example .env
# Edit .env

uvicorn app.main:app --reload
# In separate terminal:
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
- **GitHub:** https://github.com/JEONSEWON/api-health-monitor

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
