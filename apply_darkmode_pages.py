import os

def patch(path, replacements):
    if not os.path.exists(path):
        print(f"⚠️  없음: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content == original:
        print(f"⚠️  변경 없음: {path}")
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"✅ {path}")

# ── 공통 다크모드 패턴 ──────────────────────────────────────────────────────

COMMON = [
    # 페이지 배경
    (
        'className="min-h-screen bg-gradient-to-b from-white to-gray-50"',
        'className="min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-950"',
    ),
    # 헤더
    (
        'className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50"',
        'className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 dark:bg-gray-900/80 dark:border-gray-800"',
    ),
    # 네비 링크
    (
        'className="text-gray-700 hover:text-green-600 transition"',
        'className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition"',
    ),
    # 로그인 버튼
    (
        'className="text-gray-700 hover:text-green-600 transition">Log in',
        'className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in',
    ),
    # 푸터 배경
    (
        'className="border-t bg-white"',
        'className="border-t bg-white dark:bg-gray-900 dark:border-gray-800"',
    ),
    # 푸터 헤딩
    (
        'className="font-bold text-gray-900 mb-4">CheckAPI',
        'className="font-bold text-gray-900 dark:text-white mb-4">CheckAPI',
    ),
    (
        'className="font-semibold text-gray-900 mb-4">Product',
        'className="font-semibold text-gray-900 dark:text-white mb-4">Product',
    ),
    (
        'className="font-semibold text-gray-900 mb-4">Company',
        'className="font-semibold text-gray-900 dark:text-white mb-4">Company',
    ),
    (
        'className="font-semibold text-gray-900 mb-4">Legal',
        'className="font-semibold text-gray-900 dark:text-white mb-4">Legal',
    ),
    # 푸터 링크 텍스트
    (
        'className="space-y-2 text-sm text-gray-600"',
        'className="space-y-2 text-sm text-gray-600 dark:text-gray-400"',
    ),
    # 푸터 copyright
    (
        'className="border-t mt-8 pt-8 text-center text-sm text-gray-600"',
        'className="border-t mt-8 pt-8 text-center text-sm text-gray-600 dark:text-gray-400 dark:border-gray-800"',
    ),
    # 푸터 설명 텍스트
    (
        'className="text-gray-600 text-sm">Simple, reliable API monitoring',
        'className="text-gray-600 dark:text-gray-400 text-sm">Simple, reliable API monitoring',
    ),
]

# ── About ─────────────────────────────────────────────────────────────────

ABOUT = COMMON + [
    (
        'className="text-5xl md:text-6xl font-bold text-gray-900 mb-6"',
        'className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6"',
    ),
    (
        'className="text-xl text-gray-600 max-w-3xl mx-auto"',
        'className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto"',
    ),
    (
        'className="bg-white rounded-xl border border-gray-200 p-8"',
        'className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-8"',
    ),
    (
        'className="text-3xl font-bold text-gray-900 mb-4"',
        'className="text-3xl font-bold text-gray-900 dark:text-white mb-4"',
    ),
    (
        'className="text-gray-600 leading-relaxed"',
        'className="text-gray-600 dark:text-gray-400 leading-relaxed"',
    ),
    (
        'className="text-4xl font-bold text-gray-900 mb-4"',
        'className="text-4xl font-bold text-gray-900 dark:text-white mb-4"',
    ),
    (
        'className="text-xl text-gray-600"',
        'className="text-xl text-gray-600 dark:text-gray-400"',
    ),
]

# ── Blog ─────────────────────────────────────────────────────────────────

BLOG = COMMON + [
    (
        'className="text-5xl md:text-6xl font-bold text-gray-900 mb-6"',
        'className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6"',
    ),
    (
        'className="text-xl text-gray-600 max-w-2xl mx-auto"',
        'className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto"',
    ),
    (
        'className="bg-white rounded-xl border border-gray-200 p-8 hover:border-green-300 hover:shadow-lg transition"',
        'className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-8 hover:border-green-300 hover:shadow-lg transition"',
    ),
    (
        'className="text-2xl font-bold text-gray-900 mb-3 hover:text-green-600 transition"',
        'className="text-2xl font-bold text-gray-900 dark:text-white mb-3 hover:text-green-600 transition"',
    ),
    (
        'className="text-gray-600 leading-relaxed mb-4"',
        'className="text-gray-600 dark:text-gray-400 leading-relaxed mb-4"',
    ),
    (
        'className="flex items-center gap-4 text-sm text-gray-500 mb-3"',
        'className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-3"',
    ),
]

