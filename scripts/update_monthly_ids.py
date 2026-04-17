file_path = "backend/app/lemonsqueezy.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = '''PLAN_VARIANTS = {
    "starter": "923370",          # CheckAPI Starter Monthly ($5/month)
    "pro": "923382",              # CheckAPI Pro Monthly ($15/month)
    "business": "923386",         # CheckAPI Business Monthly ($49/month)
    "starter_annual": "1451933",  # CheckAPI Starter Annual ($48/year)
    "pro_annual": "1451947",      # CheckAPI Pro Annual ($144/year)
    "business_annual": "1451953", # CheckAPI Business Annual ($470/year)
}'''

new = '''PLAN_VARIANTS = {
    "starter": "1454010",         # CheckAPI Starter Monthly ($5/month)
    "pro": "1454012",             # CheckAPI Pro Monthly ($15/month)
    "business": "1454016",        # CheckAPI Business Monthly ($49/month)
    "starter_annual": "1451933",  # CheckAPI Starter Annual ($48/year)
    "pro_annual": "1451947",      # CheckAPI Pro Annual ($144/year)
    "business_annual": "1451953", # CheckAPI Business Annual ($470/year)
}'''

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
else:
    print("❌ 못 찾음")
