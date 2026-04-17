FILE = r"C:\home\jeon\api-health-monitor\frontend\components\CreateMonitorModal.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

# Fragment 열고 닫는 방식 수정
old_open = "            {/* Advanced toggle — HTTP only */}\n            {monitorType === 'http' && <>"
new_open = "            {/* Advanced toggle — HTTP only */}\n            {monitorType === 'http' && ("

old_close = "            {monitorType === 'http' && </>}"
new_close = "            )}"

c = c.replace(old_open, new_open)
c = c.replace(old_close, new_close)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
print("Fragment fixed:", "{monitorType === 'http' && </" not in c)
