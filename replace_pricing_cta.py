file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# PricingCTA import 추가
old_import = "import ClientHeader from '@/components/ClientHeader';"
new_import = "import ClientHeader from '@/components/ClientHeader';\nimport PricingCTA from '@/components/PricingCTA';"

if "PricingCTA" not in content:
    content = content.replace(old_import, new_import)
    print("✅ import 추가 완료!")

# Link 버튼을 PricingCTA로 교체
old_link = """              <Link href={plan.ctaHref} className={`block text-center py-2.5 rounded-lg font-medium transition ${plan.highlight ? 'bg-green-600 text-white hover:bg-g"""

# 더 넓게 찾기
idx = content.find('<Link href={plan.ctaHref}')
if idx == -1:
    print("❌ Link 못 찾음")
else:
    end = content.find('</Link>', idx) + len('</Link>')
    old_link_full = content[idx:end]
    print("현재 Link:", repr(old_link_full[:100]))

    new_cta = '<PricingCTA planName={plan.name} ctaHref={plan.ctaHref} highlight={plan.highlight} />'
    content = content[:idx] + new_cta + content[end:]
    print("✅ PricingCTA 교체 완료!")

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("완료!")
