with open('frontend/app/dashboard/monitors/[id]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# alert channel 관련 부분 찾기
idx = content.lower().find('alert')
print("=== alert 관련 코드 ===")
print(content[idx:idx+1000])
