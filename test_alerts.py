"""
Alert channel test script.
Run from backend directory with DATABASE_URL and RESEND_API_KEY set.

Usage:
  cd backend
  DATABASE_URL=... RESEND_API_KEY=... python ../test_alerts.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.alerts import (
    send_email_alert,
    send_slack_alert,
    send_discord_alert,
    send_telegram_alert,
    send_webhook_alert,
)

MONITOR_NAME = "CheckAPI Test Monitor"
MONITOR_URL = "https://checkapi.io"
NEW_STATUS = "down"
OLD_STATUS = "up"

print("=" * 50)
print("CheckAPI Alert Channel Test")
print("=" * 50)

# ── 1. Email (Resend) ──────────────────────────────────
TEST_EMAIL = os.environ.get("TEST_EMAIL", "wjsypdnjs123@gmail.com")
print(f"\n[1] Email → {TEST_EMAIL}")
result = send_email_alert(
    {"email": TEST_EMAIL},
    MONITOR_NAME, MONITOR_URL, NEW_STATUS, OLD_STATUS
)
print(f"    {'✅ OK' if result else '❌ FAIL'}")

# ── 2. Slack ───────────────────────────────────────────
SLACK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
if SLACK_URL:
    print(f"\n[2] Slack Webhook")
    result = send_slack_alert(
        {"webhook_url": SLACK_URL},
        MONITOR_NAME, MONITOR_URL, NEW_STATUS, OLD_STATUS
    )
    print(f"    {'✅ OK' if result else '❌ FAIL'}")
else:
    print("\n[2] Slack → SKIPPED (set SLACK_WEBHOOK_URL env var to test)")

# ── 3. Discord ─────────────────────────────────────────
DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
if DISCORD_URL:
    print(f"\n[3] Discord Webhook")
    result = send_discord_alert(
        {"webhook_url": DISCORD_URL},
        MONITOR_NAME, MONITOR_URL, NEW_STATUS, OLD_STATUS
    )
    print(f"    {'✅ OK' if result else '❌ FAIL'}")
else:
    print("\n[3] Discord → SKIPPED (set DISCORD_WEBHOOK_URL env var to test)")

# ── 4. Telegram ────────────────────────────────────────
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT  = os.environ.get("TELEGRAM_CHAT_ID", "")
if TG_TOKEN and TG_CHAT:
    print(f"\n[4] Telegram")
    result = send_telegram_alert(
        {"bot_token": TG_TOKEN, "chat_id": TG_CHAT},
        MONITOR_NAME, MONITOR_URL, NEW_STATUS, OLD_STATUS
    )
    print(f"    {'✅ OK' if result else '❌ FAIL'}")
else:
    print("\n[4] Telegram → SKIPPED (set TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID)")

# ── 5. Custom Webhook (webhook.site) ───────────────────
WEBHOOK_URL = os.environ.get("TEST_WEBHOOK_URL", "")
if WEBHOOK_URL:
    print(f"\n[5] Custom Webhook → {WEBHOOK_URL}")
    result = send_webhook_alert(
        {"url": WEBHOOK_URL},
        MONITOR_NAME, MONITOR_URL, NEW_STATUS, OLD_STATUS, "test-channel-id"
    )
    print(f"    {'✅ OK' if result else '❌ FAIL'}")
else:
    print("\n[5] Custom Webhook → SKIPPED (set TEST_WEBHOOK_URL env var to test)")

print("\n" + "=" * 50)
print("Done.")
