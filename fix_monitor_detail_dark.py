file_path = "frontend/app/dashboard/monitors/[id]/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

fixes = [
    # 헤더 back 버튼
    (
        'className="p-2 hover:bg-gray-100 rounded-lg transition"',
        'className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"',
    ),
    # 모니터 이름
    (
        'className="text-2xl font-bold text-gray-900"',
        'className="text-2xl font-bold text-gray-900 dark:text-white"',
    ),
    # URL 텍스트
    (
        'className="text-sm text-gray-500 mt-1"',
        'className="text-sm text-gray-500 dark:text-gray-400 mt-1"',
    ),
    # Pause 버튼
    (
        'className="flex items-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition text-gray-900"',
        'className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-900 dark:text-white"',
    ),
    # StatCard
    (
        'className="bg-white rounded-lg border border-gray-200 p-4"',
        'className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4"',
    ),
    (
        'className="text-sm font-medium text-gray-600">{title}',
        'className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}',
    ),
    (
        'className="text-2xl font-bold text-gray-900">{value}',
        'className="text-2xl font-bold text-gray-900 dark:text-white">{value}',
    ),
    # Configuration 카드
    (
        'className="bg-white rounded-lg border border-gray-200 shadow-sm"',
        'className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm"',
    ),
    (
        'className="px-6 py-4 border-b border-gray-200"',
        'className="px-6 py-4 border-b border-gray-200 dark:border-gray-700"',
    ),
    (
        'className="text-lg font-semibold text-gray-900">Configuration',
        'className="text-lg font-semibold text-gray-900 dark:text-white">Configuration',
    ),
    (
        'className="text-lg font-semibold text-gray-900">Recent Checks',
        'className="text-lg font-semibold text-gray-900 dark:text-white">Recent Checks',
    ),
    # ConfigItem
    (
        'className="text-sm text-gray-500 mb-1">{label}',
        'className="text-sm text-gray-500 dark:text-gray-400 mb-1">{label}',
    ),
    (
        'className="font-medium text-gray-900">{value}',
        'className="font-medium text-gray-900 dark:text-white">{value}',
    ),
    # CheckRow
    (
        'className="px-6 py-3 flex items-center justify-between hover:bg-gray-50"',
        'className="px-6 py-3 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700"',
    ),
    (
        'className="divide-y divide-gray-200"',
        'className="divide-y divide-gray-200 dark:divide-gray-700"',
    ),
    (
        'className="text-gray-500 text-sm">Status:',
        'className="text-gray-500 dark:text-gray-400 text-sm">Status:',
    ),
    (
        'className="text-gray-500 text-sm">{check.response_time}',
        'className="text-gray-500 dark:text-gray-400 text-sm">{check.response_time}',
    ),
    (
        'className="text-sm text-gray-500">\n        {formatDistanceToNow',
        'className="text-sm text-gray-500 dark:text-gray-400">\n        {formatDistanceToNow',
    ),
    # No checks yet
    (
        'className="px-6 py-12 text-center text-gray-500"',
        'className="px-6 py-12 text-center text-gray-500 dark:text-gray-400"',
    ),
    # Status badge 색상 (dark mode 대응)
    (
        "up: { bg: 'bg-green-100', text: 'text-green-800', icon: CheckCircle },",
        "up: { bg: 'bg-green-100 dark:bg-green-900', text: 'text-green-800 dark:text-green-300', icon: CheckCircle },",
    ),
    (
        "down: { bg: 'bg-red-100', text: 'text-red-800', icon: AlertCircle },",
        "down: { bg: 'bg-red-100 dark:bg-red-900', text: 'text-red-800 dark:text-red-300', icon: AlertCircle },",
    ),
    (
        "degraded: { bg: 'bg-yellow-100', text: 'text-yellow-800', icon: AlertCircle },",
        "degraded: { bg: 'bg-yellow-100 dark:bg-yellow-900', text: 'text-yellow-800 dark:text-yellow-300', icon: AlertCircle },",
    ),
]

original = content
for old, new in fixes:
    content = content.replace(old, new)

if content == original:
    print("⚠️  변경된 항목 없음")
else:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
