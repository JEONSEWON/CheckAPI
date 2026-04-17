file_path = "frontend/app/docs/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

fixes = [
    # 사이드바 링크 텍스트
    (
        'className="block text-sm text-gray-600 hover:text-green-600 py-1 transition"',
        'className="block text-sm text-gray-600 dark:text-gray-300 hover:text-green-600 py-1 transition"',
    ),
    # 사이드바 섹션 타이틀
    (
        'className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2"',
        'className="text-xs font-semibold text-gray-400 dark:text-gray-400 uppercase tracking-wider mb-2"',
    ),
    # 본문 일반 텍스트 (p 태그)
    (
        'className="mb-4 text-gray-700"',
        'className="mb-4 text-gray-700 dark:text-gray-200"',
    ),
    (
        'className="text-gray-700 leading-relaxed mb-4"',
        'className="text-gray-700 dark:text-gray-200 leading-relaxed mb-4"',
    ),
    (
        'className="text-gray-700 leading-relaxed"',
        'className="text-gray-700 dark:text-gray-200 leading-relaxed"',
    ),
    (
        'className="text-gray-700 mb-4"',
        'className="text-gray-700 dark:text-gray-200 mb-4"',
    ),
    # 테이블 셀 텍스트
    (
        'className="px-4 py-3 text-gray-700"',
        'className="px-4 py-3 text-gray-700 dark:text-gray-200"',
    ),
    # td 기본 (클래스 없는 것)
    (
        '<td className="px-4 py-3">',
        '<td className="px-4 py-3 dark:text-gray-200">',
    ),
    # 리스트 텍스트
    (
        'className="space-y-1 text-sm"',
        'className="space-y-1 text-sm dark:text-gray-200"',
    ),
    (
        'className="space-y-2 text-gray-700"',
        'className="space-y-2 text-gray-700 dark:text-gray-200"',
    ),
    # 헤딩들
    (
        'className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-3"',
        'className="text-xl font-semibold text-white mb-3"',
    ),
    (
        'className="text-3xl font-bold text-gray-900 dark:text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700"',
        'className="text-3xl font-bold text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700"',
    ),
    # code 블록 주변 텍스트
    (
        'className="text-sm text-gray-600 mb-2"',
        'className="text-sm text-gray-600 dark:text-gray-300 mb-2"',
    ),
    # 메인 배경
    (
        'className="flex-1 min-w-0 py-10 px-8 bg-white dark:bg-gray-900"',
        'className="flex-1 min-w-0 py-10 px-8 bg-white dark:bg-gray-950"',
    ),
    # 사이드바 배경
    (
        'className="w-64 flex-shrink-0 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto"',
        'className="w-64 flex-shrink-0 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-950 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto"',
    ),
]

original = content
for old, new in fixes:
    content = content.replace(old, new)

if content == original:
    print("⚠️  변경된 항목 없음 — 클래스명 확인 필요")
else:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
