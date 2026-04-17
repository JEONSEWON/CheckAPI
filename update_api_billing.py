file_path = "frontend/lib/api.ts"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = """  checkout: (plan: string) =>
    apiRequest(`/api/v1/subscription/checkout?plan=${plan}`, {
      method: 'POST',
    }),"""

new = """  checkout: (plan: string, billing: string = 'monthly') =>
    apiRequest(`/api/v1/subscription/checkout?plan=${plan}&billing=${billing}`, {
      method: 'POST',
    }),"""

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ api.ts 완료!")
else:
    print("❌ 못 찾음")
