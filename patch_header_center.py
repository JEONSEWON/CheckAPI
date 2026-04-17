FILE = r"C:\home\jeon\api-health-monitor\frontend\components\ClientHeader.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

old_header = """        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <img src="/logo.png" alt="CheckAPI" className="h-14 w-14 rounded-xl object-contain" style={{ filter: "drop-shadow(0 0 8px rgba(0,229,180,0.6))" }} />
          </div>
          <nav className="hidden md:flex space-x-8">
            <a href="#features" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Features</a>
            <a href="#pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Pricing</a>
            <Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Docs</Link>
          </nav>
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            <AuthButtons />
          </div>
        </div>"""

new_header = """        <div className="relative flex justify-between items-center h-16">
          <div className="flex items-center">
            <img src="/logo.png" alt="CheckAPI" className="h-14 w-14 rounded-xl object-contain" style={{ filter: "drop-shadow(0 0 8px rgba(0,229,180,0.6))" }} />
          </div>
          <nav className="hidden md:flex space-x-8 absolute left-1/2 -translate-x-1/2">
            <a href="#features" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Features</a>
            <a href="#pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Pricing</a>
            <Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Docs</Link>
          </nav>
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            <AuthButtons />
          </div>
        </div>"""

c = c.replace(old_header, new_header)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!", "left-1/2 -translate-x-1/2" in c)
