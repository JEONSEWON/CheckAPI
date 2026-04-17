file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_map = """          ].map((feature) => (
            <div key={feature.title} className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-6 shadow-sm hover:shadow-md transition">
              <div className="w-10 h-10 bg-green-50 dark:bg-green-950 rounded-lg flex items-center justify-center mb-4">{feature.icon}</div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{feature.title}</h3>
              <p className"""

# 실제 끝부분 찾기
idx = content.find(old_map)
if idx == -1:
    print("❌ map 블록 못 찾음")
else:
    # </div> 두 번 더 찾아서 블록 끝 위치 파악
    end = content.find('))}', idx) + 3
    old_full = content[idx:end]
    print("현재 map 블록:")
    print(repr(old_full))
    
    new_map = """          ].map((feature) => (
            <div key={feature.title} className={`rounded-xl border p-6 shadow-sm hover:shadow-md transition ${'highlight' in feature && (feature as any).highlight ? 'bg-orange-50 dark:bg-orange-950 border-orange-200 dark:border-orange-800' : 'bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700'}`}>
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center mb-4 ${'highlight' in feature && (feature as any).highlight ? 'bg-orange-100 dark:bg-orange-900' : 'bg-green-50 dark:bg-green-950'}`}>{feature.icon}</div>
              <h3 className={`font-semibold mb-2 ${'highlight' in feature && (feature as any).highlight ? 'text-orange-700 dark:text-orange-400' : 'text-gray-900 dark:text-white'}`}>{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">{feature.description}</p>
              {'highlight' in feature && (feature as any).highlight && <p className="mt-3 text-xs font-semibold text-orange-500 uppercase tracking-wide">★ Key differentiator</p>}
            </div>
          ))}"""
    
    content = content[:idx] + new_map + content[end:]
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
