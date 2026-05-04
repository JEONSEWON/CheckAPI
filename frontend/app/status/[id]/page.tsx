'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { CheckCircle, AlertCircle, Activity, Clock, Zap, ExternalLink } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

import { API_URL as API_BASE } from '@/lib/api';

export default function PublicStatusPage() {
  const params = useParams();
  const monitorId = params.id as string;
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/public/status/${monitorId}`)
      .then(res => {
        if (res.status === 404) { setNotFound(true); return null; }
        return res.json();
      })
      .then(d => { if (d) setData(d); })
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false));
  }, [monitorId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-500" />
      </div>
    );
  }

  if (notFound || !data) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400 text-lg">Monitor not found</p>
          <a href="https://checkapi.io" className="text-green-500 text-sm mt-2 inline-block hover:underline">
            Powered by CheckAPI
          </a>
        </div>
      </div>
    );
  }

  const status = data.status?.current || 'unknown';
  const isUp = status === 'up';
  const isDegraded = status === 'degraded';

  const statusConfig = {
    up: {
      bg: 'bg-green-500',
      text: 'Operational',
      icon: <CheckCircle className="h-6 w-6" />,
      ringColor: 'ring-green-500/30',
      textColor: 'text-green-400',
    },
    down: {
      bg: 'bg-red-500',
      text: 'Outage',
      icon: <AlertCircle className="h-6 w-6" />,
      ringColor: 'ring-red-500/30',
      textColor: 'text-red-400',
    },
    degraded: {
      bg: 'bg-yellow-500',
      text: 'Degraded',
      icon: <AlertCircle className="h-6 w-6" />,
      ringColor: 'ring-yellow-500/30',
      textColor: 'text-yellow-400',
    },
    unknown: {
      bg: 'bg-gray-500',
      text: 'Unknown',
      icon: <Activity className="h-6 w-6" />,
      ringColor: 'ring-gray-500/30',
      textColor: 'text-gray-400',
    },
  };

  const cfg = statusConfig[status as keyof typeof statusConfig] || statusConfig.unknown;

  const daily = data.history?.daily || [];

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <div className="border-b border-gray-800">
        <div className="max-w-2xl mx-auto px-4 py-6 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white">{data.monitor?.name}</h1>
            <a
              href={data.monitor?.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-gray-500 hover:text-gray-300 flex items-center gap-1 mt-0.5 transition"
            >
              {data.monitor?.url}
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
          <div className={`flex items-center gap-2 px-4 py-2 rounded-full bg-gray-900 ring-2 ${cfg.ringColor} ${cfg.textColor}`}>
            {cfg.icon}
            <span className="font-semibold">{cfg.text}</span>
          </div>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 py-8 space-y-6">

        {/* Uptime bars */}
        <div className="bg-gray-900 rounded-xl border border-gray-800 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">90-Day History</h2>
            <span className="text-sm text-gray-500">
              {data.status?.last_checked
                ? `Checked ${formatDistanceToNow(new Date(data.status.last_checked + 'Z'), { addSuffix: true })}`
                : ''}
            </span>
          </div>
          <UptimeBars daily={daily} />
          <div className="flex justify-between text-xs text-gray-600 mt-2">
            <span>90 days ago</span>
            <span>Today</span>
          </div>
        </div>

        {/* Uptime stats */}
        <div className="grid grid-cols-3 gap-3">
          <UptimeStat label="24h uptime" value={`${data.uptime?.['24h'] ?? '--'}%`} />
          <UptimeStat label="7d uptime" value={`${data.uptime?.['7d'] ?? '--'}%`} />
          <UptimeStat label="30d uptime" value={`${data.uptime?.['30d'] ?? '--'}%`} />
        </div>

        {/* Response time */}
        <div className="bg-gray-900 rounded-xl border border-gray-800 p-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <Zap className="h-5 w-5 text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Avg Response Time</p>
              <p className="text-2xl font-bold text-white">
                {data.performance?.avg_response_time_ms ?? '--'}
                <span className="text-sm font-normal text-gray-400 ml-1">ms</span>
              </p>
            </div>
          </div>
          <div className={`h-3 w-3 rounded-full ${cfg.bg} ${isUp ? 'animate-pulse' : ''}`} />
        </div>

        {/* Incidents */}
        {data.incidents && data.incidents.length > 0 && (
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-5">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Recent Incidents</h2>
            <div className="space-y-3">
              {data.incidents.map((incident: any, i: number) => (
                <div key={i} className="flex items-start gap-3 text-sm">
                  <div className={`mt-0.5 h-2 w-2 rounded-full flex-shrink-0 ${incident.status === 'down' ? 'bg-red-500' : 'bg-yellow-500'}`} />
                  <div className="flex-1">
                    <span className="font-medium capitalize text-gray-200">{incident.status}</span>
                    {incident.response_time && (
                      <span className="text-gray-500 ml-2">{incident.response_time}ms</span>
                    )}
                  </div>
                  <span className="text-gray-600 flex-shrink-0">
                    {formatDistanceToNow(new Date(incident.checked_at + 'Z'), { addSuffix: true })}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center pt-4 pb-8">
          <a
            href="https://checkapi.io"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-400 transition"
          >
            <span className="text-green-500 font-semibold">CheckAPI</span>
            <span>— API Monitoring</span>
          </a>
        </div>
      </div>
    </div>
  );
}

function UptimeBars({ daily }: { daily: any[] }) {
  // Show last 90 days, pad left with empty if less
  const slots = 90;
  const padded = Array(Math.max(0, slots - daily.length)).fill(null).concat(daily.slice(-slots));

  return (
    <div className="flex items-end gap-0.5 h-10">
      {padded.map((day: any, i: number) => {
        if (!day) {
          return <div key={i} className="flex-1 h-full bg-gray-800 rounded-sm opacity-30" />;
        }
        const uptime = day.uptime ?? 100;
        const color = uptime >= 99 ? 'bg-green-500' : uptime >= 95 ? 'bg-yellow-500' : 'bg-red-500';
        const height = `${Math.max(20, uptime)}%`;
        return (
          <div
            key={i}
            className="flex-1 relative group"
            style={{ height: '100%', display: 'flex', alignItems: 'flex-end' }}
          >
            <div
              className={`w-full rounded-sm ${color} transition-all`}
              style={{ height }}
              title={`${day.date}: ${uptime}% uptime`}
            />
            {/* Tooltip */}
            <div className="absolute bottom-full mb-1 left-1/2 -translate-x-1/2 bg-gray-800 text-xs text-white px-2 py-1 rounded whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none z-10 border border-gray-700">
              {day.date}<br />{uptime}% uptime
            </div>
          </div>
        );
      })}
    </div>
  );
}

function UptimeStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800 p-4 text-center">
      <p className="text-2xl font-bold text-white">{value}</p>
      <p className="text-xs text-gray-500 mt-1">{label}</p>
    </div>
  );
}
