file_path = "backend/app/alerts.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_length = len(content)

# SendGrid 이메일 함수를 Resend로 교체
old_func = '''def send_email_alert(channel_config: Dict[str, Any], monitor_name: str, monitor_url: str, 
                     new_status: str, old_status: str) -> bool:
    """
    Send email alert using SendGrid
    """
    if not settings.SENDGRID_API_KEY:
        print("⚠️  SendGrid API key not configured")
        return False
    
    email = channel_config.get("email")
    if not email:
        return False
    
    try:
        # SendGrid API
        url = "https://api.sendgrid.com/v3/mail/send"
        
        # Status emoji
        status_emoji = {
            "up": "✅",
            "down": "🔴",
            "degraded": "⚠️"
        }
        
        # Email content
        subject = f"{status_emoji.get(new_status, '🔔')} {monitor_name} is {new_status.upper()}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: {'#16a34a' if new_status == 'up' else '#dc2626'};">
                {status_emoji.get(new_status, '🔔')} Monitor Status Changed
            </h2>
            <p><strong>Monitor:</strong> {monitor_name}</p>
            <p><strong>URL:</strong> <a href="{monitor_url}">{monitor_url}</a></p>
            <p><strong>Status:</strong> {old_status.upper()} → <strong>{new_status.upper()}</strong></p>
            <p><strong>Time:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <hr>
            <p style="font-size: 12px; color: #666;">
                Sent by API Health Monitor
            </p>
        </body>
        </html>
        """
        
        payload = {
            "personalizations": [{
            "to": [{"email": email}],
                "subject": subject
            }],
            "from": {
                "email": settings.FROM_EMAIL,
                "name": "API Health Monitor"
            },
            "content": [{
                "type": "text/html",
                "value": html_content
            }]
        }
        
        headers = {
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 202:
            print(f"✉️  Email sent to {email}")
            return True
        else:
            print(f"❌ Email failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False'''

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
        status_emoji = {
            "up": "✅",
            "down": "🔴",
            "degraded": "⚠️"
        }

        subject = f"{status_emoji.get(new_status, '🔔')} {monitor_name} is {new_status.upper()}"
        status_color = "#16a34a" if new_status == "up" else "#dc2626"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: {status_color}; color: white; padding: 16px 24px; border-radius: 8px 8px 0 0;">
                <h2 style="margin: 0;">{status_emoji.get(new_status, '🔔')} Monitor Status Changed</h2>
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
                    Sent by <a href="https://checkapi.io" style="color: #16a34a;">CheckAPI</a> — API Monitoring
                </p>
            </div>
        </body>
        </html>
        """

        payload = {
            "from": "CheckAPI <noreply@checkapi.io>",
            "to": [email],
            "subject": subject,
            "html": html_content,
        }

        headers = {
            "Authorization": f"Bearer {resend_api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.resend.com/emails",
            json=payload,
            headers=headers,
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

if old_func in content:
    content = content.replace(old_func, new_func)
    print("✅ SendGrid → Resend 교체 완료!")
else:
    print("❌ 못 찾음 — 수동 확인 필요")

if len(content) >= original_length - 100:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ 저장 완료!")
else:
    print("❌ 파일 잘림 감지 — 저장 안 함")
