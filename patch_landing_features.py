FILE = r"C:\home\jeon\api-health-monitor\frontend\app\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. "coming soon" → 구현 완료로 변경
old_features = """            { icon: <CheckCircle style={{ width: '20px', height: '20px' }} />, title: 'Silent Failure Detection', desc: 'Your API returns 200 OK — but the response body contains an error, null data, or broken content. CheckAPI validates the body with <strong style={{ color: \'#00e5b4\' }}>Regex patterns</strong>, not just status codes.' },"""
# 그냥 assertions 리스트만 수정
old_assertions_list = """                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      {['Keyword match (present / absent)', 'Regex pattern matching', 'JSON field assertion (coming soon)'].map((f, i) => (
                        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '14px', color: i === 2 ? '#334155' : '#94a3b8' }}>
                          <CheckCircle style={{ width: '14px', height: '14px', color: i === 2 ? '#334155' : '#00e5b4', flexShrink: 0 }} />
                          {f}
                        </div>
                      ))}
                    </div>"""

new_assertions_list = """                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      {[
                        'Keyword match (present / absent)',
                        'Regex pattern matching',
                        'JSON Path assertions (up to 10)',
                        'Header assertion (Content-Type, etc.)',
                      ].map((f, i) => (
                        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '14px', color: '#94a3b8' }}>
                          <CheckCircle style={{ width: '14px', height: '14px', color: '#00e5b4', flexShrink: 0 }} />
                          {f}
                        </div>
                      ))}
                    </div>"""

c = c.replace(old_assertions_list, new_assertions_list)

# 2. Features grid에 Heartbeat 추가 (Maintenance Windows 앞에)
old_maintenance = "            { icon: <Lock style={{ width: '20px', height: '20px' }} />, title: 'Maintenance Windows', desc: 'Schedule recurring windows. Alerts suppressed, checks still run.' },"
new_maintenance = """            { icon: <Activity style={{ width: '20px', height: '20px' }} />, title: 'Heartbeat / Cron Monitoring', desc: 'Monitor cron jobs and scheduled tasks. Get alerted if your job doesn\\'t run on time.' },
            { icon: <Lock style={{ width: '20px', height: '20px' }} />, title: 'Maintenance Windows', desc: 'Schedule recurring windows. Alerts suppressed, checks still run.' },"""
c = c.replace(old_maintenance, new_maintenance)

# 3. import에 Activity 추가 (없으면)
if 'Activity' not in c:
    c = c.replace(
        "import { ArrowRight, CheckCircle, Zap, Shield, BarChart3, Bell, Globe, Code2, Terminal, Lock } from 'lucide-react';",
        "import { ArrowRight, CheckCircle, Zap, Shield, BarChart3, Bell, Globe, Code2, Terminal, Lock, Activity } from 'lucide-react';"
    )

# 4. 푸터 #pricing → /pricing
c = c.replace("href: '#pricing'", "href: '/pricing'")
c = c.replace('href="#pricing"', 'href="/pricing"')
c = c.replace('href="/#pricing"', 'href="/pricing"')

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
print("coming soon removed:", "coming soon" not in c)
print("Heartbeat feature:", "Heartbeat / Cron" in c)
print("JSON Path added:", "JSON Path assertions" in c)
print("Header assertion:", "Header assertion" in c)
