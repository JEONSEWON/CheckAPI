import os

# ── 1. models.py - Heartbeat 필드 추가 ───────────────────────────────────────
FILE_MODELS = r"C:\home\jeon\api-health-monitor\backend\app\models.py"

with open(FILE_MODELS, 'r', encoding='utf-8') as f:
    c = f.read()

old_keyword = "    # Response body validation\n    keyword = Column(String(500))"
new_keyword = """    # Monitor type
    monitor_type = Column(String(20), default="http")  # http, heartbeat

    # Heartbeat fields (null for http monitors)
    heartbeat_token = Column(String(64), unique=True, nullable=True)
    heartbeat_interval = Column(Integer, nullable=True)  # expected ping interval in minutes
    heartbeat_grace = Column(Integer, nullable=True, default=5)  # grace period in minutes
    last_ping_at = Column(DateTime, nullable=True)

    # Response body validation
    keyword = Column(String(500))"""

c = c.replace(old_keyword, new_keyword)

with open(FILE_MODELS, 'w', encoding='utf-8') as f:
    f.write(c)
print("models.py done!", "heartbeat_token" in c)


# ── 2. schemas.py - Heartbeat 스키마 추가 ────────────────────────────────────
FILE_SCHEMAS = r"C:\home\jeon\api-health-monitor\backend\app\schemas.py"

with open(FILE_SCHEMAS, 'r', encoding='utf-8') as f:
    c = f.read()

# MonitorCreate에 heartbeat 필드 추가
old_create_keyword = "    keyword: Optional[str] = Field(None, max_length=500)\n    keyword_present: bool = Field(default=True)\n    use_regex: bool = Field(default=False)"
new_create_keyword = """    monitor_type: str = Field(default="http", pattern="^(http|heartbeat)$")
    heartbeat_interval: Optional[int] = Field(None, ge=1, le=10080)  # 1 min to 1 week
    heartbeat_grace: Optional[int] = Field(None, ge=1, le=1440)
    keyword: Optional[str] = Field(None, max_length=500)
    keyword_present: bool = Field(default=True)
    use_regex: bool = Field(default=False)"""
c = c.replace(old_create_keyword, new_create_keyword)

# MonitorUpdate에 heartbeat 필드 추가
old_update_keyword = "    keyword: Optional[str] = Field(None, max_length=500)\n    keyword_present: Optional[bool] = None\n    use_regex: Optional[bool] = None\n    is_active: Optional[bool] = None"
new_update_keyword = """    heartbeat_interval: Optional[int] = Field(None, ge=1, le=10080)
    heartbeat_grace: Optional[int] = Field(None, ge=1, le=1440)
    keyword: Optional[str] = Field(None, max_length=500)
    keyword_present: Optional[bool] = None
    use_regex: Optional[bool] = None
    is_active: Optional[bool] = None"""
c = c.replace(old_update_keyword, new_update_keyword)

# MonitorResponse에 heartbeat 필드 추가
old_response = "    keyword: Optional[str]\n    keyword_present: bool\n    use_regex: bool = False\n    is_active: bool"
new_response = """    monitor_type: str = "http"
    heartbeat_token: Optional[str] = None
    heartbeat_interval: Optional[int] = None
    heartbeat_grace: Optional[int] = None
    last_ping_at: Optional[datetime] = None
    keyword: Optional[str]
    keyword_present: bool
    use_regex: bool = False
    is_active: bool"""
c = c.replace(old_response, new_response)

with open(FILE_SCHEMAS, 'w', encoding='utf-8') as f:
    f.write(c)
print("schemas.py done!", "heartbeat_token" in c)


# ── 3. heartbeat.py 라우터 생성 ──────────────────────────────────────────────
ROUTER_FILE = r"C:\home\jeon\api-health-monitor\backend\app\routers\heartbeat.py"

