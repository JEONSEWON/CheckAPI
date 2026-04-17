import os

# ── 1. api.ts에 maintenanceAPI 추가 ──────────────────────────────────────────
FILE_API = r"C:\home\jeon\api-health-monitor\frontend\lib\api.ts"

with open(FILE_API, 'r', encoding='utf-8') as f:
    c = f.read()

maintenance_api = '''
// Maintenance Windows API
export const maintenanceAPI = {
  list: () => apiRequest('/api/v1/maintenance/'),
  create: (data: any) => apiRequest('/api/v1/maintenance/', { method: 'POST', body: JSON.stringify(data) }),
  toggle: (id: string) => apiRequest(`/api/v1/maintenance/${id}/toggle`, { method: 'PATCH' }),
  delete: (id: string) => apiRequest(`/api/v1/maintenance/${id}`, { method: 'DELETE' }),
};
'''

# export default 앞에 추가
old_export = "export const monitors = monitorsAPI;"
c = c.replace(old_export, maintenance_api + "\n" + old_export)

with open(FILE_API, 'w', encoding='utf-8') as f:
    f.write(c)

print("api.ts done!", "maintenanceAPI" in c)


# ── 2. Maintenance Window 페이지 생성 ────────────────────────────────────────
PAGE_DIR = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\maintenance"
os.makedirs(PAGE_DIR, exist_ok=True)

