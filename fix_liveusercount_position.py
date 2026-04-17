file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 현재: div 안에 LiveUserCount가 들어가 있음
# 수정: div 앞으로 꺼내기

old = '          <LiveUserCount />\n            <CheckCircle className="h-4 w-4" />\n            Free for Commercial Use — No restrictions\n          </div>'

new = '            <CheckCircle className="h-4 w-4" />\n            Free for Commercial Use — No restrictions\n          </div>\n          <LiveUserCount />'

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
else:
    print("❌ 못 찾음")
