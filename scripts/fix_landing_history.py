file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = "'7-day history'"
new = "'30-day history'"

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 교체 성공!")
else:
    print("❌ 못 찾음")
