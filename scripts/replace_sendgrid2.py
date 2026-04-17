file_path = "backend/app/alerts.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# send_email_alert 함수 전체를 찾아서 교체
start = content.find("def send_email_alert(")
# 다음 함수 시작 찾기
end = content.find("\ndef send_slack_alert(")

if start == -1 or end == -1:
    print("❌ 함수 경계 못 찾음")
else:
    old_func = content[start:end]
    print("현재 함수 첫 3줄:")
    print('\n'.join(old_func.split('\n')[:3]))

    new_func = '''def send_email_alert(channel_config: Dict[str, Any], monitor_name: str, monitor_url: str,
                     new_status: str, old_status: str) -> bool:
    """
    Send email alert using Resend
    """
    resend_api_key = settings.RESEND_API_KEY
    if not resend_api_key:
        print("⚠️  Resend API key not configured")
        return False

    email = channel_config.get("email")
    if not email:
        return False

    try:
        status_emoji = {"up": "✅", "down": "🔴", "degraded": "⚠️"}
        subject = f"{status_emoji.get(new_status, '🔔')} {monitor_name} is {new_status.upper()}"
        status_color = "#16a34a" if new_status == "up" else "#dc2626"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: {status_color}; color: white; padding: 16px 24px; border-radius: 8px 8px 0 0;">
                <h2 style="margin: 0;">{status_emoji.get(new_status, "🔔")} Monitor Status Changed</h2>
            </div>
            <div style="border: 1px solid #e5e7eb; border-top: none; padding: 24px; border-radius: 0 0 8px 8px;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td style="padding: 8px 0; color: #6b7280;">Monitor</td><td style="padding: 8px 0; font-weight: bold;">{monitor_name}</td></tr>
                    <tr><td style="padding: 8px 0; color: #6b7280;">URL</td><td style="padding: 8px 0;"><a href="{monitor_url}" style="color: #16a34a;">{monitor_url}</a></td></tr>
                    <tr><td style="padding: 8px 0; color: #6b7280;">Status</td><td style="padding: 8px 0;">{old_status.upper()} → <strong style="color: {status_color};">{new_status.upper()}</strong></td></tr>
                    <tr><td style="padding: 8px 0; color: #6b7280;">Time</td><td style="padding: 8px 0;">{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}</td></tr>
                </table>
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                <p style="font-size: 12px; color: #9ca3af; margin: 0;">
                    Sent by <a href="https://checkapi.io" style="color: #16a34a;">CheckAPI</a>
                </p>
            </div>
        </body>
        </html>
        """

        response = requests.post(
            "https://api.resend.com/emails",
            json={
                "from": "CheckAPI <noreply@checkapi.io>",
                "to": [email],
                "subject": subject,
                "html": html_content,
            },
            headers={
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json"
            },
            timeout=10
        )

        if response.status_code == 200:
            print(f"✉️  Email sent to {email}")
            return True
        else:
            print(f"❌ Email failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False'''

    content = content[:start] + new_func + content[end:]

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ alerts.py Resend 교체 완료!")
