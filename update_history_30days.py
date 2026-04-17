import os

changes = [
    # 백엔드 analytics.py
    {
        "file": "backend/app/routers/analytics.py",
        "old": '"free": 7,',
        "new": '"free": 30,',
    },
    # 백엔드 tasks.py
    {
        "file": "backend/app/tasks.py",
        "old": '    "free": 7,',
        "new": '    "free": 30,',
    },
    # docs 페이지
    {
        "file": "frontend/app/docs/page.tsx",
        "old": '<li>• <strong className="text-gray-800">Free:</strong> 7 days</li>',
        "new": '<li>• <strong className="text-gray-800">Free:</strong> 30 days</li>',
    },
    {
        "file": "frontend/app/docs/page.tsx",
        "old": 'The free plan includes <strong className="text-gray-800">10 monitors</strong> with 5-minute check intervals and 7-day data retention',
        "new": 'The free plan includes <strong className="text-gray-800">10 monitors</strong> with 5-minute check intervals and 30-day data retention',
    },
    # privacy 페이지
    {
        "file": "frontend/app/privacy/page.tsx",
        "old": 'Monitor check history is retained for 7 days on the Free plan',
        "new": 'Monitor check history is retained for 30 days on the Free plan',
    },
    # README
    {
        "file": "README.md",
        "old": '| **Free** | $0/mo | 10 | 5 min | 7 days | ❌ |',
        "new": '| **Free** | $0/mo | 10 | 5 min | 30 days | ❌ |',
    },
    {
        "file": "README.md",
        "old": '(Retained: 7 / 30 / 90 / 365 days by plan)',
        "new": '(Retained: 30 / 30 / 90 / 365 days by plan)',
    },
]

for change in changes:
    path = change["file"]
    if not os.path.exists(path):
        print(f"⚠️  파일 없음: {path}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if change["old"] in content:
        content = content.replace(change["old"], change["new"])
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"✅ {path}")
    else:
        print(f"❌ 못 찾음: {path} — '{change['old'][:50]}...'")

print("\n완료!")
