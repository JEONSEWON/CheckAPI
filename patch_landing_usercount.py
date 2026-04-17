file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# LiveUserCount import 추가
old_import = "import ClientHeader from '@/components/ClientHeader';"
new_import = "import ClientHeader from '@/components/ClientHeader';\nimport LiveUserCount from '@/components/LiveUserCount';"

content = content.replace(old_import, new_import)

# "Free for Commercial Use" 배지 위에 LiveUserCount 삽입
# 배지가 어떤 형태인지 찾기
old_badge = '✅ Free for Commercial Use'
idx = content.find(old_badge)

if idx == -1:
    print("❌ 배지 못 찾음")
else:
    # 배지가 포함된 div/span 시작 찾기 — 줄 시작으로 거슬러 올라가기
    line_start = content.rfind('\n', 0, idx) + 1
    badge_line = content[line_start:idx + 50]
    print("배지 줄:", repr(badge_line[:100]))

    # <LiveUserCount /> 를 배지 바로 앞 줄에 삽입
    insert_point = line_start
    live_count_jsx = '          <LiveUserCount />\n'
    content = content[:insert_point] + live_count_jsx + content[insert_point:]

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 랜딩 페이지 완료!")
