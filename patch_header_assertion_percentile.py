import os

# ── 1. schemas.py - header 타입 추가 ─────────────────────────────────────────
FILE_SCHEMAS = r"C:\home\jeon\api-health-monitor\backend\app\schemas.py"

with open(FILE_SCHEMAS, 'r', encoding='utf-8') as f:
    c = f.read()

old_type = 'assertion_type: str = Field(default="jsonpath", pattern="^(keyword|jsonpath)$")'
new_type = 'assertion_type: str = Field(default="jsonpath", pattern="^(keyword|jsonpath|header)$")'
c = c.replace(old_type, new_type)

with open(FILE_SCHEMAS, 'w', encoding='utf-8') as f:
    f.write(c)
print("schemas.py done!", "header" in c)


# ── 2. assertions.py - header 타입 처리 + run_assertions에 headers 파라미터 추가
FILE_ASSERTIONS = r"C:\home\jeon\api-health-monitor\backend\app\routers\assertions.py"

with open(FILE_ASSERTIONS, 'r', encoding='utf-8') as f:
    c = f.read()

# run_assertions 함수 시그니처에 headers 파라미터 추가
old_sig = "def run_assertions(response_body: str, assertions: list) -> dict:"
new_sig = "def run_assertions(response_body: str, assertions: list, response_headers: dict = None) -> dict:"
c = c.replace(old_sig, new_sig)

# header assertion 처리 추가 (jsonpath elif 뒤에)
old_jsonpath_end = """            except Exception as e:
                passed = False
                error = str(e)

        results.append({"""

new_jsonpath_end = """            elif atype == "header":
                if response_headers is None:
                    passed = False
                    error = "No headers available"
                else:
                    # path = header name (case-insensitive)
                    header_val = None
                    if path:
                        for k, v in response_headers.items():
                            if k.lower() == path.lower():
                                header_val = v
                                break
                    actual_display = header_val
                    if operator == "exists":
                        passed = header_val is not None
                    elif operator == "is_null":
                        passed = header_val is None
                    elif operator == "is_not_null":
                        passed = header_val is not None
                    else:
                        passed = evaluate_assertion(
                            [header_val] if header_val is not None else [],
                            operator,
                            value
                        )

            except Exception as e:
                passed = False
                error = str(e)

        results.append({"""

c = c.replace(old_jsonpath_end, new_jsonpath_end)

# AssertionTestRequest에 response_headers 추가
old_test_req = """class AssertionTestRequest(BaseModel):
    response_body: str
    assertions: List[AssertionCreate]"""

new_test_req = """class AssertionTestRequest(BaseModel):
    response_body: str
    assertions: List[AssertionCreate]
    response_headers: Optional[dict] = None"""

# schemas.py에 추가 (assertions.py에 직접 정의된 경우)
with open(FILE_SCHEMAS, 'r', encoding='utf-8') as f:
    sc = f.read()
sc = sc.replace(
    "class AssertionTestRequest(BaseModel):\n    response_body: str\n    assertions: List[AssertionCreate]",
    "class AssertionTestRequest(BaseModel):\n    response_body: str\n    assertions: List[AssertionCreate]\n    response_headers: Optional[dict] = None"
)
with open(FILE_SCHEMAS, 'w', encoding='utf-8') as f:
    f.write(sc)

# test endpoint에서 headers 전달
old_test_call = "    result = run_assertions(req.response_body, req.assertions)"
new_test_call = "    result = run_assertions(req.response_body, req.assertions, req.response_headers)"
c = c.replace(old_test_call, new_test_call)

with open(FILE_ASSERTIONS, 'w', encoding='utf-8') as f:
    f.write(c)
print("assertions.py done!", "header" in c)


# ── 3. tasks.py - check_single_monitor에서 header assertions 전달 ─────────────
FILE_TASKS = r"C:\home\jeon\api-health-monitor\backend\app\tasks.py"

with open(FILE_TASKS, 'r', encoding='utf-8') as f:
    c = f.read()

old_run = "                    result = run_assertions(response.text, assertions)"
new_run = "                    result = run_assertions(response.text, assertions, dict(response.headers))"
c = c.replace(old_run, new_run)

with open(FILE_TASKS, 'w', encoding='utf-8') as f:
    f.write(c)
print("tasks.py done!", "dict(response.headers)" in c)


# ── 4. analytics router에 percentile 엔드포인트 추가 ──────────────────────────
FILE_ANALYTICS = r"C:\home\jeon\api-health-monitor\backend\app\routers\analytics.py"

with open(FILE_ANALYTICS, 'r', encoding='utf-8') as f:
    c = f.read()

percentile_endpoint = '''

@router.get("/monitors/{monitor_id}/percentiles")
def get_response_time_percentiles(
    monitor_id: str,
    hours: int = Query(24, ge=1, le=720),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get response time percentiles (p50, p95, p99) for a monitor"""
    from app.models import Check, Monitor
    from datetime import timedelta
    import statistics

    monitor = db.query(Monitor).filter(
        Monitor.id == monitor_id,
        Monitor.user_id == current_user.id
    ).first()
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")

    since = datetime.utcnow() - timedelta(hours=hours)
    checks = db.query(Check).filter(
        Check.monitor_id == monitor_id,
        Check.checked_at >= since,
        Check.response_time.isnot(None),
        Check.status == "up"
    ).all()

    if not checks:
        return {"p50": None, "p95": None, "p99": None, "sample_size": 0}

    times = sorted([c.response_time for c in checks])
    n = len(times)

    def percentile(data, p):
        idx = int(len(data) * p / 100)
        return data[min(idx, len(data) - 1)]

    return {
        "p50": percentile(times, 50),
        "p95": percentile(times, 95),
        "p99": percentile(times, 99),
        "min": times[0],
        "max": times[-1],
        "avg": round(sum(times) / n),
        "sample_size": n,
        "hours": hours,
    }
'''

# 파일 끝에 추가
c = c + percentile_endpoint

with open(FILE_ANALYTICS, 'w', encoding='utf-8') as f:
    f.write(c)
print("analytics.py done!", "percentile" in c)


# ── 5. api.ts에 percentile API 추가 ──────────────────────────────────────────
FILE_API = r"C:\home\jeon\api-health-monitor\frontend\lib\api.ts"

with open(FILE_API, 'r', encoding='utf-8') as f:
    c = f.read()

old_analytics = "  incidents: (days: number = 7) =>\n    apiRequest(`/api/v1/analytics/incidents?days=${days}`),"
new_analytics = """  incidents: (days: number = 7) =>
    apiRequest(`/api/v1/analytics/incidents?days=${days}`),
  percentiles: (monitorId: string, hours: number = 24) =>
    apiRequest(`/api/v1/analytics/monitors/${monitorId}/percentiles?hours=${hours}`),"""
c = c.replace(old_analytics, new_analytics)

with open(FILE_API, 'w', encoding='utf-8') as f:
    f.write(c)
print("api.ts done!", "percentiles" in c)

print("\nAll done!")
