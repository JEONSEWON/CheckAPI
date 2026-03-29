"""
Monitor management routes: CRUD operations for monitors
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime, timedelta
from uuid import UUID

from app.database import get_db
from app.models import User, Monitor, Check, TeamMember
from app.schemas import (
    MonitorCreate,
    MonitorUpdate,
    MonitorResponse,
    CheckResponse,
    CheckListResponse,
    MessageResponse
)
from app.auth import get_current_user, get_user_by_api_key

def get_current_user_flexible(
    request: Request,
    db: Session = Depends(get_db)
):
    """JWT 토큰 또는 API 키로 인증"""
    api_key = request.headers.get("X-API-Key")
    if api_key:
        user = get_user_by_api_key(api_key, db)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API key")
        if user.plan != "business":
            raise HTTPException(status_code=403, detail="API access requires Business plan")
        return user
    # JWT 토큰 인증
    from app.auth import get_current_user
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    token = auth[7:]
    from app.auth import decode_token as verify_token
    from app.models import User
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


router = APIRouter(prefix="/monitors", tags=["Monitors"])


def get_effective_owner_id(current_user: User, db: Session) -> str:
    """팀 멤버인 경우 오너의 user_id 반환, 아니면 본인 id 반환"""
    membership = db.query(TeamMember).filter(
        TeamMember.member_id == current_user.id,
        TeamMember.status == "active"
    ).first()
    return membership.owner_id if membership else current_user.id


def get_effective_owner(current_user: User, db: Session) -> User:
    """팀 멤버인 경우 오너 User 객체 반환"""
    owner_id = get_effective_owner_id(current_user, db)
    if owner_id != current_user.id:
        return db.query(User).filter(User.id == owner_id).first()
    return current_user


# Plan limits
PLAN_LIMITS = {
    "free": {"max_monitors": 10, "min_interval": 300},  # 5 minutes
    "starter": {"max_monitors": 20, "min_interval": 60},  # 1 minute
    "pro": {"max_monitors": 100, "min_interval": 30},  # 30 seconds
    "business": {"max_monitors": -1, "min_interval": 10},  # unlimited, 10 seconds
}


def check_plan_limits(user: User, db: Session, creating_new: bool = False) -> None:
    """Check if user has reached their plan limits"""
    limits = PLAN_LIMITS.get(user.plan, PLAN_LIMITS["free"])
    
    if creating_new and limits["max_monitors"] > 0:
        current_count = db.query(Monitor).filter(Monitor.user_id == user.id).count()
        if current_count >= limits["max_monitors"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Monitor limit reached for {user.plan} plan. Upgrade to add more monitors."
            )


def validate_interval(user: User, interval: int) -> None:
    """Validate interval based on user's plan"""
    limits = PLAN_LIMITS.get(user.plan, PLAN_LIMITS["free"])
    
    if interval < limits["min_interval"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Minimum interval for {user.plan} plan is {limits['min_interval']} seconds. Upgrade for faster checks."
        )


@router.get("/", response_model=List[MonitorResponse])
def list_monitors(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    Get all monitors for the current user
    """
    owner_id = get_effective_owner_id(current_user, db)
    monitors = (
        db.query(Monitor)
        .filter(Monitor.user_id == owner_id)
        .order_by(desc(Monitor.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return monitors


@router.post("/", response_model=MonitorResponse, status_code=status.HTTP_201_CREATED)
def create_monitor(
    monitor_data: MonitorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new monitor
    """
    # Check plan limits
    check_plan_limits(current_user, db, creating_new=True)
    
    # Validate interval
    validate_interval(current_user, monitor_data.interval)
    
    # Create monitor
    new_monitor = Monitor(
        user_id=current_user.id,
        name=monitor_data.name,
        url=str(monitor_data.url),
        method=monitor_data.method,
        interval=monitor_data.interval,
        timeout=monitor_data.timeout,
        headers=monitor_data.headers,
        body=monitor_data.body,
        expected_status=monitor_data.expected_status,
        next_check_at=datetime.utcnow()  # Check immediately
    )
    
    db.add(new_monitor)
    db.commit()
    db.refresh(new_monitor)
    
    return new_monitor


@router.get("/{monitor_id}", response_model=MonitorResponse)
def get_monitor(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific monitor by ID
    """
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()
    
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found"
        )
    
    return monitor


@router.put("/{monitor_id}", response_model=MonitorResponse)
def update_monitor(
    monitor_id: str,
    monitor_data: MonitorUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a monitor
    """
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()
    
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found"
        )
    
    # Update fields
    update_data = monitor_data.model_dump(exclude_unset=True)
    
    # Validate interval if being updated
    if "interval" in update_data:
        validate_interval(current_user, update_data["interval"])
    
    # Convert URL to string if present
    if "url" in update_data:
        update_data["url"] = str(update_data["url"])
    
    for field, value in update_data.items():
        setattr(monitor, field, value)
    
    monitor.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(monitor)
    
    return monitor


@router.delete("/{monitor_id}", response_model=MessageResponse)
def delete_monitor(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a monitor
    """
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()
    
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found"
        )
    
    db.delete(monitor)
    db.commit()
    
    return {"message": "Monitor deleted successfully"}


@router.get("/{monitor_id}/checks", response_model=CheckListResponse)
def get_monitor_checks(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    hours: int = Query(24, ge=1, le=168)  # Last 24 hours by default, max 7 days
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
    since = datetime.utcnow() - timedelta(hours=hours)
    
    # Count total
    total = db.query(Check).filter(
        Check.monitor_id == monitor_id,
        Check.checked_at >= since
    ).count()
    
    # Get paginated checks
    checks = (
        db.query(Check)
        .filter(
            Check.monitor_id == monitor_id,
            Check.checked_at >= since
        )
        .order_by(desc(Check.checked_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    
    return {
        "checks": checks,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/{monitor_id}/pause", response_model=MessageResponse)
def pause_monitor(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Pause a monitor (set is_active to False)
    """
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()
    
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found"
        )
    
    monitor.is_active = False
    monitor.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Monitor paused"}


@router.post("/{monitor_id}/resume", response_model=MessageResponse)
def resume_monitor(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resume a paused monitor (set is_active to True)
    """
    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()
    
    if not monitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found"
        )
    
    monitor.is_active = True
    monitor.next_check_at = datetime.utcnow()  # Check immediately
    monitor.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Monitor resumed"}