router_content = '''"""
Heartbeat / Cron Job monitoring endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Monitor, Check

router = APIRouter(prefix="/api/v1/heartbeat", tags=["Heartbeat"])


@router.get("/{token}")
@router.post("/{token}")
async def receive_heartbeat(token: str, request: Request, db: Session = Depends(get_db)):
    """
    Receive a heartbeat ping from a cron job or scheduled task.
    Accepts both GET and POST requests.
    No authentication required — token IS the authentication.
    """
    monitor = db.query(Monitor).filter(
        Monitor.heartbeat_token == token,
        Monitor.monitor_type == "heartbeat",
        Monitor.is_active == True
    ).first()

    if not monitor:
        raise HTTPException(status_code=404, detail="Heartbeat monitor not found")

    now = datetime.utcnow()
    previous_status = monitor.last_status

    # Update last ping time
    monitor.last_ping_at = now
    monitor.last_status = "up"
    monitor.last_checked_at = now
    monitor.updated_at = now

    # Record check
    check = Check(
        monitor_id=str(monitor.id),
        status="up",
        status_code=200,
        response_time=0,
        error_message=None,
        checked_at=now,
    )
    db.add(check)
    db.commit()

    # Send recovery alert if was down
    if previous_status == "down":
        from app.tasks import send_alerts
        send_alerts.delay(str(monitor.id), "up", "down")

    return {
        "ok": True,
        "monitor": monitor.name,
        "received_at": now.isoformat(),
        "next_expected_in": f"{monitor.heartbeat_interval}m" if monitor.heartbeat_interval else None,
    }
'''

with open(ROUTER_FILE, 'w', encoding='utf-8') as f:
    f.write(router_content)
print("heartbeat router created!")


# ── 4. monitors.py 라우터에 heartbeat 생성 로직 추가 ─────────────────────────
FILE_MONITORS = r"C:\home\jeon\api-health-monitor\backend\app\routers\monitors.py"

with open(FILE_MONITORS, 'r', encoding='utf-8') as f:
    c = f.read()

# import secrets 추가
if "import secrets" not in c:
    c = "import secrets\n" + c

# create monitor에서 heartbeat token 자동 생성
old_create = """    # Check plan limits
    check_plan_limits(current_user, db, creating_new=True)

    # Validate interval
    validate_interval(current_user, monitor_data.interval)"""

new_create = """    # Check plan limits
    check_plan_limits(current_user, db, creating_new=True)

    # Heartbeat monitors don't need interval validation
    if monitor_data.monitor_type != "heartbeat":
        validate_interval(current_user, monitor_data.interval)"""

c = c.replace(old_create, new_create)

# Monitor 생성 시 heartbeat_token 자동 부여
old_monitor_create = """    monitor = Monitor(
        user_id=current_user.id,
        name=monitor_data.name,
        url=str(monitor_data.url),"""

new_monitor_create = """    # Generate heartbeat token if needed
    heartbeat_token = None
    if monitor_data.monitor_type == "heartbeat":
        heartbeat_token = secrets.token_urlsafe(48)

    monitor = Monitor(
        user_id=current_user.id,
        monitor_type=monitor_data.monitor_type,
        heartbeat_token=heartbeat_token,
        heartbeat_interval=monitor_data.heartbeat_interval,
        heartbeat_grace=monitor_data.heartbeat_grace if monitor_data.heartbeat_grace else 5,
        last_status="pending" if monitor_data.monitor_type == "heartbeat" else None,
        name=monitor_data.name,
        url=str(monitor_data.url) if monitor_data.url else "heartbeat","""

c = c.replace(old_monitor_create, new_monitor_create)

with open(FILE_MONITORS, 'w', encoding='utf-8') as f:
    f.write(c)
print("monitors router done!", "heartbeat_token" in c)


# ── 5. tasks.py에 check_heartbeat_monitors 추가 ───────────────────────────────
FILE_TASKS = r"C:\home\jeon\api-health-monitor\backend\app\tasks.py"

with open(FILE_TASKS, 'r', encoding='utf-8') as f:
    c = f.read()

