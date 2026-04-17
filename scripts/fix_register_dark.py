file_path = "frontend/app/register/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

fixes = [
    # 배경
    (
        'className="min-h-screen bg-gradient-to-b from-white to-gray-50 flex items-center justify-center px-4"',
        'className="min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-950 flex items-center justify-center px-4"',
    ),
    # 로고 텍스트 (API Health Monitor → CheckAPI)
    (
        'API Health Monitor',
        'CheckAPI',
    ),
    # 카드 배경
    (
        'className="bg-white rounded-xl shadow-lg border border-gray-200 p-8"',
        'className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-8"',
    ),
    # 헤딩
    (
        'className="mt-4 text-2xl font-bold text-gray-900"',
        'className="mt-4 text-2xl font-bold text-gray-900 dark:text-white"',
    ),
    (
        'className="mt-2 text-gray-600"',
        'className="mt-2 text-gray-600 dark:text-gray-400"',
    ),
    # 라벨
    (
        'className="block text-sm font-medium text-gray-700 mb-2"',
        'className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"',
    ),
    # 인풋
    (
        'className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900"',
        'className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"',
    ),
    # 힌트 텍스트
    (
        'className="mt-1 text-xs text-gray-500"',
        'className="mt-1 text-xs text-gray-500 dark:text-gray-400"',
    ),
    # 하단 링크
    (
        'className="text-sm text-gray-600"',
        'className="text-sm text-gray-600 dark:text-gray-400"',
    ),
    # 약관 텍스트
    (
        'className="mt-6 text-xs text-center text-gray-500"',
        'className="mt-6 text-xs text-center text-gray-500 dark:text-gray-400"',
    ),
]

original = content
count = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        count += 1

if content == original:
    print("⚠️  변경 없음")
else:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ 완료! ({count}개 수정)")
