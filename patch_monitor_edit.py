import re

FILE = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\monitors\[id]\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. useState import 뒤에 useRef 없으면 유지, 기존 import 확인
# Edit 모달 state 추가 - linkedChannels useState 바로 아래에 삽입
old_state = "  const [linkedChannels, setLinkedChannels] = useState<any[]>([]);"
new_state = """  const [linkedChannels, setLinkedChannels] = useState<any[]>([]);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editForm, setEditForm] = useState<any>(null);
  const [editLoading, setEditLoading] = useState(false);"""

content = content.replace(old_state, new_state)

# 2. handleDelete 함수 앞에 handleEdit 함수 추가
old_delete = "  const handleDelete = async () => {"
new_edit_and_delete = """  const handleEdit = () => {
    setEditForm({
      name: monitor.name,
      url: monitor.url,
      method: monitor.method,
      interval: monitor.interval,
      timeout: monitor.timeout,
      expected_status: monitor.expected_status,
      keyword: monitor.keyword || '',
      keyword_present: monitor.keyword_present ?? true,
    });
    setShowEditModal(true);
  };

  const handleEditSubmit = async () => {
    setEditLoading(true);
    try {
      const payload: any = {
        name: editForm.name,
        url: editForm.url,
        method: editForm.method,
        interval: Number(editForm.interval),
        timeout: Number(editForm.timeout),
        expected_status: Number(editForm.expected_status),
      };
      if (editForm.keyword) {
        payload.keyword = editForm.keyword;
        payload.keyword_present = editForm.keyword_present;
      } else {
        payload.keyword = null;
        payload.keyword_present = true;
      }
      await monitorsAPI.update(monitorId, payload);
      toast.success('Monitor updated!');
      setShowEditModal(false);
      loadData();
    } catch (error) {
      toast.error('Failed to update monitor');
    } finally {
      setEditLoading(false);
    }
  };

  const handleDelete = async () => {"""

content = content.replace(old_delete, new_edit_and_delete)

# 3. Edit 버튼에 onClick 핸들러 추가 (기존 Edit 버튼 찾기)
# 현재 Edit 버튼이 있는지 확인 후 추가 - 헤더 버튼 영역에 Edit 버튼 삽입
# Delete 버튼 앞에 Edit 버튼 추가
old_delete_btn = """            <button
              onClick={handleDelete}
              className="flex items-center px-4 py-2 border border-red-300 dark:border-red-800 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-50 dark:hover:bg-red-900 transition"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Delete
            </button>"""

new_delete_btn = """            <button
              onClick={handleEdit}
              className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-900 dark:text-white"
            >
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="flex items-center px-4 py-2 border border-red-300 dark:border-red-800 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-50 dark:hover:bg-red-900 transition"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Delete
            </button>"""

content = content.replace(old_delete_btn, new_delete_btn)

# 4. </DashboardLayout> 닫기 태그 바로 앞에 Edit 모달 삽입
old_close = "    </DashboardLayout>\n  );\n}"
new_close = """      {/* Edit Modal */}
      {showEditModal && editForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Edit Monitor</h2>
              <button
                onClick={() => setShowEditModal(false)}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition"
              >
                <X className="h-5 w-5 text-gray-500" />
              </button>
            </div>
            <div className="px-6 py-4 space-y-4">
              {/* Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Name</label>
                <input
                  type="text"
                  value={editForm.name}
                  onChange={e => setEditForm({ ...editForm, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
              {/* URL */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">URL</label>
                <input
                  type="url"
                  value={editForm.url}
                  onChange={e => setEditForm({ ...editForm, url: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
              {/* Method + Expected Status */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Method</label>
                  <select
                    value={editForm.method}
                    onChange={e => setEditForm({ ...editForm, method: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    {['GET','POST','PUT','DELETE','HEAD','OPTIONS','PATCH'].map(m => (
                      <option key={m} value={m}>{m}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Expected Status</label>
                  <input
                    type="number"
                    value={editForm.expected_status}
                    onChange={e => setEditForm({ ...editForm, expected_status: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                </div>
              </div>
              {/* Interval + Timeout */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Interval (seconds)</label>
                  <select
                    value={editForm.interval}
                    onChange={e => setEditForm({ ...editForm, interval: Number(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    <option value={60}>1 min</option>
                    <option value={300}>5 min</option>
                    <option value={600}>10 min</option>
                    <option value={1800}>30 min</option>
                    <option value={3600}>60 min</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Timeout (seconds)</label>
                  <input
                    type="number"
                    value={editForm.timeout}
                    min={5}
                    max={120}
                    onChange={e => setEditForm({ ...editForm, timeout: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                </div>
              </div>
              {/* Keyword (Silent Failure Detection) */}
              <div className="border border-orange-200 dark:border-orange-800 rounded-lg p-3 bg-orange-50 dark:bg-orange-950">
                <label className="block text-sm font-medium text-orange-700 dark:text-orange-300 mb-1">
                  Silent Failure Detection (optional)
                </label>
                <input
                  type="text"
                  placeholder="Keyword to check in response body"
                  value={editForm.keyword}
                  onChange={e => setEditForm({ ...editForm, keyword: e.target.value })}
                  className="w-full px-3 py-2 border border-orange-300 dark:border-orange-700 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-orange-500 mb-2"
                />
                {editForm.keyword && (
                  <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={editForm.keyword_present}
                      onChange={e => setEditForm({ ...editForm, keyword_present: e.target.checked })}
                      className="rounded"
                    />
                    Keyword should be <strong>present</strong> (uncheck = should be absent)
                  </label>
                )}
              </div>
            </div>
            <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3">
              <button
                onClick={() => setShowEditModal(false)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-900 dark:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleEditSubmit}
                disabled={editLoading}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50"
              >
                {editLoading ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}"""

content = content.replace(old_close, new_close)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Checking replacements...")
print("showEditModal:", "showEditModal" in content)
print("handleEdit:", "handleEdit" in content)
print("handleEditSubmit:", "handleEditSubmit" in content)
print("Edit Modal JSX:", "Edit Monitor" in content)
print("Edit button onClick:", "onClick={handleEdit}" in content)
