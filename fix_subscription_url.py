file_path = "frontend/lib/api.ts"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# subscriptions → subscription (s 제거)
old = "// Subscription API\nexport const subscriptionAPI = {"
# 전체 subscriptionAPI 블록에서 URL 수정
content = content.replace(
    "apiRequest('/api/v1/subscriptions/current')",
    "apiRequest('/api/v1/subscription/')"
)
content = content.replace(
    "apiRequest('/api/v1/subscriptions/checkout'",
    "apiRequest('/api/v1/subscription/checkout'"
)
content = content.replace(
    "apiRequest('/api/v1/subscriptions/cancel'",
    "apiRequest('/api/v1/subscription/cancel'"
)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("✅ 완료!")
