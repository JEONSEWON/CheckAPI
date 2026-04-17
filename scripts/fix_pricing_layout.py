file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 카드 div에 flex flex-col 추가
old_card = "key={plan.name} className={`bg-white dark:bg-gray-900 rounded-2xl border-2 p-6 ${plan.highlight ? 'border-green-500 shadow-lg' : 'border-gray-200 dark:border-gray-700'}`}>"
new_card = "key={plan.name} className={`bg-white dark:bg-gray-900 rounded-2xl border-2 p-6 flex flex-col ${plan.highlight ? 'border-green-500 shadow-lg' : 'border-gray-200 dark:border-gray-700'}`}>"

if old_card in content:
    content = content.replace(old_card, new_card)
    print("✅ 카드 flex 추가 완료!")
else:
    print("❌ 카드 못 찾음")

# 2. feature list에 flex-1 추가해서 버튼 하단 고정
old_ul = '<ul className="space-y-2 mb-6">'
new_ul = '<ul className="space-y-2 mb-6 flex-1">'

if old_ul in content:
    content = content.replace(old_ul, new_ul)
    print("✅ ul flex-1 추가 완료!")
else:
    print("❌ ul 못 찾음")

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("완료!")
