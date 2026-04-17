import os

# ── 1. models.py - MonitorAssertion 모델 추가 ─────────────────────────────────
FILE_MODELS = r"C:\home\jeon\api-health-monitor\backend\app\models.py"

with open(FILE_MODELS, 'r', encoding='utf-8') as f:
    c = f.read()

assertion_model = '''

class MonitorAssertion(Base):
    """Assertion model - response validation rules per monitor"""
    __tablename__ = "monitor_assertions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    monitor_id = Column(String(36), ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False)
    assertion_type = Column(String(20), nullable=False, default="jsonpath")  # keyword, jsonpath
    path = Column(Text, nullable=True)           # JSON Path e.g. $.data.status
    operator = Column(String(20), nullable=False) # ==, !=, >, >=, <, <=, contains, not_contains, is_null, is_not_null, exists
    value = Column(JSON, nullable=True)           # expected value (string/number/bool/null)
    logic = Column(String(3), default="AND")      # AND / OR
    order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    monitor = relationship("Monitor", back_populates="assertions")
'''

c = c + assertion_model

# Monitor에 assertions relationship 추가
old_monitor_rel = "    maintenance_windows = relationship(\"MaintenanceWindow\", secondary=\"maintenance_window_monitors\", back_populates=\"monitors\")"
new_monitor_rel = """    maintenance_windows = relationship("MaintenanceWindow", secondary="maintenance_window_monitors", back_populates="monitors")
    assertions = relationship("MonitorAssertion", back_populates="monitor", cascade="all, delete-orphan", order_by="MonitorAssertion.order")"""
c = c.replace(old_monitor_rel, new_monitor_rel)

with open(FILE_MODELS, 'w', encoding='utf-8') as f:
    f.write(c)
print("models.py done!", "MonitorAssertion" in c)


# ── 2. schemas.py - Assertion 스키마 추가 ────────────────────────────────────
FILE_SCHEMAS = r"C:\home\jeon\api-health-monitor\backend\app\schemas.py"

with open(FILE_SCHEMAS, 'r', encoding='utf-8') as f:
    c = f.read()

assertion_schemas = '''

class AssertionCreate(BaseModel):
    assertion_type: str = Field(default="jsonpath", pattern="^(keyword|jsonpath)$")
    path: Optional[str] = None
    operator: str = Field(..., pattern="^(==|!=|>|>=|<|<=|contains|not_contains|is_null|is_not_null|exists)$")
    value: Optional[Any] = None
    logic: str = Field(default="AND", pattern="^(AND|OR)$")
    order: int = Field(default=0, ge=0)
    is_active: bool = True


class AssertionResponse(BaseModel):
    id: UUID
    assertion_type: str
    path: Optional[str]
    operator: str
    value: Optional[Any]
    logic: str
    order: int
    is_active: bool

    class Config:
        from_attributes = True


class AssertionTestRequest(BaseModel):
    response_body: str
    assertions: List[AssertionCreate]
'''

# Any import 추가
if "from typing import" in c:
    old_typing = "from typing import"
    first_line = c[c.find(old_typing):c.find('\n', c.find(old_typing))]
    if "Any" not in first_line:
        c = c.replace(first_line, first_line.rstrip() + ", Any", 1)

c = c + assertion_schemas

with open(FILE_SCHEMAS, 'w', encoding='utf-8') as f:
    f.write(c)
print("schemas.py done!", "AssertionCreate" in c)


# ── 3. assertions.py 라우터 생성 ─────────────────────────────────────────────
ROUTER_FILE = r"C:\home\jeon\api-health-monitor\backend\app\routers\assertions.py"

