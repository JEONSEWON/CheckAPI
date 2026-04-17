import os
import re

# ClientHeader.tsx
FILE1 = r"C:\home\jeon\api-health-monitor\frontend\components\ClientHeader.tsx"
with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('href="#pricing"', 'href="/pricing"')
c = c.replace('href="/#pricing"', 'href="/pricing"')
with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)
print("ClientHeader done!")

# 나머지 파일들 - frontend/app 하위 전체
base = r"C:\home\jeon\api-health-monitor\frontend\app"

skip_dirs = ['[id]', 'status']

for root, dirs, files in os.walk(base):
    # [id] 폴더 스킵
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for fname in files:
        if not fname.endswith('.tsx'):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                c = f.read()
            new_c = c.replace('href="/#pricing"', 'href="/pricing"').replace('href="#pricing"', 'href="/pricing"')
            if new_c != c:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_c)
                print(f"Updated: {fpath.split('frontend')[1]}")
        except Exception as e:
            print(f"Skipped: {fpath} ({e})")

print("\nAll done!")
