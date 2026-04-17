import os

files = [
    'frontend/app/about/page.tsx',
    'frontend/app/blog/page.tsx',
    'frontend/app/blog/uptimerobot-alternatives/page.tsx',
    'frontend/app/blog/free-api-monitoring/page.tsx',
    'frontend/app/privacy/page.tsx',
    'frontend/app/terms/page.tsx',
    'frontend/app/docs/page.tsx',
]

for path in files:
    if not os.path.exists(path):
        print(f"⚠️  없음: {path}")
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. PublicAuthButtons import 추가 (첫 번째 import 앞에)
    if "PublicAuthButtons" not in content:
        first_import = content.find("import ")
        content = content[:first_import] + "import PublicAuthButtons from '@/components/PublicAuthButtons';\n" + content[first_import:]

    # 2. 헤더 버튼 교체 - Get Started 줄바꿈 버전
    old = '<Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in</Link>\n              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">\n                Get Started\n              </Link>'
    new = '<PublicAuthButtons />'

    # dark 없는 버전
    old2 = '<Link href="/login" className="text-gray-700 hover:text-green-600 transition">Log in</Link>\n              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">\n                Get Started\n              </Link>'

    if old in content:
        content = content.replace(old, new)
    elif old2 in content:
        content = content.replace(old2, new)
    else:
        print(f"⚠️  버튼 패턴 못 찾음: {path}")

    if content == original:
        print(f"⚠️  변경 없음: {path}")
    else:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"✅ {path}")

print("\n완료!")