page_content = r"""'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import { maintenanceAPI, monitorsAPI } from '@/lib/api';
import { Clock, Plus, Trash2, Power, X } from 'lucide-react';
import toast from 'react-hot-toast';

const WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const REPEAT_TYPES = [
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
  { value: 'once', label: 'One-time' },
];

const DEFAULT_FORM = {
  name: '',
  repeat_type: 'weekly',
  weekday: 0,
  day_of_month: 1,
  start_time: '02:00',
  end_time: '04:00',
  start_date: '',
  end_date: '',
  timezone: 'Asia/Seoul',
  monitor_ids: [] as string[],
};

export default function MaintenancePage() {
  const [windows, setWindows] = useState<any[]>([]);
  const [monitors, setMonitors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ ...DEFAULT_FORM });
  const [saving, setSaving] = useState(false);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const [wins, mons] = await Promise.all([maintenanceAPI.list(), monitorsAPI.list()]);
      setWindows(wins);
      setMonitors(mons);
    } catch {
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!form.name || !form.start_time || !form.end_time) {
      toast.error('Name and times are required');
      return;
    }
    setSaving(true);
    try {
      const payload: any = {
        name: form.name,
        repeat_type: form.repeat_type,
        start_time: form.start_time,
        end_time: form.end_time,
        timezone: form.timezone,
        monitor_ids: form.monitor_ids,
      };
      if (form.repeat_type === 'weekly') payload.weekday = form.weekday;
      if (form.repeat_type === 'monthly') payload.day_of_month = form.day_of_month;
      if (form.repeat_type === 'once') {
        payload.start_date = form.start_date ? new Date(form.start_date).toISOString() : null;
        payload.end_date = form.end_date ? new Date(form.end_date).toISOString() : null;
      }
      await maintenanceAPI.create(payload);
      toast.success('Maintenance window created!');
      setShowModal(false);
      setForm({ ...DEFAULT_FORM });
      loadData();
    } catch (e: any) {
      toast.error(e.message || 'Failed to create');
    } finally {
      setSaving(false);
    }
  };

  const handleToggle = async (id: string) => {
    try {
      await maintenanceAPI.toggle(id);
      loadData();
    } catch { toast.error('Failed to toggle'); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this maintenance window?')) return;
    try {
      await maintenanceAPI.delete(id);
      toast.success('Deleted');
      loadData();
    } catch { toast.error('Failed to delete'); }
  };

  const formatSchedule = (w: any) => {
    if (w.repeat_type === 'daily') return `Daily ${w.start_time}–${w.end_time}`;
    if (w.repeat_type === 'weekly') return `Every ${WEEKDAYS[w.weekday]} ${w.start_time}–${w.end_time}`;
    if (w.repeat_type === 'monthly') return `Monthly day ${w.day_of_month}, ${w.start_time}–${w.end_time}`;
    if (w.repeat_type === 'once') return `One-time ${w.start_time}–${w.end_time}`;
    return '';
  };

  if (loading) return (
    <DashboardLayout>
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600" />
      </div>
    </DashboardLayout>
  );

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Maintenance Windows</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Suppress alerts during scheduled maintenance</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Window
          </button>
        </div>

        {/* List */}
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
          {windows.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <Clock className="h-12 w-12 text-gray-400 dark:text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No maintenance windows</h3>
              <p className="text-gray-500 dark:text-gray-400 mb-4">Create a window to suppress alerts during planned downtime</p>
              <button onClick={() => setShowModal(true)} className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition">
                Add Window
              </button>
            </div>
          ) : (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {windows.map((w) => (
                <div key={w.id} className="px-6 py-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800 transition">
                  <div className="flex items-center gap-4">
                    <div className={`p-2 rounded-lg ${w.is_active ? 'bg-green-100 dark:bg-green-950' : 'bg-gray-100 dark:bg-gray-800'}`}>
                      <Clock className={`h-5 w-5 ${w.is_active ? 'text-green-600 dark:text-green-400' : 'text-gray-400'}`} />
                    </div>
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">{w.name}</h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{formatSchedule(w)} · {w.timezone}</p>
                      {w.monitor_ids?.length > 0 && (
                        <p className="text-xs text-gray-400 dark:text-gray-500 mt-0.5">{w.monitor_ids.length} monitor(s)</p>
                      )}
                      {(!w.monitor_ids || w.monitor_ids.length === 0) && (
                        <p className="text-xs text-gray-400 dark:text-gray-500 mt-0.5">All monitors</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${w.is_active ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-gray-800 text-gray-500'}`}>
                      {w.is_active ? 'Active' : 'Inactive'}
                    </span>
                    <button onClick={() => handleToggle(w.id)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition" title="Toggle">
                      <Power className="h-4 w-4 text-gray-500 dark:text-gray-400" />
                    </button>
                    <button onClick={() => handleDelete(w.id)} className="p-2 hover:bg-red-50 dark:hover:bg-red-950 rounded-lg transition text-red-500">
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Info */}
        <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-5">
          <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">💡 How it works</h3>
          <ul className="text-sm text-blue-800 dark:text-blue-400 space-y-1">
            <li>• During an active maintenance window, alerts are suppressed</li>
            <li>• Checks still run — only notifications are paused</li>
            <li>• Leave monitors empty to apply to all monitors</li>
            <li>• Times are based on the selected timezone</li>
          </ul>
        </div>
      </div>

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">New Maintenance Window</h2>
              <button onClick={() => setShowModal(false)} className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition">
                <X className="h-5 w-5 text-gray-500" />
              </button>
            </div>
            <div className="px-6 py-4 space-y-4">
              {/* Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Name</label>
                <input type="text" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })}
                  placeholder="e.g. Weekly DB maintenance"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500" />
              </div>
              {/* Repeat */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Repeat</label>
                <select value={form.repeat_type} onChange={e => setForm({ ...form, repeat_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500">
                  {REPEAT_TYPES.map(r => <option key={r.value} value={r.value}>{r.label}</option>)}
                </select>
              </div>
              {/* Weekday (weekly) */}
              {form.repeat_type === 'weekly' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Day of Week</label>
                  <div className="flex gap-2 flex-wrap">
                    {WEEKDAYS.map((d, i) => (
                      <button key={i} onClick={() => setForm({ ...form, weekday: i })}
                        className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${form.weekday === i ? 'bg-green-600 text-white' : 'border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-green-500'}`}>
                        {d}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              {/* Day of month (monthly) */}
              {form.repeat_type === 'monthly' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Day of Month</label>
                  <input type="number" min={1} max={31} value={form.day_of_month} onChange={e => setForm({ ...form, day_of_month: Number(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500" />
                </div>
              )}
              {/* Date range (once) */}
              {form.repeat_type === 'once' && (
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Start Date</label>
                    <input type="datetime-local" value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">End Date</label>
                    <input type="datetime-local" value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500" />
                  </div>
                </div>
              )}
              {/* Time range */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Start Time</label>
                  <input type="time" value={form.start_time} onChange={e => setForm({ ...form, start_time: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">End Time</label>
                  <input type="time" value={form.end_time} onChange={e => setForm({ ...form, end_time: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500" />
                </div>
              </div>
              {/* Timezone */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Timezone</label>
                <select value={form.timezone} onChange={e => setForm({ ...form, timezone: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500">
                  <option value="Asia/Seoul">Asia/Seoul (KST)</option>
                  <option value="UTC">UTC</option>
                  <option value="America/New_York">America/New_York (EST)</option>
                  <option value="America/Los_Angeles">America/Los_Angeles (PST)</option>
                  <option value="Europe/London">Europe/London (GMT)</option>
                  <option value="Europe/Berlin">Europe/Berlin (CET)</option>
                  <option value="Asia/Tokyo">Asia/Tokyo (JST)</option>
                  <option value="Asia/Singapore">Asia/Singapore (SGT)</option>
                </select>
              </div>
              {/* Monitors */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Apply to monitors <span className="text-gray-400 font-normal">(empty = all)</span>
                </label>
                <div className="space-y-1 max-h-32 overflow-y-auto border border-gray-200 dark:border-gray-600 rounded-lg p-2">
                  {monitors.map((m: any) => (
                    <label key={m.id} className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700 px-2 py-1 rounded">
                      <input type="checkbox"
                        checked={form.monitor_ids.includes(m.id)}
                        onChange={e => {
                          if (e.target.checked) setForm({ ...form, monitor_ids: [...form.monitor_ids, m.id] });
                          else setForm({ ...form, monitor_ids: form.monitor_ids.filter(id => id !== m.id) });
                        }}
                        className="rounded" />
                      {m.name}
                    </label>
                  ))}
                </div>
              </div>
            </div>
            <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3">
              <button onClick={() => setShowModal(false)} className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition">
                Cancel
              </button>
              <button onClick={handleCreate} disabled={saving}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50">
                {saving ? 'Creating...' : 'Create'}
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
"""