heartbeat_task = '''

@celery_app.task(name="app.tasks.check_heartbeat_monitors")
def check_heartbeat_monitors():
    """
    Check heartbeat monitors for missing pings.
    Runs every minute.
    """
    from datetime import timedelta
    db = SessionLocal()
    try:
        from app.models import Monitor
        monitors = db.query(Monitor).filter(
            Monitor.monitor_type == "heartbeat",
            Monitor.is_active == True,
        ).all()

        alerted = 0
        for monitor in monitors:
            if not monitor.last_ping_at:
                continue  # Never pinged yet — stay pending

            interval = monitor.heartbeat_interval or 5
            grace = monitor.heartbeat_grace or 5
            threshold_minutes = interval + grace

            now = datetime.utcnow()
            elapsed = (now - monitor.last_ping_at).total_seconds() / 60

            if elapsed > threshold_minutes:
                if monitor.last_status != "down":
                    previous_status = monitor.last_status
                    monitor.last_status = "down"
                    monitor.last_checked_at = now
                    monitor.updated_at = now

                    # Record failed check
                    from app.models import Check
                    check = Check(
                        monitor_id=str(monitor.id),
                        status="down",
                        status_code=None,
                        response_time=None,
                        error_message=f"No ping received in {elapsed:.0f}m (expected every {interval}m + {grace}m grace)",
                        checked_at=now,
                    )
                    db.add(check)
                    db.commit()

                    send_alerts.delay(str(monitor.id), "down", previous_status or "pending")
                    alerted += 1

        return {"checked": len(monitors), "alerted": alerted}
    finally:
        db.close()

'''

# cleanup_old_checks 앞에 추가
old_cleanup = '@celery_app.task(name="app.tasks.cleanup_old_checks")'
c = c.replace(old_cleanup, heartbeat_task + old_cleanup)

with open(FILE_TASKS, 'w', encoding='utf-8') as f:
    f.write(c)
print("tasks.py done!", "check_heartbeat_monitors" in c)


# ── 6. celery_app.py에 beat schedule 추가 ────────────────────────────────────
FILE_CELERY = r"C:\home\jeon\api-health-monitor\backend\app\celery_app.py"

with open(FILE_CELERY, 'r', encoding='utf-8') as f:
    c = f.read()

old_schedule = '    "check-ssl-certificates": {'
new_schedule = '''    "check-heartbeat-monitors": {
        "task": "app.tasks.check_heartbeat_monitors",
        "schedule": 60.0,  # Every 60 seconds
    },
    "check-ssl-certificates": {'''
c = c.replace(old_schedule, new_schedule)

with open(FILE_CELERY, 'w', encoding='utf-8') as f:
    f.write(c)
print("celery_app.py done!", "check_heartbeat_monitors" in c)


# ── 7. main.py에 heartbeat router 등록 ───────────────────────────────────────
FILE_MAIN = r"C:\home\jeon\api-health-monitor\backend\app\main.py"

with open(FILE_MAIN, 'r', encoding='utf-8') as f:
    c = f.read()

if "heartbeat" not in c:
    old_import = "from app.routers import assertions"
    new_import = "from app.routers import assertions\nfrom app.routers import heartbeat"
    c = c.replace(old_import, new_import)

    old_include = "app.include_router(assertions.router)"
    new_include = "app.include_router(assertions.router)\napp.include_router(heartbeat.router)"
    c = c.replace(old_include, new_include)

    with open(FILE_MAIN, 'w', encoding='utf-8') as f:
        f.write(c)
    print("main.py done!")


# ── 8. DB 마이그레이션 ────────────────────────────────────────────────────────
MIGRATE_FILE = r"C:\home\jeon\api-health-monitor\migrate_heartbeat.py"

migration = '''import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS monitor_type VARCHAR(20) DEFAULT \'http\';")
cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS heartbeat_token VARCHAR(64) UNIQUE;")
cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS heartbeat_interval INTEGER;")
cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS heartbeat_grace INTEGER DEFAULT 5;")
cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS last_ping_at TIMESTAMP;")
cur.execute("CREATE INDEX IF NOT EXISTS idx_monitors_heartbeat_token ON monitors(heartbeat_token);")

conn.commit()
cur.close()
conn.close()
print("Migration done! Heartbeat fields added.")
'''

with open(MIGRATE_FILE, 'w', encoding='utf-8') as f:
    f.write(migration)
print("Migration script created!")
print("\nAll backend done!")
