file_path = "frontend/components/CreateMonitorModal.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 정확한 패턴으로 교체
old = '            {/* Silent Failure Detection */}\n          <div className="bg-orange-50'
new = '            {/* Silent Failure Detection */}\n            <div className="bg-orange-50'

if old in content:
    content = content.replace(old, new)
    print("✅ div 들여쓰기 수정!")
else:
    print("❌ 못 찾음")

# 닫는 태그도 수정
old2 = '            </div>\n          {/* Advanced toggle */}'
new2 = '            </div>\n            {/* Advanced toggle */}'

if old2 in content:
    content = content.replace(old2, new2)
    print("✅ 닫는 태그 수정!")
else:
    print("❌ 닫는 태그 못 찾음")

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("완료!")
