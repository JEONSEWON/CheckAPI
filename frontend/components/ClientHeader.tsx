'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';

function AuthButtons() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsLoggedIn(false);
    window.location.href = '/';
  };

  if (!mounted) return <div className="w-24 h-9" />;

  if (isLoggedIn) {
    return (
      <div className="flex items-center space-x-3">
        <a
          href="/dashboard"
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium"
        >
          Dashboard →
        </a>
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
    <>
      <Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">
        Log in
      </Link>
      <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">
        Get Started
      </Link>
    </>
  );
}

export default function ClientHeader() {
  return (
    <header className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="relative flex justify-between items-center h-16">
          <div className="flex items-center">
            <img src="/logo.png" alt="CheckAPI" className="h-14 w-14 rounded-xl object-contain" style={{ filter: "drop-shadow(0 0 8px rgba(0,229,180,0.6))" }} />
          </div>
          <nav className="hidden md:flex space-x-8 absolute left-1/2 -translate-x-1/2">
            <a href="#features" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Features</a>
            <a href="/pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Pricing</a>
            <Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition">Docs</Link>
          </nav>
          <div className="flex items-center space-x-4">
            <AuthButtons />
          </div>
        </div>
      </div>
    </header>
  );
}
