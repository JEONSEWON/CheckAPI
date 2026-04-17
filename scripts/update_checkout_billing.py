file_path = "backend/app/routers/subscriptions.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = '''@router.post("/checkout")
def create_checkout(
    plan: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create checkout session for plan upgrade
    
    Args:
        plan: Target plan (starter, pro, business)
    """
    if plan not in ["starter", "pro", "business"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan.\nMust be one of: starter, pro, business"
        )'''

new = '''@router.post("/checkout")
def create_checkout(
    plan: str,
    billing: str = "monthly",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create checkout session for plan upgrade

    Args:
        plan: Target plan (starter, pro, business)
        billing: Billing cycle (monthly, annual)
    """
    if plan not in ["starter", "pro", "business"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan.\nMust be one of: starter, pro, business"
        )
    if billing not in ["monthly", "annual"]:
        billing = "monthly"'''

if old in content:
    content = content.replace(old, new)
    # get_variant_id_for_plan 호출도 수정
    content = content.replace(
        "variant_id = get_variant_id_for_plan(plan)",
        "variant_id = get_variant_id_for_plan(plan, billing)"
    )
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ subscriptions.py 완료!")
else:
    print("❌ 못 찾음")
