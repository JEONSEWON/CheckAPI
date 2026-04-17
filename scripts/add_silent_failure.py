file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. lucide-react import에 AlertTriangle 추가
old_import = "import { ArrowRight, CheckCircle, Zap, Shield, BarChart3, Bell, Globe } from 'lucide-react';"
new_import = "import { ArrowRight, CheckCircle, Zap, Shield, BarChart3, Bell, Globe, AlertTriangle } from 'lucide-react';"
if old_import in content:
    content = content.replace(old_import, new_import)
else:
    # Bell, Globe 없는 버전
    old_import2 = "import { ArrowRight, CheckCircle, Zap, Shield, BarChart3 } from 'lucide-react';"
    new_import2 = "import { ArrowRight, CheckCircle, Zap, Shield, BarChart3, AlertTriangle } from 'lucide-react';"
    content = content.replace(old_import2, new_import2)

# 2. Features 섹션 - Silent Failure Detection 카드 추가 (첫 번째로)
old_features = '''        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard 
            icon={<Zap className="h-8 w-8 text-green-600" />}
            title="Real-time Monitoring"
            description="Check your APIs every minute. Get instant alerts when something goes wrong."
          />'''

new_features = '''        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<AlertTriangle className="h-8 w-8 text-orange-500" />}
            title="Silent Failure Detection"
            description='Your API returns 200 OK — but the response says \\"error\\". Most monitors miss this. CheckAPI catches it.'
            highlight
          />
          <FeatureCard 
            icon={<Zap className="h-8 w-8 text-green-600" />}
            title="Real-time Monitoring"
            description="Check your APIs every minute. Get instant alerts when something goes wrong."
          />'''

if old_features in content:
    content = content.replace(old_features, new_features)
    print("✅ Feature 카드 추가 완료")
else:
    print("❌ Feature 카드 블록 못 찾음")

# 3. 히어로 서브텍스트에 Silent Failure 언급 추가
old_subtext = "Minimalist API monitoring &amp; status pages built for solo founders. 5-minute setup, zero bloat, 24/7 peace of mind."
new_subtext = "Minimalist API monitoring &amp; status pages built for solo founders. 5-minute setup, zero bloat, 24/7 peace of mind. Catches silent failures — even when your API returns 200 OK."

if old_subtext in content:
    content = content.replace(old_subtext, new_subtext)
    print("✅ 히어로 서브텍스트 수정 완료")
else:
    # 다른 버전 시도
    old_subtext2 = "Get instant alerts when your APIs go down. Simple setup, powerful monitoring, \n            and affordable pricing for developers and teams."
    new_subtext2 = "Get instant alerts when your APIs go down — including silent failures where the API returns 200 OK but something is actually broken. Simple setup, powerful monitoring."
    if old_subtext2 in content:
        content = content.replace(old_subtext2, new_subtext2)
        print("✅ 히어로 서브텍스트(v2) 수정 완료")
    else:
        print("⚠️  히어로 서브텍스트 못 찾음")

# 4. Free 플랜 pricing에 Silent failure detection 추가
old_free = "features={['10 monitors', '5-minute checks', 'All alert channels', 'Public status page', '30-day history']}"
new_free = "features={['10 monitors', '5-minute checks', 'All alert channels', 'Silent failure detection', 'Public status page', '30-day history']}"
if old_free in content:
    content = content.replace(old_free, new_free)
    print("✅ Free 플랜 pricing 수정 완료")
else:
    # 7-day history 버전
    old_free2 = "features={['10 monitors', '5-minute checks', 'All alert channels', 'Public status page', '7-day history']}"
    new_free2 = "features={['10 monitors', '5-minute checks', 'All alert channels', 'Silent failure detection', 'Public status page', '30-day history']}"
    if old_free2 in content:
        content = content.replace(old_free2, new_free2)
        print("✅ Free 플랜 pricing(v2) 수정 완료")
    else:
        print("⚠️  Free 플랜 pricing 못 찾음")

# 5. FeatureCard 컴포넌트에 highlight prop 추가
old_feature_component = '''function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white p-6 rounded-xl border border-gray-200 hover:border-green-300 hover:shadow-lg transition">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}'''

new_feature_component = '''function FeatureCard({ icon, title, description, highlight }: { icon: React.ReactNode; title: string; description: string; highlight?: boolean }) {
  return (
    <div className={`p-6 rounded-xl border hover:shadow-lg transition ${highlight ? 'bg-orange-50 dark:bg-orange-950 border-orange-200 dark:border-orange-800 hover:border-orange-400' : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-green-300'}`}>
      <div className="mb-4">{icon}</div>
      <h3 className={`text-xl font-semibold mb-2 ${highlight ? 'text-orange-700 dark:text-orange-400' : 'text-gray-900 dark:text-white'}`}>{title}</h3>
      <p className="text-gray-600 dark:text-gray-400">{description}</p>
      {highlight && (
        <div className="mt-3 text-xs font-semibold text-orange-600 dark:text-orange-400 uppercase tracking-wide">
          ★ Key differentiator
        </div>
      )}
    </div>
  );
}'''

if old_feature_component in content:
    content = content.replace(old_feature_component, new_feature_component)
    print("✅ FeatureCard 컴포넌트 수정 완료")
else:
    print("⚠️  FeatureCard 컴포넌트 못 찾음 — 수동 확인 필요")

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("\n완료!")
