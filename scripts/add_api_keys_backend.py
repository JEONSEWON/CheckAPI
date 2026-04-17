import os

# ============================================================
# 1. models.py에 APIKey 모델 추가
# ============================================================
models_path = "backend/app/models.py"
with open(models_path, "r", encoding="utf-8") as f:
    content = f.read()

# User 모델에 api_keys relationship 추가
old_user_rel = "    subscription = relationship(\"Subscription\", back_populates=\"user\", uselist=False)"
new_user_rel = "    subscription = relationship(\"Subscription\", back_populates=\"user\", uselist=False)\n    api_keys = relationship(\"APIKey\", back_populates=\"user\", cascade=\"all, delete-orphan\")"
content = content.replace(old_user_rel, new_user_rel)

# APIKey 모델 추가
api_key_model = '''

class APIKey(Base):
    """API Key model - for Business plan programmatic access"""
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True)
    key_prefix = Column(String(10), nullable=False)
    last_used_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="api_keys")
'''

content = content.rstrip() + api_key_model

with open(models_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("✅ models.py 완료!")

# ============================================================
# 2. api_keys router 생성
# ============================================================
api_keys_router = '''"""
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
    prefix = raw_key[:12]

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
        "message": "Save this key — it won\'t be shown again."
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
'''

with open("backend/app/routers/api_keys.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(api_keys_router)
print("✅ api_keys.py router 완료!")

# ============================================================
# 3. main.py에 api_keys 라우터 등록
# ============================================================
main_path = "backend/app/main.py"
with open(main_path, "r", encoding="utf-8") as f:
    main_content = f.read()

old_import = "from app.routers import monitors, alert_channels, subscriptions, public, analytics, teams"
new_import = "from app.routers import monitors, alert_channels, subscriptions, public, analytics, teams, api_keys"

old_include = "app.include_router(teams.router, prefix=\"/api/v1\")"
new_include = "app.include_router(teams.router, prefix=\"/api/v1\")\napp.include_router(api_keys.router, prefix=\"/api/v1\")"

main_content = main_content.replace(old_import, new_import)
main_content = main_content.replace(old_include, new_include)

with open(main_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(main_content)
print("✅ main.py 완료!")

print("\n모든 백엔드 작업 완료!")
