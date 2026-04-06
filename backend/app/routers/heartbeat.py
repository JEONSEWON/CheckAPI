"""
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
