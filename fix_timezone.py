file_path = "frontend/app/dashboard/monitors/[id]/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# checked_at에 Z 추가해서 UTC로 해석하게
old1 = 'formatDistanceToNow(new Date(check.checked_at), { addSuffix: true })'
new1 = 'formatDistanceToNow(new Date(check.checked_at + "Z"), { addSuffix: true })'

# last_checked_at에도 적용
old2 = 'formatDistanceToNow(new Date(monitor.last_checked_at), { addSuffix: true })'
new2 = 'formatDistanceToNow(new Date(monitor.last_checked_at + "Z"), { addSuffix: true })'

count = 0
if old1 in content:
    content = content.replace(old1, new1)
    count += 1
if old2 in content:
    content = content.replace(old2, new2)
    count += 1

if count > 0:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ 완료! ({count}개 수정)")
else:
    print("❌ 못 찾음")