router_content = '''"""
Monitor Assertions API - JSON Path & Keyword validation rules
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Optional
import json

from app.database import get_db
from app.auth import get_current_user
from app.models import User, Monitor, MonitorAssertion
from app.schemas import AssertionCreate, AssertionResponse, AssertionTestRequest

router = APIRouter(prefix="/api/v1/monitors", tags=["Assertions"])

MAX_ASSERTIONS = 10


def evaluate_assertion(actual_values: list, operator: str, expected) -> bool:
    """Evaluate a single assertion against extracted JSON path values"""
    if operator == "exists":
        return len(actual_values) > 0

    if operator == "is_null":
        return all(v is None for v in actual_values) if actual_values else True

    if operator == "is_not_null":
        return all(v is not None for v in actual_values) if actual_values else False

    if not actual_values:
        return False

    actual = actual_values[0]

    # Auto-cast expected value
    if expected is not None and isinstance(actual, (int, float)) and isinstance(expected, str):
        try:
            expected = type(actual)(expected)
        except (ValueError, TypeError):
            pass
    elif expected is not None and isinstance(actual, bool) and isinstance(expected, str):
        expected = expected.lower() in ("true", "1", "yes")

    if operator == "==":
        return actual == expected
    elif operator == "!=":
        return actual != expected
    elif operator == ">":
        return actual > expected
    elif operator == ">=":
        return actual >= expected
    elif operator == "<":
        return actual < expected
    elif operator == "<=":
        return actual <= expected
    elif operator == "contains":
        return str(expected) in str(actual)
    elif operator == "not_contains":
        return str(expected) not in str(actual)
    return False


def run_assertions(response_body: str, assertions: list) -> dict:
    """Run all assertions against response body. Returns result dict."""
    if not assertions:
        return {"passed": True, "results": [], "error": None}

    try:
        try:
            response_json = json.loads(response_body)
        except json.JSONDecodeError:
            response_json = None
    except Exception:
        response_json = None

    results = []
    logic = assertions[0].logic if hasattr(assertions[0], 'logic') else (assertions[0].get('logic', 'AND') if isinstance(assertions[0], dict) else 'AND')

    for a in assertions:
        if isinstance(a, dict):
            atype = a.get('assertion_type', 'jsonpath')
            path = a.get('path')
            operator = a.get('operator')
            value = a.get('value')
        else:
            atype = getattr(a, 'assertion_type', 'jsonpath')
            path = getattr(a, 'path', None)
            operator = getattr(a, 'operator', None)
            value = getattr(a, 'value', None)

        if not getattr(a, 'is_active', True) if not isinstance(a, dict) else a.get('is_active', True):
            continue

        passed = False
        actual_display = None
        error = None

        try:
            if atype == "keyword":
                # Simple keyword check
                if operator in ("exists", "is_not_null"):
                    passed = path in response_body if path else False
                elif operator in ("is_null", "not_contains"):
                    passed = (path not in response_body) if path else True
                elif operator == "contains":
                    passed = (path in response_body) if path else False
                elif operator == "==":
                    passed = response_body == path
                else:
                    passed = path in response_body if path else False
                actual_display = "present" if path in response_body else "absent"

            elif atype == "jsonpath":
                if response_json is None:
                    passed = False
                    error = "Response is not valid JSON"
                else:
                    from jsonpath_ng import parse
                    from jsonpath_ng.exceptions import JsonPathParserError
                    try:
                        expr = parse(path)
                        matches = [m.value for m in expr.find(response_json)]
                        actual_display = matches[0] if matches else None
                        passed = evaluate_assertion(matches, operator, value)
                    except JsonPathParserError as e:
                        passed = False
                        error = f"Invalid JSON path: {str(e)}"

        except Exception as e:
            passed = False
            error = str(e)

        results.append({
            "path": path,
            "operator": operator,
            "expected": value,
            "actual": actual_display,
            "passed": passed,
            "error": error,
        })

    if not results:
        return {"passed": True, "results": [], "error": None}

    if logic == "OR":
        overall = any(r["passed"] for r in results)
    else:  # AND
        overall = all(r["passed"] for r in results)

    return {"passed": overall, "results": results, "error": None}


@router.get("/{monitor_id}/assertions", response_model=List[AssertionResponse])
def list_assertions(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    monitor = db.query(Monitor).filter(Monitor.id == monitor_id, Monitor.user_id == current_user.id).first()
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return monitor.assertions


@router.post("/{monitor_id}/assertions", response_model=List[AssertionResponse])
def save_assertions(
    monitor_id: str,
    assertions: List[AssertionCreate],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    monitor = db.query(Monitor).filter(Monitor.id == monitor_id, Monitor.user_id == current_user.id).first()
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")

    if len(assertions) > MAX_ASSERTIONS:
        raise HTTPException(status_code=400, detail=f"Maximum {MAX_ASSERTIONS} assertions allowed")

    # Replace all assertions
    db.query(MonitorAssertion).filter(MonitorAssertion.monitor_id == monitor_id).delete()

    new_assertions = []
    for i, a in enumerate(assertions):
        obj = MonitorAssertion(
            monitor_id=monitor_id,
            assertion_type=a.assertion_type,
            path=a.path,
            operator=a.operator,
            value=a.value,
            logic=a.logic,
            order=i,
            is_active=a.is_active,
        )
        db.add(obj)
        new_assertions.append(obj)

    db.commit()
    for obj in new_assertions:
        db.refresh(obj)
    return new_assertions


@router.post("/{monitor_id}/assertions/test")
def test_assertions(
    monitor_id: str,
    req: AssertionTestRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    monitor = db.query(Monitor).filter(Monitor.id == monitor_id, Monitor.user_id == current_user.id).first()
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")

    assertions_dicts = [a.dict() for a in req.assertions]
    result = run_assertions(req.response_body, req.assertions)
    return result
'''

