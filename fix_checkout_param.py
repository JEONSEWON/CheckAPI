file_path = "frontend/lib/api.ts"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# checkout 함수를 쿼리 파라미터 방식으로 수정
old = """  checkout: (plan: string) =>
    apiRequest('/api/v1/subscriptions/checkout', {
      method: 'POST',
      body: JSON.stringify({ variant_id: plan }),
    }),"""

new = """  checkout: (plan: string) =>
    apiRequest(`/api/v1/subscription/checkout?plan=${plan}`, {
      method: 'POST',
    }),"""

if old in content:
    content = content.replace(old, new)
    print("✅ checkout 수정 완료!")
else:
    # 이미 URL이 수정된 버전
    old2 = """  checkout: (plan: string) =>
    apiRequest('/api/v1/subscription/checkout', {
      method: 'POST',
      body: JSON.stringify({ variant_id: plan }),
    }),"""
    if old2 in content:
        content = content.replace(old2, new)
        print("✅ checkout 수정 완료! (v2)")
    else:
        print("❌ 못 찾음")
        idx = content.find("checkout:")
        print(repr(content[idx:idx+200]))

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
