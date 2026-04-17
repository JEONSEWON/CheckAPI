import re

# ── 1. 백엔드 monitors.py ────────────────────────────────────────────────────
FILE1 = r"C:\home\jeon\api-health-monitor\backend\app\routers\monitors.py"

with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()

# PLAN_LIMITS에 history_hours 추가
old_limits = '''PLAN_LIMITS = {
    "free": {"max_monitors": 10, "min_interval": 300},  # 5 minutes
    "starter": {"max_monitors": 20, "min_interval": 60},  # 1 minute
    "pro": {"max_monitors": 100, "min_interval": 30},  # 30 seconds
    "business": {"max_monitors": -1, "min_interval": 10},  # unlimited, 10 seconds
}'''
new_limits = '''PLAN_LIMITS = {
    "free":     {"max_monitors": 10,  "min_interval": 300, "history_hours": 720},    # 30 days
    "starter":  {"max_monitors": 20,  "min_interval": 60,  "history_hours": 720},    # 30 days
    "pro":      {"max_monitors": 100, "min_interval": 30,  "history_hours": 2160},   # 90 days
    "business": {"max_monitors": -1,  "min_interval": 10,  "history_hours": 8760},   # 365 days
}'''
c = c.replace(old_limits, new_limits)

# checks 엔드포인트 hours 제한 수정
old_endpoint = '''    hours: int = Query(24, ge=1, le=168)  # Last 24 hours by default, max 7 days
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
new_endpoint = '''    hours: int = Query(None, ge=1)
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
c = c.replace(old_endpoint, new_endpoint)

with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)

print("Backend done!")
print("history_hours:", "history_hours" in c)
print("max_hours:", "max_hours" in c)

# ── 2. 프론트 page.tsx - hours 파라미터 제거 ─────────────────────────────────
FILE2 = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\monitors\[id]\page.tsx"

with open(FILE2, 'r', encoding='utf-8') as f:
    c2 = f.read()

old_checks = '''      const checksResponse = await monitorsAPI.checks(monitorId, {
        page: 1,
        page_size: 20,
      });'''
new_checks = '''      const checksResponse = await monitorsAPI.checks(monitorId, {
        page: 1,
        page_size: 20,
      }); // hours omitted — backend applies plan limit automatically'''
c2 = c2.replace(old_checks, new_checks)

with open(FILE2, 'w', encoding='utf-8') as f:
    f.write(c2)

print("\nFrontend done!")
print("plan limit comment:", "plan limit automatically" in c2)
