file_path = "backend/app/database.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = '''# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True if not settings.DATABASE_URL.startswith("sqlite") else False,
)'''

new = '''# Create engine
is_postgres = not settings.DATABASE_URL.startswith("sqlite")
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=is_postgres,
    pool_recycle=300 if is_postgres else -1,      # 5분마다 연결 갱신
    pool_size=5 if is_postgres else 5,
    max_overflow=10 if is_postgres else 0,
)'''

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
else:
    print("❌ 못 찾음")
