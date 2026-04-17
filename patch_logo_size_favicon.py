import shutil, os

# ── 1. 로고 크기 키우기 ───────────────────────────────────────────────────────

# ClientHeader.tsx - h-9 w-9 → h-12 w-12, object-cover → object-contain
FILE1 = r"C:\home\jeon\api-health-monitor\frontend\components\ClientHeader.tsx"
with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('className="h-9 w-9 rounded-lg object-cover"', 'className="h-12 w-12 rounded-xl object-contain"')
with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)
print("ClientHeader done!", 'h-12 w-12' in c)

# DashboardLayout.tsx - h-10 w-10 → h-12 w-12, object-cover → object-contain
FILE2 = r"C:\home\jeon\api-health-monitor\frontend\components\DashboardLayout.tsx"
with open(FILE2, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('className="h-10 w-10 rounded-lg object-cover"', 'className="h-12 w-12 rounded-xl object-contain"')
with open(FILE2, 'w', encoding='utf-8') as f:
    f.write(c)
print("DashboardLayout done!", 'h-12 w-12' in c)

# Landing page footer - 32x32 → 48x48, object-contain
FILE3 = r"C:\home\jeon\api-health-monitor\frontend\app\page.tsx"
with open(FILE3, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace(
    "<img src=\"/logo.png\" alt=\"CheckAPI\" style={{ width: '32px', height: '32px', borderRadius: '8px' }} />",
    "<img src=\"/logo.png\" alt=\"CheckAPI\" style={{ width: '48px', height: '48px', borderRadius: '10px', objectFit: 'contain' }} />"
)
with open(FILE3, 'w', encoding='utf-8') as f:
    f.write(c)
print("Landing footer done!", '48px' in c)

# ── 2. favicon 교체 ───────────────────────────────────────────────────────────
# logo.png를 favicon 파일들로 복사 (Python pillow로 리사이즈)
try:
    from PIL import Image
    src = r"C:\home\jeon\api-health-monitor\frontend\public\logo.png"
    img = Image.open(src).convert("RGBA")

    sizes = {
        'favicon-16x16.png': 16,
        'favicon-32x32.png': 32,
        'favicon-96x96.png': 96,
        'android-chrome-192x192.png': 192,
        'android-chrome-512x512.png': 512,
        'apple-touch-icon.png': 180,
    }

    pub = r"C:\home\jeon\api-health-monitor\frontend\public"
    for fname, size in sizes.items():
        resized = img.resize((size, size), Image.LANCZOS)
        resized.save(os.path.join(pub, fname))
        print(f"  {fname} ({size}x{size}) saved")

    # favicon.ico (16, 32, 48 멀티사이즈)
    ico_images = [img.resize((s, s), Image.LANCZOS) for s in [16, 32, 48]]
    ico_images[0].save(
        os.path.join(pub, 'favicon.ico'),
        format='ICO',
        sizes=[(16,16),(32,32),(48,48)]
    )
    print("  favicon.ico saved")
    print("Favicon done!")

except ImportError:
    print("Pillow not installed, installing...")
    import subprocess
    subprocess.run(['pip', 'install', 'Pillow', '--break-system-packages', '-q'])
    from PIL import Image
    src = r"C:\home\jeon\api-health-monitor\frontend\public\logo.png"
    img = Image.open(src).convert("RGBA")
    sizes = {
        'favicon-16x16.png': 16,
        'favicon-32x32.png': 32,
        'favicon-96x96.png': 96,
        'android-chrome-192x192.png': 192,
        'android-chrome-512x512.png': 512,
        'apple-touch-icon.png': 180,
    }
    pub = r"C:\home\jeon\api-health-monitor\frontend\public"
    for fname, size in sizes.items():
        resized = img.resize((size, size), Image.LANCZOS)
        resized.save(os.path.join(pub, fname))
        print(f"  {fname} saved")
    ico_images = [img.resize((s, s), Image.LANCZOS) for s in [16, 32, 48]]
    ico_images[0].save(os.path.join(pub, 'favicon.ico'), format='ICO', sizes=[(16,16),(32,32),(48,48)])
    print("Favicon done!")
