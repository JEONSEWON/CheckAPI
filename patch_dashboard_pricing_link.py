FILE = r"C:\home\jeon\api-health-monitor\frontend\components\DashboardLayout.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

old_header = """            <div className="flex-1 flex justify-end items-center gap-4">
              {user?.plan === 'free' && (
                <Link href="/dashboard/settings" className="text-sm text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">
                  Upgrade to Pro →
                </Link>
              )}
              <ThemeToggle />
            </div>"""

new_header = """            <div className="flex-1 flex justify-end items-center gap-4">
              <Link href="/pricing" className="text-sm text-gray-600 dark:text-gray-400 hover:text-green-600 dark:hover:text-green-400 transition">
                Pricing
              </Link>
              {user?.plan === 'free' && (
                <Link href="/dashboard/settings" className="text-sm font-medium text-green-600 dark:text-green-400 hover:text-green-700 transition">
                  Upgrade →
                </Link>
              )}
              <ThemeToggle />
            </div>"""

c = c.replace(old_header, new_header)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!", "/pricing" in c)
