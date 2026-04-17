import re

# ── 1. models.py - use_regex 컬럼 추가 ──────────────────────────────────────
FILE_MODELS = r"C:\home\jeon\api-health-monitor\backend\app\models.py"

with open(FILE_MODELS, 'r', encoding='utf-8') as f:
    c = f.read()

old_model = "    keyword = Column(String(500))\n    keyword_present = Column(Boolean, default=True)"
new_model = "    keyword = Column(String(500))\n    keyword_present = Column(Boolean, default=True)\n    use_regex = Column(Boolean, default=False)"
c = c.replace(old_model, new_model)

with open(FILE_MODELS, 'w', encoding='utf-8') as f:
    f.write(c)

print("models.py done!", "use_regex" in c)


# ── 2. schemas.py - use_regex 필드 추가 ─────────────────────────────────────
FILE_SCHEMAS = r"C:\home\jeon\api-health-monitor\backend\app\schemas.py"

with open(FILE_SCHEMAS, 'r', encoding='utf-8') as f:
    c = f.read()

# MonitorCreate
old_create = "    keyword: Optional[str] = Field(None, max_length=500)\n    keyword_present: bool = Field(default=True)"
new_create = "    keyword: Optional[str] = Field(None, max_length=500)\n    keyword_present: bool = Field(default=True)\n    use_regex: bool = Field(default=False)"
c = c.replace(old_create, new_create)

# MonitorUpdate
old_update = "    keyword: Optional[str] = Field(None, max_length=500)\n    keyword_present: Optional[bool] = None\n    is_active: Optional[bool] = None"
new_update = "    keyword: Optional[str] = Field(None, max_length=500)\n    keyword_present: Optional[bool] = None\n    use_regex: Optional[bool] = None\n    is_active: Optional[bool] = None"
c = c.replace(old_update, new_update)

# MonitorResponse
old_response = "    keyword: Optional[str]\n    keyword_present: bool\n    is_active: bool"
new_response = "    keyword: Optional[str]\n    keyword_present: bool\n    use_regex: bool = False\n    is_active: bool"
c = c.replace(old_response, new_response)

with open(FILE_SCHEMAS, 'w', encoding='utf-8') as f:
    f.write(c)

print("schemas.py done!", c.count("use_regex"))


# ── 3. tasks.py - regex 검증 로직 ───────────────────────────────────────────
FILE_TASKS = r"C:\home\jeon\api-health-monitor\backend\app\tasks.py"

with open(FILE_TASKS, 'r', encoding='utf-8') as f:
    c = f.read()

# re import 추가 (없으면)
if "import re" not in c:
    c = "import re\n" + c

old_keyword = """            # Step 2: keyword check in response body (only if status code passed)
            if status == "up" and monitor.keyword:
                try:
                    body_text = response.text
                    keyword_found = monitor.keyword in body_text
                    if monitor.keyword_present and not keyword_found:
                        status = "degraded"
                        error_message = f"Keyword '{monitor.keyword}' not found in response body"
                    elif not monitor.keyword_present and keyword_found:
                        status = "degraded"
                        error_message = f"Keyword '{monitor.keyword}' found in response body (expected absent)"
                except Exception as e:
                    print(f"Keyword check error: {e}")"""

new_keyword = """            # Step 2: keyword/regex check in response body (only if status code passed)
            if status == "up" and monitor.keyword:
                try:
                    body_text = response.text
                    use_regex = getattr(monitor, 'use_regex', False)
                    if use_regex:
                        try:
                            keyword_found = bool(re.search(monitor.keyword, body_text))
                            pattern_label = f"Pattern '{monitor.keyword}'"
                        except re.error as regex_err:
                            keyword_found = False
                            pattern_label = f"Invalid regex '{monitor.keyword}'"
                    else:
                        keyword_found = monitor.keyword in body_text
                        pattern_label = f"Keyword '{monitor.keyword}'"
                    if monitor.keyword_present and not keyword_found:
                        status = "degraded"
                        error_message = f"{pattern_label} not found in response body"
                    elif not monitor.keyword_present and keyword_found:
                        status = "degraded"
                        error_message = f"{pattern_label} found in response body (expected absent)"
                except Exception as e:
                    print(f"Keyword check error: {e}")"""

c = c.replace(old_keyword, new_keyword)

with open(FILE_TASKS, 'w', encoding='utf-8') as f:
    f.write(c)

print("tasks.py done!", "use_regex" in c)


# ── 4. DB 마이그레이션 스크립트 생성 ─────────────────────────────────────────
FILE_MIGRATE = r"C:\home\jeon\api-health-monitor\migrate_add_use_regex.py"

migration = '''import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    ALTER TABLE monitors
    ADD COLUMN IF NOT EXISTS use_regex BOOLEAN DEFAULT FALSE;
""")

conn.commit()
cur.close()
conn.close()
print("Migration done! use_regex column added.")
'''

with open(FILE_MIGRATE, 'w', encoding='utf-8') as f:
    f.write(migration)

print("Migration script created!")
print("\nAll done! Summary:")
print("- models.py: use_regex column added")
print("- schemas.py: use_regex field in Create/Update/Response")
print("- tasks.py: regex matching logic")
print("- migrate_add_use_regex.py: DB migration script")
