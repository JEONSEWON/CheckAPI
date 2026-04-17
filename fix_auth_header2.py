import os

PUBLIC_PAGES = [
    "frontend/app/about/page.tsx",
    "frontend/app/blog/page.tsx",
    "frontend/app/blog/uptimerobot-alternatives/page.tsx",
    "frontend/app/blog/free-api-monitoring/page.tsx",
    "frontend/app/contact/page.tsx",
    "frontend/app/privacy/page.tsx",
    "frontend/app/terms/page.tsx",
    "frontend/app/docs/page.tsx",
    "frontend/app/page.tsx",
]

AUTH_COMPONENT = '''
function AuthButtons() {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  React.useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
  }, []);

  if (isLoggedIn) {
    return (
      <a href="/dashboard" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium">
        Dashboard →
      </a>
    );
  }

  return (
    <div className="flex items-center space-x-4">
      <a href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in</a>
      <a href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium">Get Started</a>
    </div>
  );
}
'''

for path in PUBLIC_PAGES:
    if not os.path.exists(path):
        print(f"⚠️  없음: {path}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # React import 추가
    if "'use client'" in content and "import React" not in content:
        content = content.replace("'use client';", "'use client';\nimport React from 'react';")

    # Log in 링크가 포함된 div 블록 찾아서 <AuthButtons />로 교체
    # 다양한 패턴 시도
    patterns = [
        # about, blog 등 (Link 사용)
        '<Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in</Link>\n              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">Get Started</Link>',
        # landing page (Link + 줄바꿈)
        '<Link href="/login" className="text-gray-700 hover:text-green-600 transition">Log in</Link>\n              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium">\n                Get Started\n              </Link>',
        # dark 없는 버전
        '<Link href="/login" className="text-gray-700 hover:text-green-600 transition">Log in</Link>\n              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">Get Started</Link>',
    ]

    replaced = False
    for p in patterns:
        if p in content:
            content = content.replace(p, '<AuthButtons />')
            replaced = True
            break

    # AuthButtons 컴포넌트 추가
    if replaced and "function AuthButtons" not in content:
        content = content.rstrip() + "\n" + AUTH_COMPONENT

    if content == original:
        # 못 찾으면 실제 패턴 출력
        idx = content.find('Log in')
        if idx != -1:
            print(f"❌ 패턴 못 찾음 [{path}]: {repr(content[idx-50:idx+150])}")
        else:
            print(f"⚠️  Log in 없음: {path}")
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"✅ {path}")

print("\n완료!")
