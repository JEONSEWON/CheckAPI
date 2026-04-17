"""
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


def run_assertions(response_body: str, assertions: list, response_headers: dict = None) -> dict:
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

            elif atype == "header":
                headers = response_headers or {}
                # Case-insensitive header lookup
                header_val = next(
                    (v for k, v in headers.items() if k.lower() == (path or '').lower()),
                    None
                )
                actual_display = header_val
                passed = evaluate_assertion([header_val] if header_val is not None else [], operator, value)

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
    result = run_assertions(req.response_body, req.assertions, req.response_headers)
    return result
