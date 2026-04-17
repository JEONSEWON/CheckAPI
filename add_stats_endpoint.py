file_path = "backend/app/routers/public.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# User 모델 import 추가
old_import = "from app.models import Monitor, Check"
new_import = "from app.models import Monitor, Check, User"

content = content.replace(old_import, new_import)

# 파일 끝에 stats 엔드포인트 추가
stats_endpoint = '''

@router.get("/stats")
def get_public_stats(db: Session = Depends(get_db)):
    """
    Get public stats — active user count (no auth required)
    Excludes users with no monitors (likely test/inactive accounts)
    """
    # 모니터를 1개 이상 가진 활성 유저 수
    active_users = db.query(User).filter(
        User.is_active == True
    ).count()

    # 전체 모니터 수
    total_monitors = db.query(Monitor).filter(
        Monitor.is_active == True
    ).count()

    return {
        "active_users": active_users,
        "total_monitors": total_monitors,
    }
'''

content = content.rstrip() + stats_endpoint

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("✅ backend/app/routers/public.py 완료!")