# ── Contact ──────────────────────────────────────────────────────────────

CONTACT = COMMON + [
    (
        'className="text-5xl md:text-6xl font-bold text-gray-900 mb-6"',
        'className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6"',
    ),
    (
        'className="text-xl text-gray-600 max-w-2xl mx-auto"',
        'className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto"',
    ),
    (
        'className="bg-white p-6 rounded-xl border border-gray-200 hover:border-green-300 hover:shadow-lg transition text-center"',
        'className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-green-300 hover:shadow-lg transition text-center"',
    ),
    (
        'className="text-xl font-semibold text-gray-900 mb-2"',
        'className="text-xl font-semibold text-gray-900 dark:text-white mb-2"',
    ),
    (
        'className="text-gray-600 text-sm mb-4"',
        'className="text-gray-600 dark:text-gray-400 text-sm mb-4"',
    ),
    (
        'className="bg-white rounded-xl border border-gray-200 p-10 shadow-sm"',
        'className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-10 shadow-sm"',
    ),
    (
        'className="text-3xl font-bold text-gray-900 mb-8"',
        'className="text-3xl font-bold text-gray-900 dark:text-white mb-8"',
    ),
    (
        'className="block text-sm font-medium text-gray-700 mb-2"',
        'className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"',
    ),
    (
        'className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition text-gray-900"',
        'className="w-full px-4 py-3 border border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition text-gray-900 dark:text-white bg-white dark:bg-gray-700"',
    ),
    (
        'className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition resize-none text-gray-900"',
        'className="w-full px-4 py-3 border border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition resize-none text-gray-900 dark:text-white bg-white dark:bg-gray-700"',
    ),
    (
        'className="text-5xl mb-4">✅</div>\n              <h3 className="text-2xl font-bold text-gray-900 mb-2">Message sent!</h3>',
        'className="text-5xl mb-4">✅</div>\n              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Message sent!</h3>',
    ),
]

# ── Privacy ──────────────────────────────────────────────────────────────

PRIVACY = COMMON + [
    (
        'className="bg-white rounded-xl border border-gray-200 p-10 shadow-sm space-y-10 text-gray-600 leading-relaxed"',
        'className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-10 shadow-sm space-y-10 text-gray-600 dark:text-gray-400 leading-relaxed"',
    ),
    (
        'className="text-2xl font-bold text-gray-900 mb-4"',
        'className="text-2xl font-bold text-gray-900 dark:text-white mb-4"',
    ),
    (
        'className="text-5xl font-bold text-gray-900 mb-4"',
        'className="text-5xl font-bold text-gray-900 dark:text-white mb-4"',
    ),
    (
        'className="text-gray-500">Last updated',
        'className="text-gray-500 dark:text-gray-400">Last updated',
    ),
]

# ── Terms ─────────────────────────────────────────────────────────────────

TERMS = COMMON + [
    (
        'className="bg-white rounded-xl border border-gray-200 p-10 shadow-sm space-y-10 text-gray-600 leading-relaxed"',
        'className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-10 shadow-sm space-y-10 text-gray-600 dark:text-gray-400 leading-relaxed"',
    ),
    (
        'className="text-2xl font-bold text-gray-900 mb-4"',
        'className="text-2xl font-bold text-gray-900 dark:text-white mb-4"',
    ),
    (
        'className="text-5xl font-bold text-gray-900 mb-4"',
        'className="text-5xl font-bold text-gray-900 dark:text-white mb-4"',
    ),
    (
        'className="text-gray-500">Last updated',
        'className="text-gray-500 dark:text-gray-400">Last updated',
    ),
]

