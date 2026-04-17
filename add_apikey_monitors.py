file_path = "backend/app/routers/monitors.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_length = len(content)

# get_current_user import에 추가
old_import = "from app.auth import get_current_user"
new_import = "from app.auth import get_current_user, get_user_by_api_key"

content = content.replace(old_import, new_import)

# Request import 추가
old_fastapi = "from fastapi import APIRouter, Depends, HTTPException, status"
new_fastapi = "from fastapi import APIRouter, Depends, HTTPException, status, Request"

content = content.replace(old_fastapi, new_fastapi)

# get_current_user_or_api_key 의존성 함수 추가 (라우터 정의 바로 위)
router_def = 'router = APIRouter(prefix="/monitors"'
new_dep = '''def get_current_user_flexible(
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
    from app.auth import verify_token
    from app.models import User
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


'''

if router_def in content:
    content = content.replace(router_def, new_dep + router_def)
    print("✅ flexible auth 함수 추가 완료!")
else:
    print("❌ router 정의 못 찾음")

if len(content) >= original_length:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ monitors.py 완료!")
else:
    print("❌ 파일 잘림")
