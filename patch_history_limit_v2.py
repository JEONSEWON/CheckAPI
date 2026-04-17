FILE1 = r"C:\home\jeon\api-health-monitor\backend\app\routers\monitors.py"

with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()

old_fn = '''    hours: int = Query(24, ge=1, le=168)  # Last 24 hours by default, max 7 days
):
    """
    Get check history for a monitor
    """
    # Verify monitor ownership
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found"
        )
    # Get checks from last N hours
    since = datetime.utcnow() - timedelta(hours=hours)'''

new_fn = '''    hours: int = Query(None, ge=1)
):
    """
    Get check history for a monitor
    """
    # Verify monitor ownership
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found"
        )
    # Apply plan-based history limit
    limits = PLAN_LIMITS.get(current_user.plan, PLAN_LIMITS["free"])
    max_hours = limits["history_hours"]
    if hours is None or hours > max_hours:
        hours = max_hours
    # Get checks from last N hours
    since = datetime.utcnow() - timedelta(hours=hours)'''

if old_fn in c:
    c = c.replace(old_fn, new_fn)
    print("Replace success!")
else:
    # 디버깅: 실제 파일에서 해당 라인 찾기
    lines = c.split('\n')
    for i, line in enumerate(lines):
        if 'le=168' in line or 'Last 24 hours' in line:
            print(f"Line {i}: {repr(line)}")

with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)

print("max_hours:", "max_hours" in c)
print("history_hours:", "history_hours" in c)
