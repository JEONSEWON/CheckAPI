FILE = r"C:\home\jeon\api-health-monitor\frontend\app\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "coming soon" in line and "JSON field" in line:
        print(f"Found at line {i+1}: {repr(line[:80])}")
        lines[i] = lines[i].replace(
            "['Keyword match (present / absent)', 'Regex pattern matching', 'JSON field assertion (coming soon)'].map((f, i) => (",
            "['Keyword match (present / absent)', 'Regex pattern matching', 'JSON Path assertions (up to 10)', 'Header assertion (Content-Type, etc.)'].map((f, i) => ("
        )
        print(f"Replaced!")
        break

    if "color: i === 2 ? '#334155' : '#94a3b8'" in line:
        lines[i] = lines[i].replace(
            "color: i === 2 ? '#334155' : '#94a3b8'",
            "color: '#94a3b8'"
        ).replace(
            "color: i === 2 ? '#334155' : '#00e5b4'",
            "color: '#00e5b4'"
        )

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

content = ''.join(lines)
print("coming soon removed:", "coming soon" not in content)
print("JSON Path added:", "JSON Path assertions" in content)
print("Header assertion:", "Header assertion" in content)
