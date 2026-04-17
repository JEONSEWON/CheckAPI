file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = "            { icon: <Zap className=\"h-6 w-6 text-green-600 dark:text-green-400\" />, title: 'Instant Alerts', description: 'Check your APIs every minute. Get instant alerts when something goes wrong.' },"

new = """            { icon: <Shield className="h-6 w-6 text-orange-500" />, title: 'Silent Failure Detection', description: 'Your API returns 200 OK — but the response body says "error". Most monitors miss this. CheckAPI catches it.', highlight: true },
            { icon: <Zap className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Instant Alerts', description: 'Check your APIs every minute. Get instant alerts when something goes wrong.' },"""

if old in content:
    content = content.replace(old, new)
    print("✅ Silent Failure 카드 첫 번째로 이동 완료!")
else:
    print("❌ 못 찾음")

# Silent Failure 기존 항목 제거 (중복 방지)
old_dup = "            { icon: <Shield className=\"h-6 w-6 text-green-600 dark:text-green-400\" />, title: 'Silent Failure Detection', description: 'Catches failures even when your API returns 200 OK but something is actually broken.' },"
content = content.replace(old_dup, "")

# .map() 렌더링 부분 — highlight 스타일 추가
old_map = """          ].map((feature, i) => (
            <div key={i} className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-green-300 dark:hover:border-green-600 hover:shadow-lg transition">
              <div className="mb-4 p-2 bg-green-50 dark:bg-green-900/30 rounded-lg w-fit">{feature.icon}</div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">{feature.description}</p>
            </div>
          ))}"""

new_map = """          ].map((feature, i) => (
            <div key={i} className={`p-6 rounded-xl border hover:shadow-lg transition ${(feature as any).highlight ? 'bg-orange-50 dark:bg-orange-950 border-orange-200 dark:border-orange-800 hover:border-orange-400' : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-green-300 dark:hover:border-green-600'}`}>
              <div className={`mb-4 p-2 rounded-lg w-fit ${(feature as any).highlight ? 'bg-orange-100 dark:bg-orange-900/30' : 'bg-green-50 dark:bg-green-900/30'}`}>{feature.icon}</div>
              <h3 className={`text-lg font-semibold mb-2 ${(feature as any).highlight ? 'text-orange-700 dark:text-orange-400' : 'text-gray-900 dark:text-white'}`}>{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">{feature.description}</p>
              {(feature as any).highlight && <p className="mt-3 text-xs font-semibold text-orange-500 uppercase tracking-wide">★ Key differentiator</p>}
            </div>
          ))}"""

if old_map in content:
    content = content.replace(old_map, new_map)
    print("✅ 카드 렌더링 highlight 스타일 추가 완료!")
else:
    print("⚠️  map 블록 못 찾음 — 카드 순서만 변경됨")

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("\n완료!")
