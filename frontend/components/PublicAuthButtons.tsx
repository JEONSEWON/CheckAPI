'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { authAPI, API_URL, getAccessToken } from '@/lib/api';

export default function PublicAuthButtons() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const token = getAccessToken();
    fetch(`${API_URL}/api/v1/auth/me`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      credentials: 'include',
    })
      .then((r) => setIsLoggedIn(r.ok))
      .catch(() => setIsLoggedIn(false));
  }, []);

  const handleLogout = async () => {
    await authAPI.logout();
    setIsLoggedIn(false);
    window.location.href = '/';
  };

  if (!mounted) return <div className="w-24 h-9" />;

  if (isLoggedIn) {
    return (
      <div className="flex items-center space-x-3">
        <Link
          href="/dashboard"
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium"
        >
          Dashboard →
        </Link>
        <button
          onClick={handleLogout}
          className="text-gray-500 dark:text-gray-400 hover:text-red-500 transition text-sm"
        >
          Log out
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-4">
      <Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">
        Log in
      </Link>
      <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">
        Get Started
      </Link>
    </div>
  );
}
