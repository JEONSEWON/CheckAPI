'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import { analyticsAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import { Activity, TrendingUp, AlertCircle, Clock } from 'lucide-react';
import toast from 'react-hot-toast';

export default function AnalyticsPage() {
  const [overview, setOverview] = useState<any>(null);
  const [incidents, setIncidents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [slaReport, setSlaReport] = useState<any>(null);
  const [slaMonths, setSlaMonths] = useState(3);
  const user = useAuthStore((state) => state.user);

  useEffect(() => { loadData(); }, []);

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
    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app';
      const res = await fetch(`${API_URL}/api/v1/analytics/sla?months=${months}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) setSlaReport(await res.json());
    } catch {}
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
      </div>
    </DashboardLayout>
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
