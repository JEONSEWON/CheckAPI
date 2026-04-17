FILE = r"C:\home\jeon\api-health-monitor\backend\app\routers\public.py"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

# 함수 파라미터 UUID → str 변경
c = c.replace('def calculate_uptime(monitor_id: UUID,', 'def calculate_uptime(monitor_id: str,')
c = c.replace('def get_average_response_time(monitor_id: UUID,', 'def get_average_response_time(monitor_id: str,')
c = c.replace('def get_incidents(monitor_id: UUID,', 'def get_incidents(monitor_id: str,')
c = c.replace('def get_public_status(monitor_id: UUID,', 'def get_public_status(monitor_id: str,')
c = c.replace('def get_status_badge(monitor_id: UUID,', 'def get_status_badge(monitor_id: str,')

# monitor_id: UUID 파라미터 (get_check_history 등)
c = c.replace('    monitor_id: UUID,\n    hours: int = 24,', '    monitor_id: str,\n    hours: int = 24,')

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
print("UUID remaining:", c.count('monitor_id: UUID'))
