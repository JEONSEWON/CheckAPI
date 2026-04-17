file_path = "backend/app/routers/public.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# stats 엔드포인트 블록 추출 후 제거
stats_block = '''

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

# 파일 끝에서 제거
content = content.replace(stats_block, '')

# /status/{monitor_id} 라우터 앞에 삽입
insert_before = '@router.get("/status/{monitor_id}")'
idx = content.find(insert_before)

if idx == -1:
    print("❌ status 라우터 못 찾음")
else:
    content = content[:idx] + stats_block.lstrip('\n') + '\n' + content[idx:]
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ stats 엔드포인트 순서 수정 완료!")
