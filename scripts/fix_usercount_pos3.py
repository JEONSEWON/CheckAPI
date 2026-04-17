file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 현재: 배지 div → LiveUserCount → h1
# 목표: LiveUserCount → 배지 div → h1

old = '            Free for Commercial Use — No restrictions\n          </div>\n          <LiveUserCount />\n          <h1'
new = '            Free for Commercial Use — No restrictions\n          </div>\n          <h1'

if old in content:
    content = content.replace(old, new)
    # 배지 div 시작 앞에 LiveUserCount 삽입
    badge_start = content.find('text-green-700 dark:text-green-400 text-sm font-medium px-4 py-2 rounded-full mb-8">')
    line_start = content.rfind('\n', 0, badge_start) + 1
    div_line_start = content.rfind('\n', 0, line_start - 1) + 1
    content = content[:div_line_start] + '          <LiveUserCount />\n' + content[div_line_start:]
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
else:
    print("❌ 못 찾음")
