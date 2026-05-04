'use client';

import { useEffect, useState } from 'react';

import { API_URL } from '@/lib/api';

export default function LiveUserCount() {
  const [count, setCount] = useState<number | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/public/stats`);
        if (res.ok) {
          const data = await res.json();
          setCount(data.active_users);
        }
      } catch {
        // 실패해도 조용히 숨김
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 60000);
    return () => clearInterval(interval);
  }, []);

  if (count === null) return null;

  return (
    <div className="flex justify-center mb-4">
      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gray-900/60 border border-gray-700 text-sm text-gray-300">
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
        </span>
        <span>
          <strong className="text-white">{count.toLocaleString()}</strong> developers already monitoring their APIs
        </span>
      </div>
    </div>
  );
}
