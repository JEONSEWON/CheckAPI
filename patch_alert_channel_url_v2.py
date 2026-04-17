FILE = r"C:\home\jeon\api-health-monitor\frontend\lib\api.ts"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

old_link = "    apiRequest(`/api/v1/monitors/${monitorId}/alert-channels/${channelId}`, {\n      method: 'POST',\n    }),"
new_link = "    apiRequest(`/api/v1/alert-channels/${channelId}/attach/${monitorId}`, {\n      method: 'POST',\n    }),"
content = content.replace(old_link, new_link)

old_unlink = "    apiRequest(`/api/v1/monitors/${monitorId}/alert-channels/${channelId}`, {\n      method: 'DELETE',\n    }),"
new_unlink = "    apiRequest(`/api/v1/alert-channels/${channelId}/detach/${monitorId}`, {\n      method: 'POST',\n    }),"
content = content.replace(old_unlink, new_unlink)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("attach URL:", "attach" in content)
print("detach URL:", "detach" in content)
