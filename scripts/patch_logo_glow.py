# ── ClientHeader.tsx ─────────────────────────────────────────────────────────
FILE1 = r"C:\home\jeon\api-health-monitor\frontend\components\ClientHeader.tsx"
with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    'className="h-12 w-12 rounded-xl object-contain"',
    'className="h-14 w-14 rounded-xl object-contain" style={{ filter: "drop-shadow(0 0 8px rgba(0,229,180,0.6))" }}'
)
with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)
print("ClientHeader done!", 'h-14 w-14' in c)


# ── DashboardLayout.tsx ───────────────────────────────────────────────────────
FILE2 = r"C:\home\jeon\api-health-monitor\frontend\components\DashboardLayout.tsx"
with open(FILE2, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    'className="h-12 w-12 rounded-xl object-contain"',
    'className="h-14 w-14 rounded-xl object-contain" style={{ filter: "drop-shadow(0 0 8px rgba(0,229,180,0.6))" }}'
)
with open(FILE2, 'w', encoding='utf-8') as f:
    f.write(c)
print("DashboardLayout done!", 'h-14 w-14' in c)


# ── Landing page footer ───────────────────────────────────────────────────────
FILE3 = r"C:\home\jeon\api-health-monitor\frontend\app\page.tsx"
with open(FILE3, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "<img src=\"/logo.png\" alt=\"CheckAPI\" style={{ width: '48px', height: '48px', borderRadius: '10px', objectFit: 'contain' }} />",
    "<img src=\"/logo.png\" alt=\"CheckAPI\" style={{ width: '56px', height: '56px', borderRadius: '12px', objectFit: 'contain', filter: 'drop-shadow(0 0 8px rgba(0,229,180,0.6))' }} />"
)
with open(FILE3, 'w', encoding='utf-8') as f:
    f.write(c)
print("Landing footer done!", '56px' in c)
