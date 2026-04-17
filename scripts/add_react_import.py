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

    # React import 없으면 첫 줄 뒤에 추가
    if "import React from 'react'" not in content:
        first_import_idx = content.find('import ')
        if first_import_idx != -1:
            content = content[:first_import_idx] + "import React from 'react';\n" + content[first_import_idx:]

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('fixed:', path)

print('완료!')
