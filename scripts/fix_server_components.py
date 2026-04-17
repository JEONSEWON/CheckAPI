import os

files = [
    'frontend/app/about/page.tsx',
    'frontend/app/blog/page.tsx',
    'frontend/app/blog/uptimerobot-alternatives/page.tsx',
    'frontend/app/blog/free-api-monitoring/page.tsx',
    'frontend/app/privacy/page.tsx',
    'frontend/app/terms/page.tsx',
]

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # AuthButtons 함수 전체 제거
    if 'function AuthButtons' in content:
        idx = content.find('\nfunction AuthButtons')
        content = content[:idx]

    # React import 제거
    content = content.replace("'use client';\nimport React from 'react';\n", '')
    content = content.replace("import React from 'react';\n", '')
    content = content.replace("'use client';\n", '')

    # AuthButtons 태그를 원래 버튼으로 교체
    old = '<AuthButtons />'
    new = '<Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in</Link>\n              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">\n                Get Started\n              </Link>'
    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('fixed:', path)

print('완료!')
