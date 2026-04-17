import os

PUBLIC_PAGES = [
    "frontend/app/about/page.tsx",
    "frontend/app/blog/page.tsx",
    "frontend/app/blog/uptimerobot-alternatives/page.tsx",
    "frontend/app/privacy/page.tsx",
    "frontend/app/terms/page.tsx",
    "frontend/app/docs/page.tsx",
]

FREE_API_BLOG = "frontend/app/blog/free-api-monitoring/page.tsx"

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

def process(path, old, new):
    if not os.path.exists(path):
        print(f"⚠️  없음: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    # React import 추가
    if "'use client'" in content and "import React" not in content:
        content = content.replace("'use client';", "'use client';\nimport React from 'react';")
    if old in content:
        content = content.replace(old, new)
        if "function AuthButtons" not in content:
            content = content.rstrip() + "\n" + AUTH_COMPONENT
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"✅ {path}")
    else:
        print(f"❌ 못 찾음: {path}")

# about, blog, privacy, terms, docs — dark:text-gray-300 버전 + Get Started 줄바꿈
OLD_DARK = 'Log in</Link>\n              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">\n                Get Started\n              </Link>'
NEW_BTN = '<AuthButtons />'

for path in PUBLIC_PAGES:
    process(path, OLD_DARK, NEW_BTN)

# free-api-monitoring — dark 없는 버전
OLD_FREE = 'Log in</Link>\n              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">\n                Get Started\n              </Link>'
process(FREE_API_BLOG, OLD_FREE, NEW_BTN)

# contact — 이미 <a> 태그로 변환된 상태
CONTACT = "frontend/app/contact/page.tsx"
if os.path.exists(CONTACT):
    with open(CONTACT, "r", encoding="utf-8") as f:
        content = f.read()
    # 이미 AuthButtons 있는지 확인
    if "function AuthButtons" in content:
        print(f"✅ contact 이미 처리됨")
    else:
        print(f"⚠️  contact 수동 확인 필요")

# 랜딩 페이지 — Log in 없으면 이미 다른 구조
LANDING = "frontend/app/page.tsx"
if os.path.exists(LANDING):
    with open(LANDING, "r", encoding="utf-8") as f:
        content = f.read()
    idx = content.find("Log in")
    if idx == -1:
        # ClientHeader 컴포넌트 사용 중이거나 다른 구조
        print(f"⚠️  랜딩 Log in 없음 — 현재 헤더 구조:")
        # 헤더 영역 찾기
        hidx = content.find("header")
        if hidx != -1:
            print(repr(content[hidx:hidx+500]))
    else:
        print(f"랜딩 Log in 위치: {repr(content[idx-100:idx+200])}")

print("\n완료!")