with open(ROUTER_FILE, 'w', encoding='utf-8') as f:
    f.write(router_content)
print("assertions router created!")


# ── 4. tasks.py에 assertion 체크 로직 추가 ────────────────────────────────────
FILE_TASKS = r"C:\home\jeon\api-health-monitor\backend\app\tasks.py"

with open(FILE_TASKS, 'r', encoding='utf-8') as f:
    c = f.read()

old_keyword = "            # Step 2: keyword/regex check in response body (only if status code passed)"
new_assertion = '''            # Step 2: assertions check (keyword/regex/jsonpath)
            if status == "up":
                try:
                    from app.models import MonitorAssertion
                    from app.routers.assertions import run_assertions
                    assertions = db.query(MonitorAssertion).filter(
                        MonitorAssertion.monitor_id == monitor.id,
                        MonitorAssertion.is_active == True
                    ).order_by(MonitorAssertion.order).all()

                    if assertions:
                        result = run_assertions(response.text, assertions)
                        if not result["passed"]:
                            status = "degraded"
                            failed = [r for r in result["results"] if not r["passed"]]
                            if failed:
                                f = failed[0]
                                error_message = f"Assertion failed: {f['path']} {f['operator']} {f['expected']} (got: {f['actual']})"
                            else:
                                error_message = "Assertion failed"
                    elif monitor.keyword:
                        # Legacy keyword/regex fallback
                        pass
                except Exception as e:
                    print(f"Assertion check error: {e}")

            # Step 2b: legacy keyword/regex check (only if no assertions defined)
            ''' + old_keyword[old_keyword.find('#'):]

# legacy keyword 로직을 assertions 없을 때만 실행하도록
if old_keyword in c:
    c = c.replace(old_keyword, new_assertion)
    print("tasks.py assertion logic added!")
else:
    print("WARNING: tasks.py keyword section not found - manual check needed")

with open(FILE_TASKS, 'w', encoding='utf-8') as f:
    f.write(c)


# ── 5. main.py에 assertions router 등록 ──────────────────────────────────────
FILE_MAIN = r"C:\home\jeon\api-health-monitor\backend\app\main.py"

with open(FILE_MAIN, 'r', encoding='utf-8') as f:
    c = f.read()

if "assertions" not in c:
    old_import = "from app.routers import maintenance"
    new_import = "from app.routers import maintenance\nfrom app.routers import assertions"
    c = c.replace(old_import, new_import)

    old_include = "app.include_router(maintenance.router)"
    new_include = "app.include_router(maintenance.router)\napp.include_router(assertions.router)"
    c = c.replace(old_include, new_include)

    with open(FILE_MAIN, 'w', encoding='utf-8') as f:
        f.write(c)
    print("main.py updated!")
else:
    print("main.py already has assertions")


# ── 6. DB 마이그레이션 스크립트 생성 ─────────────────────────────────────────
MIGRATE_FILE = r"C:\home\jeon\api-health-monitor\migrate_assertions.py"

migration = '''import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS monitor_assertions (
        id VARCHAR(36) PRIMARY KEY,
        monitor_id VARCHAR(36) NOT NULL REFERENCES monitors(id) ON DELETE CASCADE,
        assertion_type VARCHAR(20) NOT NULL DEFAULT \'jsonpath\',
        path TEXT,
        operator VARCHAR(20) NOT NULL,
        value JSONB,
        logic VARCHAR(3) DEFAULT \'AND\',
        "order" INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW()
    );
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_assertions_monitor_id ON monitor_assertions(monitor_id);")

conn.commit()
cur.close()
conn.close()
print("Migration done! monitor_assertions table created.")
'''

with open(MIGRATE_FILE, 'w', encoding='utf-8') as f:
    f.write(migration)
print("Migration script created!")
print("\nAll backend done!")
