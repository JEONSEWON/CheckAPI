import os

# 랜딩 페이지는 Server Component라 따로 처리
# 공개 페이지들은 Client Component이므로 useEffect로 토큰 체크 가능

# 1. 공개 페이지들 (Client Component) — 헤더 버튼 부분 교체
PUBLIC_PAGES = [
    "frontend/app/about/page.tsx",
    "frontend/app/blog/page.tsx",
    "frontend/app/blog/uptimerobot-alternatives/page.tsx",
    "frontend/app/blog/free-api-monitoring/page.tsx",
    "frontend/app/contact/page.tsx",
    "frontend/app/privacy/page.tsx",
    "frontend/app/terms/page.tsx",
    "frontend/app/docs/page.tsx",
]

OLD_HEADER_BUTTONS = '''            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in</Link>
              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">Get Started</Link>
            </div>'''

OLD_HEADER_BUTTONS_NODARK = '''            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-700 hover:text-green-600 transition">Log in</Link>
              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">Get Started</Link>
            </div>'''

NEW_HEADER_BUTTONS = '''            <AuthButtons />'''

# AuthButtons 컴포넌트 추가 (파일 끝에 삽입)
AUTH_BUTTONS_COMPONENT = '''
function AuthButtons() {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  React.useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
  }, []);

  if (isLoggedIn) {
    return (
      <a href="/dashboard" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">
        Dashboard
      </a>
    );
  }

  return (
    <div className="flex items-center space-x-4">
      <a href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in</a>
      <a href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">Get Started</a>
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

    # React import 확인 및 추가
    if "'use client'" in content and "import React" not in content:
        content = content.replace("'use client';", "'use client';\nimport React from 'react';")

    # 헤더 버튼 교체 (dark 버전)
    if OLD_HEADER_BUTTONS in content:
        content = content.replace(OLD_HEADER_BUTTONS, NEW_HEADER_BUTTONS)
    elif OLD_HEADER_BUTTONS_NODARK in content:
        content = content.replace(OLD_HEADER_BUTTONS_NODARK, NEW_HEADER_BUTTONS)

    # AuthButtons 컴포넌트가 없으면 파일 끝에 추가
    if "function AuthButtons" not in content and NEW_HEADER_BUTTONS in content:
        content = content.rstrip() + "\n" + AUTH_BUTTONS_COMPONENT

    if content == original:
        print(f"⚠️  변경 없음: {path}")
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"✅ {path}")

# 2. 랜딩 페이지 (page.tsx) — ClientHeader 컴포넌트 분리 필요
# 랜딩 페이지는 'use client' 추가해서 처리
landing = "frontend/app/page.tsx"
if os.path.exists(landing):
    with open(landing, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 'use client' 없으면 추가
    if "'use client'" not in content:
        content = "'use client';\nimport React from 'react';\n" + content
    elif "import React" not in content:
        content = content.replace("'use client';", "'use client';\nimport React from 'react';")

    # 랜딩 헤더 버튼 교체
    old_landing = '''              <Link href="/login" className="text-gray-700 hover:text-green-600 transition">Log in</Link>
              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium">
                Get Started
              </Link>'''

    new_landing = '''              <AuthHeaderButtons />'''

    auth_landing_component = '''
function AuthHeaderButtons() {
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
    <>
      <a href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in</a>
      <a href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium">
        Get Started
      </a>
    </>
  );
}
'''

    if old_landing in content:
        content = content.replace(old_landing, new_landing)
        if "function AuthHeaderButtons" not in content:
            content = content.rstrip() + "\n" + auth_landing_component
        with open(landing, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"✅ {landing}")
    else:
        print(f"⚠️  랜딩 페이지 헤더 버튼 패턴 못 찾음: {landing}")

print("\n전체 완료!")
