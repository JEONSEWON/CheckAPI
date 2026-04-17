FILE = r"C:\home\jeon\api-health-monitor\backend\app\main.py"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

old_line = "app.include_router(api_keys.router, prefix=\"/api/v1\")"
new_line = "app.include_router(api_keys.router, prefix=\"/api/v1\")\napp.include_router(maintenance.router)"

c = c.replace(old_line, new_line)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!", "maintenance.router" in c)
