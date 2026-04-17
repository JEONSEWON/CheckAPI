import os

# ── 1. models.py - MaintenanceWindow 모델 추가 ───────────────────────────────
FILE_MODELS = r"C:\home\jeon\api-health-monitor\backend\app\models.py"

with open(FILE_MODELS, 'r', encoding='utf-8') as f:
    c = f.read()

maintenance_model = '''

class MaintenanceWindow(Base):
    """Maintenance Window - suppress alerts during scheduled maintenance"""
    __tablename__ = "maintenance_windows"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    repeat_type = Column(String(20), default="once")  # once, daily, weekly, monthly
    weekday = Column(Integer)  # 0=Mon ~ 6=Sun (weekly only)
    day_of_month = Column(Integer)  # 1-31 (monthly only)
    start_time = Column(String(5), nullable=False)  # HH:MM
    end_time = Column(String(5), nullable=False)    # HH:MM
    start_date = Column(DateTime)  # once only
    end_date = Column(DateTime)    # once only
    timezone = Column(String(50), default="UTC")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="maintenance_windows")
    monitors = relationship("Monitor", secondary="maintenance_window_monitors", back_populates="maintenance_windows")


class MaintenanceWindowMonitor(Base):
    """Many-to-Many: MaintenanceWindow <-> Monitor"""
    __tablename__ = "maintenance_window_monitors"

    maintenance_window_id = Column(String(36), ForeignKey("maintenance_windows.id", ondelete="CASCADE"), primary_key=True)
    monitor_id = Column(String(36), ForeignKey("monitors.id", ondelete="CASCADE"), primary_key=True)
'''

# APIKey 클래스 뒤에 추가
c = c + maintenance_model

# User에 maintenance_windows relationship 추가
old_user_rel = "    api_keys = relationship(\"APIKey\", back_populates=\"user\", cascade=\"all, delete-orphan\")"
new_user_rel = "    api_keys = relationship(\"APIKey\", back_populates=\"user\", cascade=\"all, delete-orphan\")\n    maintenance_windows = relationship(\"MaintenanceWindow\", back_populates=\"user\", cascade=\"all, delete-orphan\")"
c = c.replace(old_user_rel, new_user_rel)

# Monitor에 maintenance_windows relationship 추가
old_monitor_rel = "    alert_channels = relationship(\"AlertChannel\", secondary=\"monitor_alert_channels\", back_populates=\"monitors\")"
new_monitor_rel = "    alert_channels = relationship(\"AlertChannel\", secondary=\"monitor_alert_channels\", back_populates=\"monitors\")\n    maintenance_windows = relationship(\"MaintenanceWindow\", secondary=\"maintenance_window_monitors\", back_populates=\"monitors\")"
c = c.replace(old_monitor_rel, new_monitor_rel)

with open(FILE_MODELS, 'w', encoding='utf-8') as f:
    f.write(c)

print("models.py done!", "MaintenanceWindow" in c)


# ── 2. schemas.py - MaintenanceWindow 스키마 추가 ────────────────────────────
FILE_SCHEMAS = r"C:\home\jeon\api-health-monitor\backend\app\schemas.py"

with open(FILE_SCHEMAS, 'r', encoding='utf-8') as f:
    c = f.read()

maintenance_schemas = '''

class MaintenanceWindowCreate(BaseModel):
    name: str = Field(..., max_length=255)
    repeat_type: str = Field(default="once", pattern="^(once|daily|weekly|monthly)$")
    weekday: Optional[int] = Field(None, ge=0, le=6)
    day_of_month: Optional[int] = Field(None, ge=1, le=31)
    start_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    end_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    timezone: str = Field(default="UTC", max_length=50)
    monitor_ids: List[str] = []


class MaintenanceWindowResponse(BaseModel):
    id: UUID
    name: str
    repeat_type: str
    weekday: Optional[int]
    day_of_month: Optional[int]
    start_time: str
    end_time: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    timezone: str
    is_active: bool
    created_at: datetime
    monitor_ids: List[str] = []

    class Config:
        from_attributes = True
'''

c = c + maintenance_schemas

with open(FILE_SCHEMAS, 'w', encoding='utf-8') as f:
    f.write(c)

print("schemas.py done!", "MaintenanceWindowCreate" in c)


# ── 3. maintenance.py 라우터 생성 ────────────────────────────────────────────
ROUTER_FILE = r"C:\home\jeon\api-health-monitor\backend\app\routers\maintenance.py"

