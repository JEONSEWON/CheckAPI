FILE = r"C:\home\jeon\api-health-monitor\backend\app\tasks.py"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

# send_alerts 함수에 maintenance window 체크 추가
old_send = '''        monitor = db.query(Monitor).filter(Monitor.id == monitor_id).first()
        if not monitor:
            return
        print(f"🚨 ALERT: {monitor.name} changed from {old_status} to {new_status}")
        # Get alert channels for this monitor
        alert_channels = monitor.alert_channels'''

new_send = '''        monitor = db.query(Monitor).filter(Monitor.id == monitor_id).first()
        if not monitor:
            return
        print(f"🚨 ALERT: {monitor.name} changed from {old_status} to {new_status}")

        # Check if monitor is in active maintenance window
        if is_in_maintenance(monitor, db):
            print(f"🔕 Suppressed: {monitor.name} is in maintenance window")
            return

        # Get alert channels for this monitor
        alert_channels = monitor.alert_channels'''

c = c.replace(old_send, new_send)

# is_in_maintenance 함수 추가 (send_alerts 함수 바로 앞에)
maintenance_fn = '''
def is_in_maintenance(monitor, db) -> bool:
    """Check if monitor is currently in an active maintenance window"""
    from app.models import MaintenanceWindow
    from datetime import datetime, timezone
    import pytz

    now_utc = datetime.utcnow()

    # Get all active maintenance windows for this monitor or user
    windows = db.query(MaintenanceWindow).filter(
        MaintenanceWindow.user_id == monitor.user_id,
        MaintenanceWindow.is_active == True
    ).all()

    for window in windows:
        # Check if window applies to this monitor (empty = all monitors)
        if window.monitors and monitor not in window.monitors:
            continue

        # Convert now to window timezone
        try:
            tz = pytz.timezone(window.timezone)
            now_local = datetime.now(tz)
        except Exception:
            now_local = now_utc.replace(tzinfo=timezone.utc)

        current_time = now_local.strftime("%H:%M")
        current_weekday = now_local.weekday()  # 0=Mon
        current_day = now_local.day

        in_time_range = window.start_time <= current_time <= window.end_time

        if not in_time_range:
            continue

        if window.repeat_type == "daily":
            return True
        elif window.repeat_type == "weekly" and window.weekday == current_weekday:
            return True
        elif window.repeat_type == "monthly" and window.day_of_month == current_day:
            return True
        elif window.repeat_type == "once":
            if window.start_date and window.end_date:
                if window.start_date <= now_utc <= window.end_date:
                    return True

    return False


'''

old_task_decorator = '@celery_app.task(name="app.tasks.send_alerts")'
c = c.replace(old_task_decorator, maintenance_fn + old_task_decorator)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
print("is_in_maintenance:", "is_in_maintenance" in c)
print("Suppressed log:", "Suppressed" in c)
