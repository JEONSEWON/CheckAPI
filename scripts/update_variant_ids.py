file_path = "backend/app/lemonsqueezy.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = '''PLAN_VARIANTS = {
    "starter": "1309924",  # API Health Monitor - Starter ($5/month)
    "pro": "1309944",      # API Health Monitor - Pro ($15/month)
    "business": "1309949"  # API Health Monitor - Business ($49/month)
}'''

new = '''PLAN_VARIANTS = {
    "starter": "1451933",  # CheckAPI Starter ($5/month)
    "pro": "1451947",      # CheckAPI Pro ($15/month)
    "business": "1451953"  # CheckAPI Business ($49/month)
}'''

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ Variant ID 업데이트 완료!")
else:
    print("❌ 못 찾음")
