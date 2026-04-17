file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# LiveUserCount import 추가
if "LiveUserCount" not in content:
    old_import = "import ClientHeader from '@/components/ClientHeader';"
    new_import = "import ClientHeader from '@/components/ClientHeader';\nimport LiveUserCount from '@/components/LiveUserCount';"
    content = content.replace(old_import, new_import)

# "Free for Commercial Use" 배지 앞에 LiveUserCount 삽입
old_badge = 'Free for Commercial Use — No restrictions'
idx = content.find(old_badge)

if idx == -1:
    print("❌ 배지 못 찾음")
else:
    # 해당 줄 시작 찾기
    line_start = content.rfind('\n', 0, idx) + 1
    # 그 줄이 포함된 div 블록 시작 찾기 (한 줄 더 위)
    prev_line_start = content.rfind('\n', 0, line_start - 1) + 1

    live_count_jsx = '          <LiveUserCount />\n'

    if '<LiveUserCount />' not in content:
        content = content[:prev_line_start] + live_count_jsx + content[prev_line_start:]
        print("✅ LiveUserCount 삽입 완료!")
    else:
        print("⚠️  이미 삽입됨")

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 랜딩 페이지 완료!")
