# landing page
with open('frontend/app/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old = "features: ['Unlimited monitors','10-second checks','API access','Custom features','SLA','1-year history']"
new = "features: ['Unlimited monitors','10-second checks','REST API access (API keys)','Custom features','SLA','1-year history']"

if old in content:
    content = content.replace(old, new)
    with open('frontend/app/page.tsx', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print("✅ landing page 완료!")
else:
    print("❌ 못 찾음")

# settings page
with open('frontend/app/dashboard/settings/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old2 = "features: ['Unlimited monitors', '10-second checks', 'All alert channels', 'Analytics', 'Team sharing (unlimited)', 'Keyword validation', 'SSL monitoring', '1-year history']"
new2 = "features: ['Unlimited monitors', '10-second checks', 'All alert channels', 'Analytics', 'Team sharing (unlimited)', 'Keyword validation', 'SSL monitoring', 'REST API access', '1-year history']"

if old2 in content:
    content = content.replace(old2, new2)
    with open('frontend/app/dashboard/settings/page.tsx', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print("✅ settings page 완료!")
else:
    print("❌ 못 찾음")