# ── Docs ──────────────────────────────────────────────────────────────────

DOCS = COMMON + [
    # 사이드바
    (
        'className="w-64 flex-shrink-0 border-r border-gray-200 bg-white sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto"',
        'className="w-64 flex-shrink-0 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto"',
    ),
    (
        'className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2"',
        'className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2"',
    ),
    # 메인 콘텐츠 배경
    (
        'className="flex-1 min-w-0 py-10 px-8"',
        'className="flex-1 min-w-0 py-10 px-8 bg-white dark:bg-gray-900"',
    ),
    # 섹션 헤딩
    (
        'className="text-3xl font-bold text-gray-900 mb-8 pb-3 border-b border-gray-200"',
        'className="text-3xl font-bold text-gray-900 dark:text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700"',
    ),
    (
        'className="text-xl font-semibold text-gray-800 mb-3"',
        'className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-3"',
    ),
    # 일반 텍스트
    (
        'className="text-gray-700 leading-relaxed mb-4"',
        'className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4"',
    ),
    (
        'className="text-gray-700 leading-relaxed"',
        'className="text-gray-700 dark:text-gray-300 leading-relaxed"',
    ),
    # 테이블
    (
        'className="w-full text-sm border border-gray-200 rounded-xl overflow-hidden"',
        'className="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden"',
    ),
    (
        'className="bg-gray-50"',
        'className="bg-gray-50 dark:bg-gray-800"',
    ),
    (
        'className="text-left px-4 py-3 font-semibold text-gray-700"',
        'className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300"',
    ),
    (
        'className="divide-y divide-gray-100"',
        'className="divide-y divide-gray-100 dark:divide-gray-700"',
    ),
    # 강조 텍스트
    (
        'className="text-gray-800"',
        'className="text-gray-800 dark:text-gray-200"',
    ),
    # 지원 섹션
    (
        'className="bg-green-50 rounded-2xl border border-green-100 p-8 text-center"',
        'className="bg-green-50 dark:bg-green-950 rounded-2xl border border-green-100 dark:border-green-900 p-8 text-center"',
    ),
    (
        'className="text-2xl font-bold text-gray-900 mb-2"',
        'className="text-2xl font-bold text-gray-900 dark:text-white mb-2"',
    ),
    (
        'className="text-gray-600 mb-5"',
        'className="text-gray-600 dark:text-gray-400 mb-5"',
    ),
    # docs content: free plan history 7 → 30
    (
        '5-minute check intervals and 7-day data retention',
        '5-minute check intervals and 30-day data retention',
    ),
    (
        '<li>• <strong className="text-gray-800 dark:text-gray-200">Free:</strong> 7 days</li>',
        '<li>• <strong className="text-gray-800 dark:text-gray-200">Free:</strong> 30 days</li>',
    ),
    # docs content: Axiom Technologies 추가
    (
        '<p className="text-gray-600 dark:text-gray-400 text-sm">Simple, reliable API monitoring for developers and teams.</p>',
        '<p className="text-gray-600 dark:text-gray-400 text-sm">Simple, reliable API monitoring for developers and teams. Built by <a href="https://axiom.so" className="hover:text-green-600">Axiom Technologies</a>.</p>',
    ),
]

# ── Settings (free plan 7 → 30) ───────────────────────────────────────────

SETTINGS = [
    (
        "'7-day history',",
        "'30-day history',",
    ),
]

# ── 실행 ─────────────────────────────────────────────────────────────────

patch("frontend/app/about/page.tsx", ABOUT)
patch("frontend/app/blog/page.tsx", BLOG)
patch("frontend/app/blog/uptimerobot-alternatives/page.tsx", BLOG)
patch("frontend/app/contact/page.tsx", CONTACT)
patch("frontend/app/privacy/page.tsx", PRIVACY)
patch("frontend/app/terms/page.tsx", TERMS)
patch("frontend/app/docs/page.tsx", DOCS)
patch("frontend/app/dashboard/settings/page.tsx", SETTINGS)

print("\n전체 완료!")
