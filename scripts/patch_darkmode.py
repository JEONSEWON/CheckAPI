import re

# ── 1. CreateAlertChannelModal 다크모드 ──────────────────────────────────────
FILE1 = r"C:\home\jeon\api-health-monitor\frontend\components\CreateAlertChannelModal.tsx"

with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()

replacements_modal = [
    # 모달 컨테이너
    ('relative bg-white rounded-lg shadow-xl max-w-md w-full',
     'relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full'),
    # 헤더
    ('flex items-center justify-between px-6 py-4 border-b border-gray-200',
     'flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700'),
    ('text-xl font-semibold text-gray-900',
     'text-xl font-semibold text-gray-900 dark:text-white'),
    ('p-2 hover:bg-gray-100 rounded-lg text-gray-700',
     'p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg text-gray-700 dark:text-gray-300'),
    # 라벨들
    ('block text-sm font-medium text-gray-700 mb-2',
     'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2'),
    # select
    ('w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 bg-white',
     'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700'),
    # input들 (여러 개 동일 클래스)
    ('w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900',
     'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white dark:bg-gray-700'),
    # hint 텍스트
    ('text-xs text-gray-500 mt-1',
     'text-xs text-gray-500 dark:text-gray-400 mt-1'),
    # Cancel 버튼
    ('px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition text-gray-900',
     'px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-900 dark:text-white'),
]

for old, new in replacements_modal:
    c = c.replace(old, new)

with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)

print("CreateAlertChannelModal done!")
print("dark:bg-gray-800:", "dark:bg-gray-800" in c)
print("dark:bg-gray-700 input:", "dark:bg-gray-700" in c)


# ── 2. 블로그 다크모드 (free-api-monitoring) ─────────────────────────────────
FILE2 = r"C:\home\jeon\api-health-monitor\frontend\app\blog\free-api-monitoring\page.tsx"

with open(FILE2, 'r', encoding='utf-8') as f:
    c2 = f.read()

blog_replacements = [
    ('min-h-screen bg-gradient-to-b from-white to-gray-50',
     'min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-950 dark:to-gray-900'),
    ('border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50',
     'border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm sticky top-0 z-50'),
    ('"text-gray-700 hover:text-green-600 transition"',
     '"text-gray-700 dark:text-gray-300 hover:text-green-600 transition"'),
    ('text-gray-600', 'text-gray-600 dark:text-gray-400'),
    ('text-gray-500', 'text-gray-500 dark:text-gray-400'),
    ('text-gray-900', 'text-gray-900 dark:text-white'),
    ('bg-white rounded', 'bg-white dark:bg-gray-800 rounded'),
    ('bg-gray-50', 'bg-gray-50 dark:bg-gray-900'),
    ('border-gray-200', 'border-gray-200 dark:border-gray-700'),
    ('bg-green-50', 'bg-green-50 dark:bg-green-950'),
]

for old, new in blog_replacements:
    c2 = c2.replace(old, new)

with open(FILE2, 'w', encoding='utf-8') as f:
    f.write(c2)

print("\nfree-api-monitoring blog done!")
print("dark:from-gray-950:", "dark:from-gray-950" in c2)


# ── 3. 블로그 다크모드 (slack-api-alerts) ────────────────────────────────────
FILE3 = r"C:\home\jeon\api-health-monitor\frontend\app\blog\slack-api-alerts\page.tsx"

with open(FILE3, 'r', encoding='utf-8') as f:
    c3 = f.read()

for old, new in blog_replacements:
    c3 = c3.replace(old, new)

with open(FILE3, 'w', encoding='utf-8') as f:
    f.write(c3)

print("\nslack-api-alerts blog done!")
print("dark:from-gray-950:", "dark:from-gray-950" in c3)
