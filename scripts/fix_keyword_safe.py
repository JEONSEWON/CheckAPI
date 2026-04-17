file_path = "frontend/components/CreateMonitorModal.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_length = len(content)

# 1. Advanced 기본값을 true로 변경 (항상 열려있게)
old_advanced = "const [showAdvanced, setShowAdvanced] = useState(false);"
new_advanced = "const [showAdvanced, setShowAdvanced] = useState(true);"

if old_advanced in content:
    content = content.replace(old_advanced, new_advanced)
    print("✅ Advanced 기본 열림 설정 완료!")
else:
    print("❌ Advanced state 못 찾음")

# 2. Keyword Check 라벨 강조
old_label = '                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">\n                    Response Keyword <span className="text-gray-400 font-normal">(op'
new_label = '                  <label className="block text-sm font-medium text-orange-600 dark:text-orange-400 mb-2">\n                    ⚡ Silent Failure Detection <span className="text-gray-400 font-normal text-xs">(op'

if old_label in content:
    content = content.replace(old_label, new_label)
    print("✅ Keyword 라벨 강조 완료!")
else:
    print("❌ Keyword 라벨 못 찾음")

# 파일 길이 체크
if len(content) < original_length - 100:
    print("❌ 파일이 잘렸어요! 저장 안 함")
else:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ 저장 완료! (원본 {original_length}자 → {len(content)}자)")