router_content = '''"""
Maintenance Window API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.models import User, MaintenanceWindow, Monitor, MaintenanceWindowMonitor
from app.schemas import MaintenanceWindowCreate, MaintenanceWindowResponse
from datetime import datetime

router = APIRouter(prefix="/api/v1/maintenance", tags=["Maintenance"])


@router.get("/", response_model=List[MaintenanceWindowResponse])
def list_maintenance_windows(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    windows = db.query(MaintenanceWindow).filter(
        MaintenanceWindow.user_id == current_user.id
    ).order_by(MaintenanceWindow.created_at.desc()).all()

    result = []
    for w in windows:
        d = MaintenanceWindowResponse(
            id=w.id,
            name=w.name,
            repeat_type=w.repeat_type,
            weekday=w.weekday,
            day_of_month=w.day_of_month,
            start_time=w.start_time,
            end_time=w.end_time,
            start_date=w.start_date,
            end_date=w.end_date,
            timezone=w.timezone,
            is_active=w.is_active,
            created_at=w.created_at,
            monitor_ids=[str(m.id) for m in w.monitors]
        )
        result.append(d)
    return result


@router.post("/", response_model=MaintenanceWindowResponse)
def create_maintenance_window(
    data: MaintenanceWindowCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    window = MaintenanceWindow(
        user_id=current_user.id,
        name=data.name,
        repeat_type=data.repeat_type,
        weekday=data.weekday,
        day_of_month=data.day_of_month,
        start_time=data.start_time,
        end_time=data.end_time,
        start_date=data.start_date,
        end_date=data.end_date,
        timezone=data.timezone,
    )
    db.add(window)
    db.flush()

    # Attach monitors
    if data.monitor_ids:
        monitors = db.query(Monitor).filter(
            Monitor.id.in_(data.monitor_ids),
            Monitor.user_id == current_user.id
        ).all()
        window.monitors = monitors

    db.commit()
    db.refresh(window)

    return MaintenanceWindowResponse(
        id=window.id,
        name=window.name,
        repeat_type=window.repeat_type,
        weekday=window.weekday,
        day_of_month=window.day_of_month,
        start_time=window.start_time,
        end_time=window.end_time,
        start_date=window.start_date,
        end_date=window.end_date,
        timezone=window.timezone,
        is_active=window.is_active,
        created_at=window.created_at,
        monitor_ids=[str(m.id) for m in window.monitors]
    )


@router.patch("/{window_id}/toggle", response_model=MaintenanceWindowResponse)
def toggle_maintenance_window(
    window_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    window = db.query(MaintenanceWindow).filter(
        MaintenanceWindow.id == window_id,
        MaintenanceWindow.user_id == current_user.id
    ).first()
    if not window:
        raise HTTPException(status_code=404, detail="Maintenance window not found")
    window.is_active = not window.is_active
    window.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(window)
    return MaintenanceWindowResponse(
        id=window.id,
        name=window.name,
        repeat_type=window.repeat_type,
        weekday=window.weekday,
        day_of_month=window.day_of_month,
        start_time=window.start_time,
        end_time=window.end_time,
        start_date=window.start_date,
        end_date=window.end_date,
        timezone=window.timezone,
        is_active=window.is_active,
        created_at=window.created_at,
        monitor_ids=[str(m.id) for m in window.monitors]
    )


@router.delete("/{window_id}")
def delete_maintenance_window(
    window_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    window = db.query(MaintenanceWindow).filter(
        MaintenanceWindow.id == window_id,
        MaintenanceWindow.user_id == current_user.id
    ).first()
    if not window:
        raise HTTPException(status_code=404, detail="Maintenance window not found")
    db.delete(window)
    db.commit()
    return {"message": "Deleted"}
'''

with open(ROUTER_FILE, 'w', encoding='utf-8') as f:
    f.write(router_content)
print("maintenance router created!")


# ── 4. main.py에 router 등록 ─────────────────────────────────────────────────
MAIN_FILES = [
    r"C:\home\jeon\api-health-monitor\backend\app\main.py",
    r"C:\home\jeon\api-health-monitor\backend\main.py",
]
for MAIN_FILE in MAIN_FILES:
    if not os.path.exists(MAIN_FILE):
        continue
    with open(MAIN_FILE, 'r', encoding='utf-8') as f:
        c = f.read()
    if "maintenance" not in c:
        old_import = "from app.routers import"
        if old_import in c:
            # 마지막 router import 찾아서 maintenance 추가
            import re
            match = re.search(r'from app\.routers import ([^\n]+)', c)
            if match:
                old_line = match.group(0)
                new_line = old_line + "\nfrom app.routers import maintenance"
                c = c.replace(old_line, new_line)
        # router include 찾기
        old_include = "app.include_router(alert_channels.router)"
        if old_include in c:
            c = c.replace(old_include, old_include + "\napp.include_router(maintenance.router)")
        with open(MAIN_FILE, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"main.py updated: {MAIN_FILE}")
    break


# ── 5. DB 마이그레이션 스크립트 ──────────────────────────────────────────────
MIGRATE_FILE = r"C:\home\jeon\api-health-monitor\migrate_maintenance.py"

migration = '''import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_windows (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        repeat_type VARCHAR(20) DEFAULT \'once\',
        weekday INTEGER,
        day_of_month INTEGER,
        start_time VARCHAR(5) NOT NULL,
        end_time VARCHAR(5) NOT NULL,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        timezone VARCHAR(50) DEFAULT \'UTC\',
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_window_monitors (
        maintenance_window_id VARCHAR(36) NOT NULL REFERENCES maintenance_windows(id) ON DELETE CASCADE,
        monitor_id VARCHAR(36) NOT NULL REFERENCES monitors(id) ON DELETE CASCADE,
        PRIMARY KEY (maintenance_window_id, monitor_id)
    );
""")

conn.commit()
cur.close()
conn.close()
print("Migration done! maintenance_windows and maintenance_window_monitors tables created.")
'''

with open(MIGRATE_FILE, 'w', encoding='utf-8') as f:
    f.write(migration)
print("Migration script created!")
print("\nAll backend done!")