with open(os.path.join(PAGE_DIR, "page.tsx"), 'w', encoding='utf-8') as f:
    f.write(page_content)
print("Maintenance page created!")


# ── 3. DashboardLayout 사이드바에 Maintenance 메뉴 추가 ──────────────────────
FILE_LAYOUT = r"C:\home\jeon\api-health-monitor\frontend\components\DashboardLayout.tsx"

with open(FILE_LAYOUT, 'r', encoding='utf-8') as f:
    c = f.read()

# Wrench 아이콘 import 추가
old_icons = "import { Activity, Bell, BarChart3, Settings, LogOut, Menu, X, Sun, Moon } from 'lucide-react';"
new_icons = "import { Activity, Bell, BarChart3, Settings, LogOut, Menu, X, Sun, Moon, Wrench } from 'lucide-react';"
c = c.replace(old_icons, new_icons)

# 네비게이션에 Maintenance 추가
old_nav = "    { name: 'Settings', href: '/dashboard/settings', icon: Settings },"
new_nav = "    { name: 'Settings', href: '/dashboard/settings', icon: Settings },\n    { name: 'Maintenance', href: '/dashboard/maintenance', icon: Wrench },"
c = c.replace(old_nav, new_nav)

with open(FILE_LAYOUT, 'w', encoding='utf-8') as f:
    f.write(c)

print("DashboardLayout done!", "Maintenance" in c)
print("\nAll frontend done!")
