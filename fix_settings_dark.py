file_path = "frontend/app/dashboard/settings/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

fixes = [
    # 페이지 헤더
    (
        'className="text-3xl font-bold text-gray-900">Settings',
        'className="text-3xl font-bold text-gray-900 dark:text-white">Settings',
    ),
    (
        'className="text-gray-600 mt-1">Manage your account and subscription',
        'className="text-gray-600 dark:text-gray-400 mt-1">Manage your account and subscription',
    ),
    # Current Plan 카드
    (
        'className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">\n          <h2 className="text-lg font-semibold text-gray-900 mb-4">Current Plan',
        'className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">\n          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Current Plan',
    ),
    (
        'className="text-2xl font-bold text-gray-900 capitalize"',
        'className="text-2xl font-bold text-gray-900 dark:text-white capitalize"',
    ),
    (
        'className="text-sm text-gray-500 mt-1">\n                  Status:',
        'className="text-sm text-gray-500 dark:text-gray-400 mt-1">\n                  Status:',
    ),
    # Upgrade Your Plan 헤딩
    (
        'className="text-xl font-semibold text-gray-900 mb-4">Upgrade Your Plan',
        'className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Upgrade Your Plan',
    ),
    # Account Info 카드
    (
        'className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">\n          <h2 className="text-lg font-semibold text-gray-900 mb-4">Account Information',
        'className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">\n          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Account Information',
    ),
    # PlanCard 컴포넌트
    (
        "bg-white rounded-lg border-2 p-6\n        ${plan.popular ? 'border-green-600 shadow-lg' : 'border-gray-200'}",
        "bg-white dark:bg-gray-800 rounded-lg border-2 p-6\n        ${plan.popular ? 'border-green-600 shadow-lg' : 'border-gray-200 dark:border-gray-700'}",
    ),
    (
        'className="text-2xl font-bold text-gray-900 mt-4">{plan.name}',
        'className="text-2xl font-bold text-gray-900 dark:text-white mt-4">{plan.name}',
    ),
    (
        'className="text-4xl font-bold text-gray-900">{plan.price}',
        'className="text-4xl font-bold text-gray-900 dark:text-white">{plan.price}',
    ),
    (
        'className="text-gray-600">/month',
        'className="text-gray-600 dark:text-gray-400">/month',
    ),
    (
        'className="flex items-center text-gray-700"',
        'className="flex items-center text-gray-700 dark:text-gray-300"',
    ),
    (
        'className="w-full py-2 border-2 border-gray-300 text-gray-500 rounded-lg font-medium"',
        'className="w-full py-2 border-2 border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 rounded-lg font-medium"',
    ),
    (
        "'border-2 border-green-600 text-green-600 hover:bg-green-50'",
        "'border-2 border-green-600 text-green-600 hover:bg-green-50 dark:hover:bg-green-900'",
    ),
    # InfoRow 컴포넌트
    (
        'className="flex justify-between py-2"',
        'className="flex justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-0"',
    ),
    (
        'className="text-gray-600">{label}',
        'className="text-gray-600 dark:text-gray-400">{label}',
    ),
    (
        'className="font-medium text-gray-900">{value}',
        'className="font-medium text-gray-900 dark:text-white">{value}',
    ),
    # Free plan history fix
    (
        "'7-day history',",
        "'30-day history',",
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
