"""
API Keys management routes - Business plan feature
"""

import secrets
import hashlib
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import User, APIKey
from app.auth import get_current_user

router = APIRouter(prefix="/api-keys", tags=["API Keys"])


def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def require_business_plan(user: User):
    if user.plan not in ["business"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API access is available on Business plan only"
        )


@router.get("/")
def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_business_plan(current_user)
    keys = db.query(APIKey).filter(
        APIKey.user_id == current_user.id,
        APIKey.is_active == True
    ).all()
    return [
        {
            "id": k.id,
            "name": k.name,
            "key_prefix": k.key_prefix,
            "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None,
            "created_at": k.created_at.isoformat(),
        }
        for k in keys
    ]


@router.post("/")
def create_api_key(
    name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_business_plan(current_user)

    # 최대 5개 제한
    count = db.query(APIKey).filter(
        APIKey.user_id == current_user.id,
        APIKey.is_active == True
    ).count()
    if count >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 API keys allowed"
        )

    # 키 생성: ck_live_xxxxxxxxxxxx
    raw_key = f"ck_live_{secrets.token_urlsafe(32)}"
    prefix = raw_key[:8]

    api_key = APIKey(
        user_id=current_user.id,
        name=name,
        key_hash=hash_key(raw_key),
        key_prefix=prefix,
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {
        "id": api_key.id,
        "name": api_key.name,
        "key": raw_key,  # 한 번만 반환
        "key_prefix": prefix,
        "created_at": api_key.created_at.isoformat(),
        "message": "Save this key — it won't be shown again."
    }


@router.delete("/{key_id}")
def delete_api_key(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_business_plan(current_user)

    key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == current_user.id
    ).first()

    if not key:
        raise HTTPException(status_code=404, detail="API key not found")

    key.is_active = False
    db.commit()
    return {"message": "API key deleted"}
