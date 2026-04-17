file_path = "frontend/app/dashboard/settings/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = "  useEffect(() => { loadSubscription(); }, []);"
new = """  useEffect(() => {
    loadSubscription();
  }, []);

  useEffect(() => {
    if (user?.plan === 'business') loadApiKeys();
  }, [user?.plan]);"""

content = content.replace(old, new)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("done")
