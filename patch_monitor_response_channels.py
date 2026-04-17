FILE = r"C:\home\jeon\api-health-monitor\backend\app\schemas.py"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# AlertChannelResponse 간단 버전 추가 (순환참조 방지용)
old_monitor_response = """class MonitorResponse(BaseModel):
    \"\"\"Monitor response\"\"\"
    id: UUID
    name: str
    url: str
    method: str
    interval: int
    timeout: int
    headers: Optional[Dict[str, str]]
    body: Optional[str]
    expected_status: int
    keyword: Optional[str]
    keyword_present: bool
    is_active: bool
    last_status: Optional[str]
    last_checked_at: Optional[datetime]
    next_check_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime"""

new_monitor_response = """class AlertChannelBrief(BaseModel):
    \"\"\"Brief alert channel info for monitor response\"\"\"
    id: UUID
    type: str
    config: Dict[str, str]
    is_active: bool

    class Config:
        from_attributes = True


class MonitorResponse(BaseModel):
    \"\"\"Monitor response\"\"\"
    id: UUID
    name: str
    url: str
    method: str
    interval: int
    timeout: int
    headers: Optional[Dict[str, str]]
    body: Optional[str]
    expected_status: int
    keyword: Optional[str]
    keyword_present: bool
    is_active: bool
    last_status: Optional[str]
    last_checked_at: Optional[datetime]
    next_check_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    alert_channels: List[AlertChannelBrief] = []"""

content = content.replace(old_monitor_response, new_monitor_response)

# List import 확인 - 이미 있으면 스킵
if "from typing import" in content and "List" not in content.split("from typing import")[1].split("\n")[0]:
    content = content.replace("from typing import", "from typing import List, ", 1)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("AlertChannelBrief:", "AlertChannelBrief" in content)
print("alert_channels field:", "alert_channels: List[AlertChannelBrief]" in content)
