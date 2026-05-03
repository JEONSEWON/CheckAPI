'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { subscriptionAPI, authAPI } from '@/lib/api';
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
  billing?: string;
}

export default function PricingCTA({ planName, ctaHref, highlight, billing = 'monthly' }: PricingCTAProps) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPlan, setCurrentPlan] = useState<string>('free');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    authAPI.me().then((user: any) => {
      setIsLoggedIn(true);
      setCurrentPlan(user.plan || 'free');
    }).catch(() => {});
  }, []);

  const isCurrent = planName.toLowerCase() === currentPlan;

  const handleClick = async () => {
    if (isCurrent) return;

    if (planName === 'Free') {
      router.push(isLoggedIn ? '/dashboard' : '/register');
      return;
    }

    if (!isLoggedIn) {
      router.push('/register');
      return;
    }

    setLoading(true);
    try {
      const response = await subscriptionAPI.checkout(PLAN_MAP[planName], billing);
      window.location.href = response.checkout_url;
    } catch (error: any) {
      toast.error('Failed to create checkout');
    } finally {
      setLoading(false);
    }
  };

  const getLabel = () => {
    if (isCurrent) return 'Current Plan';
    if (planName === 'Free') return isLoggedIn ? 'Go to Dashboard' : 'Start Free';
    return isLoggedIn ? 'Upgrade Now' : 'Get Started';
  };

  const baseClass = `w-full py-3 rounded-xl font-semibold transition text-center`;

  const getClass = () => {
    if (isCurrent) return `${baseClass} border-2 border-green-500 text-green-600 dark:text-green-400 cursor-default`;
    if (highlight) return `${baseClass} bg-green-600 text-white hover:bg-green-700 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`;
    return `${baseClass} border-2 border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white hover:border-green-500 dark:hover:border-green-500 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`;
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading || isCurrent}
      className={getClass()}
    >
      {loading ? 'Loading...' : getLabel()}
    </button>
  );
}
