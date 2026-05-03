"""
Audit logging helpers — fire-and-forget, never raise on failure.
"""
from sqlalchemy.orm import Session
from app.models import AuditLog


def log_action(
    db: Session,
    user_id: str,
    action: str,
    resource_type: str = None,
    resource_id: str = None,
    detail: dict = None,
) -> None:
    try:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            detail=detail,
        )
        db.add(entry)
        db.commit()
    except Exception as e:
        print(f"⚠️  audit log error (non-fatal): {e}")
        db.rollback()
