'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

export default function PublicAuthButtons() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
  }, []);

  if (!mounted) return <div className="w-24 h-9" />;

  if (isLoggedIn) {
    return (
      <a
        href="/dashboard"
        className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium"
      >
        Dashboard →
      </a>
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
