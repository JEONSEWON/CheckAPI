file_path = "backend/app/auth.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_length = len(content)

# APIKey 인증 함수 추가
api_key_auth = '''

import hashlib as _hashlib

def get_api_key_header(request) -> str | None:
    return request.headers.get("X-API-Key")


def get_user_by_api_key(api_key: str, db) -> "User | None":
    from app.models import APIKey
    key_hash = _hashlib.sha256(api_key.encode()).hexdigest()
    api_key_obj = db.query(APIKey).filter(
        APIKey.key_hash == key_hash,
        APIKey.is_active == True
    ).first()
    if not api_key_obj:
        return None
    # last_used_at 업데이트
    from datetime import datetime
    api_key_obj.last_used_at = datetime.utcnow()
    db.commit()
    return api_key_obj.user
'''

content = content.rstrip() + api_key_auth

if len(content) >= original_length:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ auth.py 완료!")
else:
    print("❌ 파일 잘림")
