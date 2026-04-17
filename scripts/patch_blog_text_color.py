files = [
    r"C:\home\jeon\api-health-monitor\frontend\app\blog\free-api-monitoring\page.tsx",
    r"C:\home\jeon\api-health-monitor\frontend\app\blog\slack-api-alerts\page.tsx",
    r"C:\home\jeon\api-health-monitor\frontend\app\blog\uptimerobot-alternatives\page.tsx",
]

replacements = [
    ('dark:text-gray-400', 'dark:text-gray-200'),
    # 혹시 아직 변환 안 된 것들
    ('text-gray-600', 'text-gray-600 dark:text-gray-200'),
    ('text-gray-500', 'text-gray-500 dark:text-gray-300'),
    ('text-gray-700', 'text-gray-700 dark:text-gray-200'),
]

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()

        for old, new in replacements:
            c = c.replace(old, new)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)

        print(f"Done: {fpath.split(chr(92))[-2]}")
    except Exception as e:
        print(f"Error: {fpath} — {e}")
