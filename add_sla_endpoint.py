file_path = "backend/app/routers/analytics.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_length = len(content)

sla_endpoint = '''

@router.get("/sla")
def get_sla_report(
    months: int = Query(3, ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get SLA report for all monitors - Business plan feature
    Returns monthly uptime, downtime, incidents per monitor
    """
    if current_user.plan not in ["business", "pro"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="SLA reports are available on Pro and Business plans"
        )

    monitors = db.query(Monitor).filter(
        Monitor.user_id == current_user.id,
        Monitor.is_active == True
    ).all()

    report = []

    for monitor in monitors:
        monthly_stats = []

        for month_offset in range(months - 1, -1, -1):
            # 월 시작/끝 계산
            now = datetime.utcnow()
            first_of_month = (now.replace(day=1) - timedelta(days=month_offset * 30)).replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            if first_of_month.month == 12:
                last_of_month = first_of_month.replace(year=first_of_month.year + 1, month=1) - timedelta(seconds=1)
            else:
                last_of_month = first_of_month.replace(month=first_of_month.month + 1) - timedelta(seconds=1)

            checks = db.query(Check).filter(
                Check.monitor_id == monitor.id,
                Check.checked_at >= first_of_month,
                Check.checked_at <= last_of_month
            ).all()

            if not checks:
                monthly_stats.append({
                    "month": first_of_month.strftime("%Y-%m"),
                    "uptime_percentage": None,
                    "total_checks": 0,
                    "downtime_minutes": 0,
                    "incidents": 0,
                    "avg_response_time": 0,
                })
                continue

            total = len(checks)
            up_count = sum(1 for c in checks if c.status == "up")
            uptime_pct = round((up_count / total) * 100, 3)

            # 다운타임 계산
            downtime_seconds = 0
            in_incident = False
            incident_start = None
            incidents = 0

            for c in sorted(checks, key=lambda x: x.checked_at):
                if c.status in ["down", "degraded"] and not in_incident:
                    in_incident = True
                    incident_start = c.checked_at
                    incidents += 1
                elif c.status == "up" and in_incident:
                    in_incident = False
                    if incident_start:
                        downtime_seconds += (c.checked_at - incident_start).total_seconds()

            if in_incident and incident_start:
                downtime_seconds += (last_of_month - incident_start).total_seconds()

            response_times = [c.response_time for c in checks if c.response_time]
            avg_response = int(sum(response_times) / len(response_times)) if response_times else 0

            monthly_stats.append({
                "month": first_of_month.strftime("%Y-%m"),
                "uptime_percentage": uptime_pct,
                "total_checks": total,
                "downtime_minutes": round(downtime_seconds / 60, 1),
                "incidents": incidents,
                "avg_response_time": avg_response,
            })

        # 전체 평균
        valid_months = [m for m in monthly_stats if m["uptime_percentage"] is not None]
        overall_uptime = round(
            sum(m["uptime_percentage"] for m in valid_months) / len(valid_months), 3
        ) if valid_months else None

        report.append({
            "monitor_id": str(monitor.id),
            "monitor_name": monitor.name,
            "monitor_url": monitor.url,
            "overall_uptime": overall_uptime,
            "monthly": monthly_stats,
        })

    return {
        "period_months": months,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "monitors": report,
    }
'''

content = content.rstrip() + sla_endpoint

if len(content) >= original_length:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ analytics.py SLA 엔드포인트 추가 완료!")
else:
    print("❌ 파일 잘림")
