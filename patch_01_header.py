import os

path = r"C:\home\jeon\api-health-monitor\frontend\components\ClientHeader.tsx"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '<Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Docs</Link>'
new = '''<Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Docs</Link>
            <Link href="/blog" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Blog</Link>'''

if old not in content:
    print("ERROR: target string not found. Check file manually.")
else:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ ClientHeader.tsx patched — Blog link added to nav")
