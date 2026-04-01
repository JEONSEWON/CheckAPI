"""
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
