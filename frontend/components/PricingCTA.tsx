'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { subscriptionAPI } from '@/lib/api';
import toast from 'react-hot-toast';

const PLAN_MAP: Record<string, string> = {
  'Starter': 'starter',
  'Pro': 'pro',
  'Business': 'business',
};

interface PricingCTAProps {
  planName: string;
  ctaHref: string;
  highlight: boolean;
}

export default function PricingCTA({ planName, ctaHref, highlight }: PricingCTAProps) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
  }, []);

  const handleClick = async () => {
    if (planName === 'Free') {
      router.push(isLoggedIn ? '/dashboard' : '/register');
      return;
    }

    if (!isLoggedIn) {
      router.push('/register');
      return;
    }

    // 로그인 상태 → 바로 결제
    setLoading(true);
    try {
      const response = await subscriptionAPI.checkout(PLAN_MAP[planName]);
      window.location.href = response.checkout_url;
    } catch (error: any) {
      toast.error('Failed to create checkout');
    } finally {
      setLoading(false);
    }
  };

  const getLabel = () => {
    if (planName === 'Free') return isLoggedIn ? 'Go to Dashboard' : 'Start Free';
    return isLoggedIn ? 'Upgrade Now' : 'Get Started';
  };

  const baseClass = `w-full py-3 rounded-xl font-semibold transition text-center`;
  const highlightClass = highlight
    ? 'bg-green-600 text-white hover:bg-green-700'
    : 'border-2 border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white hover:border-green-500 dark:hover:border-green-500';

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className={`${baseClass} ${highlightClass} ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      {loading ? 'Loading...' : getLabel()}
    </button>
  );
}
