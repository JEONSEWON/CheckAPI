FILE = r"C:\home\jeon\api-health-monitor\frontend\app\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

# Features 섹션 Instant Alerts 설명 수정
old_desc = "Check every minute. Email, Slack, Telegram, Discord, Webhook — all on the free plan."
new_desc = "Free plan checks every 5 minutes. Upgrade to Starter for 1-minute checks, Pro for 30-second. Email, Slack, Telegram, Discord, Webhook — all plans."
c = c.replace(old_desc, new_desc)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!", new_desc in c)
