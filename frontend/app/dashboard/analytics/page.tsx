'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import { analyticsAPI, getAccessToken, API_URL } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import { Activity, TrendingUp, AlertCircle, Clock, Shield, ChevronDown, ChevronUp } from 'lucide-react';
import toast from 'react-hot-toast';

export default function AnalyticsPage() {
  const [overview, setOverview] = useState<any>(null);
  const [incidents, setIncidents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [slaReport, setSlaReport] = useState<any>(null);
  const [slaMonths, setSlaMonths] = useState(3);
  const [slaLoading, setSlaLoading] = useState(false);
  const user = useAuthStore((state) => state.user);

  const isPro = user?.plan === 'pro' || user?.plan === 'business';

  useEffect(() => { loadData(); }, []);

  useEffect(() => {
    if (isPro) loadSLA(slaMonths);
  }, [isPro, slaMonths]);

  const loadData = async () => {
    try {
      const [overviewRes, incidentsRes] = await Promise.all([
        analyticsAPI.overview(),
        analyticsAPI.incidents(7),
      ]);
      setOverview(overviewRes);
      setIncidents(incidentsRes.incidents || []);
    } catch (error) {
      toast.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  const loadSLA = async (months: number) => {
    setSlaLoading(true);
    try {
      const token = getAccessToken();
      const res = await fetch(`${API_URL}/api/v1/analytics/sla?months=${months}`, {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {},
        credentials: 'include',
      });
      if (res.ok) setSlaReport(await res.json());
    } catch {
    } finally {
      setSlaLoading(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Analytics</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Performance overview and insights</p>
        </div>

        {overview && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <StatCard title="Total Monitors" value={overview.total_monitors} icon={<Activity className="h-6 w-6 text-blue-600 dark:text-blue-400" />} subtitle={`${overview.active_monitors} active`} />
            <StatCard title="Overall Uptime" value={`${overview.overall_uptime}%`} icon={<TrendingUp className="h-6 w-6 text-green-600 dark:text-green-400" />} subtitle="Last 24 hours" />
            <StatCard title="Total Checks" value={overview.total_checks_24h} icon={<Clock className="h-6 w-6 text-purple-600 dark:text-purple-400" />} subtitle="Last 24 hours" />
            <StatCard title="Status" value={`${overview.monitors_up}/${overview.total_monitors}`} icon={<AlertCircle className="h-6 w-6 text-orange-600 dark:text-orange-400" />} subtitle="Monitors online" />
          </div>
        )}

        {overview && (
          <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Monitor Status Distribution</h2>
            <div className="grid grid-cols-3 gap-4">
              <StatusBox label="Online" count={overview.monitors_up} color="green" />
              <StatusBox label="Degraded" count={overview.monitors_degraded} color="yellow" />
              <StatusBox label="Offline" count={overview.monitors_down} color="red" />
            </div>
          </div>
        )}

        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Incidents (7 days)</h2>
          </div>
          {incidents.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <AlertCircle className="h-12 w-12 text-gray-400 dark:text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No incidents</h3>
              <p className="text-gray-600 dark:text-gray-400">All systems have been running smoothly!</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {incidents.slice(0, 10).map((incident, i) => (
                <IncidentRow key={i} incident={incident} />
              ))}
            </div>
          )}
        </div>

        {/* SLA Report */}
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-purple-600 dark:text-purple-400" />
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">SLA Report</h2>
              <span className="px-2 py-0.5 text-xs font-medium bg-purple-100 dark:bg-purple-950 text-purple-700 dark:text-purple-300 rounded-full">
                Pro / Business
              </span>
            </div>
            {isPro && (
              <div className="flex items-center gap-1">
                {[1, 3, 6, 12].map((m) => (
                  <button
                    key={m}
                    onClick={() => setSlaMonths(m)}
                    className={`px-3 py-1 text-sm rounded-md font-medium transition-colors ${
                      slaMonths === m
                        ? 'bg-purple-600 text-white'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    {m}M
                  </button>
                ))}
              </div>
            )}
          </div>

          {!isPro ? (
            <div className="px-6 py-12 text-center">
              <Shield className="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Pro / Business Plan Required</h3>
              <p className="text-gray-500 dark:text-gray-400 max-w-sm mx-auto">
                Upgrade to access detailed SLA reports with monthly uptime, downtime, and incident tracking per monitor.
              </p>
            </div>
          ) : slaLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
            </div>
          ) : slaReport && slaReport.monitors.length > 0 ? (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {slaReport.monitors.map((monitor: any) => (
                <SLAMonitorRow key={monitor.monitor_id} monitor={monitor} />
              ))}
            </div>
          ) : (
            <div className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
              No monitor data available for this period.
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}

function SLAMonitorRow({ monitor }: any) {
  const [expanded, setExpanded] = useState(false);
  const uptime = monitor.overall_uptime;
  const uptimeColor =
    uptime === null
      ? 'text-gray-400 dark:text-gray-500'
      : uptime >= 99.9
      ? 'text-green-600 dark:text-green-400'
      : uptime >= 99
      ? 'text-yellow-600 dark:text-yellow-400'
      : 'text-red-600 dark:text-red-400';

  return (
    <div>
      <button
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-left"
        onClick={() => setExpanded(!expanded)}
      >
        <div>
          <p className="font-medium text-gray-900 dark:text-white">{monitor.monitor_name}</p>
          <p className="text-sm text-gray-500 dark:text-gray-400">{monitor.monitor_url}</p>
        </div>
        <div className="flex items-center gap-6">
          <div className="text-right">
            <p className={`text-xl font-bold ${uptimeColor}`}>
              {uptime !== null ? `${uptime}%` : 'N/A'}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Overall Uptime</p>
          </div>
          {expanded
            ? <ChevronUp className="h-4 w-4 text-gray-400" />
            : <ChevronDown className="h-4 w-4 text-gray-400" />
          }
        </div>
      </button>

      {expanded && (
        <div className="px-6 pb-5 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">
                <th className="pb-2 font-medium">Month</th>
                <th className="pb-2 font-medium text-right">Uptime</th>
                <th className="pb-2 font-medium text-right">Downtime</th>
                <th className="pb-2 font-medium text-right">Incidents</th>
                <th className="pb-2 font-medium text-right">Avg Response</th>
                <th className="pb-2 font-medium text-right">Total Checks</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
              {monitor.monthly.map((m: any) => {
                const color =
                  m.uptime_percentage === null
                    ? 'text-gray-400'
                    : m.uptime_percentage >= 99.9
                    ? 'text-green-600 dark:text-green-400'
                    : m.uptime_percentage >= 99
                    ? 'text-yellow-600 dark:text-yellow-400'
                    : 'text-red-600 dark:text-red-400';
                return (
                  <tr key={m.month}>
                    <td className="py-2.5 text-gray-700 dark:text-gray-300">{m.month}</td>
                    <td className={`py-2.5 text-right font-semibold ${color}`}>
                      {m.uptime_percentage !== null ? `${m.uptime_percentage}%` : 'No data'}
                    </td>
                    <td className="py-2.5 text-right text-gray-600 dark:text-gray-400">
                      {m.downtime_minutes > 0 ? `${m.downtime_minutes}m` : '—'}
                    </td>
                    <td className="py-2.5 text-right text-gray-600 dark:text-gray-400">{m.incidents}</td>
                    <td className="py-2.5 text-right text-gray-600 dark:text-gray-400">
                      {m.avg_response_time > 0 ? `${m.avg_response_time}ms` : '—'}
                    </td>
                    <td className="py-2.5 text-right text-gray-600 dark:text-gray-400">{m.total_checks}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function StatCard({ title, value, icon, subtitle }: any) {
  return (
    <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</span>
        {icon}
      </div>
      <p className="text-3xl font-bold text-gray-900 dark:text-white mb-1">{value}</p>
      {subtitle && <p className="text-sm text-gray-500 dark:text-gray-400">{subtitle}</p>}
    </div>
  );
}

function StatusBox({ label, count, color }: any) {
  const colors = {
    green: 'bg-green-100 dark:bg-green-950 border-green-200 dark:border-green-800 text-green-800 dark:text-green-300',
    yellow: 'bg-yellow-100 dark:bg-yellow-950 border-yellow-200 dark:border-yellow-800 text-yellow-800 dark:text-yellow-300',
    red: 'bg-red-100 dark:bg-red-950 border-red-200 dark:border-red-800 text-red-800 dark:text-red-300',
  };
  return (
    <div className={`${colors[color as keyof typeof colors]} border-2 rounded-lg p-4 text-center`}>
      <p className="text-3xl font-bold mb-1">{count}</p>
      <p className="text-sm font-medium">{label}</p>
    </div>
  );
}

function IncidentRow({ incident }: any) {
  const statusColors = {
    down: 'bg-red-100 dark:bg-red-950 text-red-800 dark:text-red-300',
    degraded: 'bg-yellow-100 dark:bg-yellow-950 text-yellow-800 dark:text-yellow-300',
  };
  const duration = incident.duration_seconds;
  const durationText = duration < 60 ? `${duration}s` : duration < 3600 ? `${Math.floor(duration / 60)}m` : `${Math.floor(duration / 3600)}h`;
  return (
    <div className="px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-medium text-gray-900 dark:text-white">{incident.monitor_name}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">{new Date(incident.started_at).toLocaleString()}</p>
        </div>
        <div className="flex items-center space-x-3">
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[incident.status as keyof typeof statusColors]}`}>
            {incident.status.toUpperCase()}
          </span>
          <span className="text-sm text-gray-600 dark:text-gray-400">{durationText}</span>
          {incident.ongoing && (
            <span className="px-2 py-1 bg-orange-100 dark:bg-orange-950 text-orange-800 dark:text-orange-300 rounded text-xs font-medium">Ongoing</span>
          )}
        </div>
      </div>
    </div>
  );
}
