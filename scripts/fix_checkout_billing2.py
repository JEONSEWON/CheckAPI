file_path = "backend/app/routers/subscriptions.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = '''def create_checkout(
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
            det'''

# 더 넓게 찾기
idx = content.find('def create_checkout(')
end = content.find('variant_id = get_variant_id_for_plan(plan)', idx)

if idx == -1:
    print("❌ create_checkout 못 찾음")
else:
    old_block = content[idx:end + len('variant_id = get_variant_id_for_plan(plan)')]
    new_block = '''def create_checkout(
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
            detail="Invalid plan. Must be one of: starter, pro, business"
        )
    if billing not in ["monthly", "annual"]:
        billing = "monthly"

    # Check if user already has an active subscription
    existing_sub = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()

    if existing_sub and existing_sub.plan == plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You are already on the {plan} plan"
        )

    # Get variant ID for plan
    variant_id = get_variant_id_for_plan(plan, billing)'''

    content = content[:idx] + new_block + content[end + len('variant_id = get_variant_id_for_plan(plan)'):]

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ subscriptions.py 완료!")
