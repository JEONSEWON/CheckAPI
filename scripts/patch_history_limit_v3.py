FILE1 = r"C:\home\jeon\api-health-monitor\backend\app\routers\monitors.py"

with open(FILE1, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 264번 라인 (0-indexed: 263) 교체
for i, line in enumerate(lines):
    if 'le=168' in line and 'Last 24 hours' in line:
        print(f"Found at line {i+1}: {repr(line)}")
        lines[i] = '    hours: int = Query(None, ge=1)\n'
        print(f"Replaced with: {repr(lines[i])}")
        break

# "Get checks from last N hours" 아래에 plan limit 코드 삽입
for i, line in enumerate(lines):
    if '# Get checks from last N hours' in line:
        print(f"Found injection point at line {i+1}")
        lines[i] = (
            '    # Apply plan-based history limit\n'
            '    limits = PLAN_LIMITS.get(current_user.plan, PLAN_LIMITS["free"])\n'
            '    max_hours = limits["history_hours"]\n'
            '    if hours is None or hours > max_hours:\n'
            '        hours = max_hours\n'
            '    # Get checks from last N hours\n'
        )
        break

with open(FILE1, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nDone!")
print("max_hours:", "max_hours" in ''.join(lines))
print("history_hours:", "history_hours" in ''.join(lines))
