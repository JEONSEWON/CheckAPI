FILE = r"C:\home\jeon\api-health-monitor\frontend\lib\api.ts"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

old_link = """  linkToMonitor: (monitorId: string, channelId: string) =>
    apiRequest(`/api/v1/monitors/${monitorId}/alert-channels/${channelId}`, {
      method: 'POST',
    }),
  unlinkFromMonitor: (monitorId: string, channelId: string) =>
    apiRequest(`/api/v1/monitors/${monitorId}/alert-channels/${channelId}`, {
      method: 'DELETE',
    }),"""

new_link = """  linkToMonitor: (monitorId: string, channelId: string) =>
    apiRequest(`/api/v1/alert-channels/${channelId}/attach/${monitorId}`, {
      method: 'POST',
    }),
  unlinkFromMonitor: (monitorId: string, channelId: string) =>
    apiRequest(`/api/v1/alert-channels/${channelId}/detach/${monitorId}`, {
      method: 'POST',
    }),"""

content = content.replace(old_link, new_link)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("attach URL:", "attach" in content)
print("detach URL:", "detach" in content)
