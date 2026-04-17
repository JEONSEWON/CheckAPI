# ── 1. ClientHeader.tsx ──────────────────────────────────────────────────────
FILE1 = r"C:\home\jeon\api-health-monitor\frontend\components\ClientHeader.tsx"

with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()

old_logo = """          <div className="flex items-center">
            <span className="text-2xl font-bold
bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              CheckAPI
            </span>
          </div>"""

new_logo = """          <div className="flex items-center">
            <img src="/logo.jpg" alt="CheckAPI" className="h-9 w-9 rounded-lg object-cover" />
          </div>"""

if old_logo in c:
    c = c.replace(old_logo, new_logo)
    print("ClientHeader: exact match replaced!")
else:
    # 줄바꿈 차이 대비 - 라인 기반 교체
    lines = c.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        if 'flex items-center' in lines[i] and i+1 < len(lines) and 'text-2xl font-bold' in lines[i+1]:
            # 이 블록 전체를 새 로고로 교체
            new_lines.append('          <div className="flex items-center">')
            new_lines.append('            <img src="/logo.jpg" alt="CheckAPI" className="h-9 w-9 rounded-lg object-cover" />')
            new_lines.append('          </div>')
            # 기존 블록 스킵 (닫는 div까지)
            depth = 0
            while i < len(lines):
                if '<div' in lines[i]: depth += 1
                if '</div>' in lines[i]: depth -= 1
                i += 1
                if depth == 0: break
        else:
            new_lines.append(lines[i])
            i += 1
    c = '\n'.join(new_lines)
    print("ClientHeader: line-based replacement done!")

with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)

print("ClientHeader logo:", '/logo.jpg' in c)


# ── 2. DashboardLayout.tsx ────────────────────────────────────────────────────
FILE2 = r"C:\home\jeon\api-health-monitor\frontend\components\DashboardLayout.tsx"

with open(FILE2, 'r', encoding='utf-8') as f:
    c2 = f.read()

# 텍스트 span 제거, 이미지 크기 조정
old_dash = """              <img src="/logo.jpg" alt="CheckAPI Logo" className="h-10 w-10 rounded-lg object-cover" />
              <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">CheckAPI</span>"""

new_dash = """              <img src="/logo.jpg" alt="CheckAPI" className="h-10 w-10 rounded-lg object-cover" />"""

if old_dash in c2:
    c2 = c2.replace(old_dash, new_dash)
    print("DashboardLayout: replaced!")
else:
    # 라인 기반
    lines2 = c2.split('\n')
    new_lines2 = []
    skip_next = False
    for i, line in enumerate(lines2):
        if skip_next:
            skip_next = False
            continue
        if 'text-2xl font-bold' in line and 'CheckAPI' in lines2[i+1] if i+1 < len(lines2) else False:
            skip_next = True
            continue
        if 'text-2xl font-bold bg-gradient' in line and 'CheckAPI' in line:
            continue
        new_lines2.append(line)
    c2 = '\n'.join(new_lines2)
    print("DashboardLayout: line-based done!")

with open(FILE2, 'w', encoding='utf-8') as f:
    f.write(c2)

print("DashboardLayout logo:", '/logo.jpg' in c2)
print("DashboardLayout text removed:", 'CheckAPI</span>' not in c2)
