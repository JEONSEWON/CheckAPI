import os

# 1. config.py에 RESEND_API_KEY 추가
config_path = "backend/app/config.py"
with open(config_path, "r", encoding="utf-8") as f:
    content = f.read()

old_config = '''    # SendGrid
    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@apihealthmonitor.com"'''

new_config = '''    # Email (Resend)
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@checkapi.io"

    # SendGrid (legacy)
    SENDGRID_API_KEY: str = ""'''

if old_config in content:
    content = content.replace(old_config, new_config)
    with open(config_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ config.py 완료!")
else:
    print("❌ config.py 패턴 못 찾음")

# 2. requirements.txt에 sendgrid 제거, resend는 requests로 처리하므로 별도 패키지 불필요
req_path = "backend/requirements.txt"
with open(req_path, "r", encoding="utf-8") as f:
    req = f.read()

old_req = "# Email\nsendgrid==6.11.0"
new_req = "# Email (Resend - uses requests library)"

if old_req in req:
    req = req.replace(old_req, new_req)
    with open(req_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(req)
    print("✅ requirements.txt 완료!")
else:
    print("⚠️  requirements.txt sendgrid 못 찾음 (이미 제거됐을 수 있음)")

print("\n완료!")
