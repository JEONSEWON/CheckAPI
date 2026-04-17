FILE = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\monitors\[id]\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Link 아이콘 import 추가
old_import = "  X\n} from 'lucide-react';"
new_import = "  X,\n  Link\n} from 'lucide-react';"
content = content.replace(old_import, new_import)

# 2. handleDelete 앞에 handleCopyStatusUrl 추가
old_fn = "  const handleDelete = async () => {"
new_fn = """  const handleCopyStatusUrl = () => {
    const url = `${window.location.origin}/status/${monitorId}`;
    navigator.clipboard.writeText(url);
    toast.success('Status page URL copied!');
  };

  const handleDelete = async () => {"""
content = content.replace(old_fn, new_fn)

# 3. Edit 버튼 앞에 Copy Status URL 버튼 추가
old_edit_btn = """            <button
              onClick={handleEdit}
              className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-900 dark:text-white"
            >
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </button>"""
new_edit_btn = """            <button
              onClick={handleCopyStatusUrl}
              className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-900 dark:text-white"
            >
              <Link className="h-4 w-4 mr-2" />
              Status Page
            </button>
            <button
              onClick={handleEdit}
              className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-900 dark:text-white"
            >
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </button>"""
content = content.replace(old_edit_btn, new_edit_btn)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("handleCopyStatusUrl:", "handleCopyStatusUrl" in content)
print("Status Page button:", "Status Page" in content)
print("Link icon:", "Link" in content)
