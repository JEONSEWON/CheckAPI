'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import { useAuthStore } from '@/lib/store';
import { subscriptionAPI, getAccessToken } from '@/lib/api';
import { CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';

export default function SettingsPage() {
  const user = useAuthStore((state) => state.user);
  const [subscription, setSubscription] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [billing, setBilling] = useState<'monthly' | 'annual'>('monthly');
  const [apiKeys, setApiKeys] = useState<any[]>([]);
  const [newKeyName, setNewKeyName] = useState('');
  const [createdKey, setCreatedKey] = useState<string | null>(null);
  const [apiKeyLoading, setApiKeyLoading] = useState(false);

  useEffect(() => {
    loadSubscription();
  }, []);

  useEffect(() => {
    if (user?.plan === 'business') loadApiKeys();
  }, [user?.plan]);

  const loadSubscription = async () => {
    try {
      const response = await subscriptionAPI.get();
      setSubscription(response);
    } catch (error) {
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async (plan: string) => {
    try {
      const response = await subscriptionAPI.checkout(plan, billing);
      window.location.href = response.checkout_url;
    } catch (error: any) {
      toast.error(error.message || 'Failed to create checkout');
    }
  };

  const loadApiKeys = async () => {
    try {
      const token = getAccessToken();
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app'}/api/v1/api-keys/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) setApiKeys(await res.json());
    } catch {}
  };

  const handleCreateApiKey = async () => {
    if (!newKeyName.trim()) return;
    setApiKeyLoading(true);
    try {
      const token = getAccessToken();
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app'}/api/v1/api-keys/?name=${encodeURIComponent(newKeyName)}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      if (res.ok) {
        setCreatedKey(data.key);
        setNewKeyName('');
        loadApiKeys();
        toast.success('API key created!');
      } else {
        toast.error(data.detail || 'Failed to create key');
      }
    } catch {
      toast.error('Failed to create key');
    } finally {
      setApiKeyLoading(false);
    }
  };

  const handleDeleteApiKey = async (keyId: string) => {
    if (!confirm('Delete this API key? This cannot be undone.')) return;
    try {
      const token = getAccessToken();
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app'}/api/v1/api-keys/${keyId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      loadApiKeys();
      toast.success('API key deleted');
    } catch {
      toast.error('Failed to delete key');
    }
  };

  const handleCancel = async () => {
    if (!confirm('Are you sure you want to cancel your subscription?')) return;
    try {
      await subscriptionAPI.cancel();
      toast.success('Subscription cancelled');
      loadSubscription();
    } catch (error) {
      toast.error('Failed to cancel subscription');
    }
  };

  const plans = [
    {
      name: 'Free',
      monthlyPrice: '$0',
      annualPrice: '$0',
      annualMonthly: '$0',
      features: ['10 monitors', '5-minute checks', 'All alert channels', 'Public status page', 'Keyword validation', 'SSL monitoring', '30-day history'],
    },
    {
      name: 'Starter',
      monthlyPrice: '$5',
      annualPrice: '$48',
      annualMonthly: '$4',
      features: ['20 monitors', '1-minute checks', 'All alert channels', 'Analytics', 'Keyword validation', 'SSL monitoring', '30-day history'],
      popular: true,
    },
    {
      name: 'Pro',
      monthlyPrice: '$15',
      annualPrice: '$144',
      annualMonthly: '$12',
      features: ['100 monitors', '30-second checks', 'All alert channels', 'Analytics', 'Team sharing (5 members)', 'Keyword validation', 'SSL monitoring', '90-day history'],
    },
    {
      name: 'Business',
      monthlyPrice: '$49',
      annualPrice: '$470',
      annualMonthly: '$39',
      features: ['Unlimited monitors', '10-second checks', 'All alert channels', 'Analytics', 'Team sharing (unlimited)', 'Keyword validation', 'SSL monitoring', 'REST API access', '1-year history'],
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your account and subscription</p>
        </div>

        {/* Current Plan */}
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Current Plan</h2>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white capitalize">{user?.plan}</p>
              {subscription && (
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Status: {subscription.status}</p>
              )}
            </div>
            {user?.plan !== 'free' && (
              <button onClick={handleCancel} className="text-sm text-red-600 dark:text-red-400 hover:text-red-700">
                Cancel Subscription
              </button>
            )}
          </div>
        </div>

        {/* Upgrade Plan */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Upgrade Your Plan</h2>
            <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
              <button
                onClick={() => setBilling('monthly')}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition ${billing === 'monthly' ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm' : 'text-gray-500 dark:text-gray-400'}`}
              >
                Monthly
              </button>
              <button
                onClick={() => setBilling('annual')}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition ${billing === 'annual' ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm' : 'text-gray-500 dark:text-gray-400'}`}
              >
                Annual
                <span className="ml-1.5 text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 px-1.5 py-0.5 rounded-full">-20%</span>
              </button>
            </div>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {plans.map((plan) => (
              <PlanCard
                key={plan.name}
                plan={plan}
                currentPlan={user?.plan || 'free'}
                onUpgrade={handleUpgrade}
                billing={billing}
              />
            ))}
          </div>
        </div>

        {/* Account Info */}
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Account Information</h2>
          <div className="space-y-3">
            <InfoRow label="Email" value={user?.email || ''} />
            <InfoRow label="Name" value={user?.name || 'Not set'} />
            <InfoRow label="Member since" value={user ? new Date(user.created_at).toLocaleDateString() : ''} />
          </div>
        </div>

        {/* API Access - Business Plan */}
        {user?.plan === 'business' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">API Access</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">Use API keys to access your monitor data programmatically.</p>

            {createdKey && (
              <div className="mb-4 p-4 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg">
                <p className="text-sm font-semibold text-green-700 dark:text-green-400 mb-2">⚠️ Save this key — it won't be shown again!</p>
                <div className="flex items-center gap-2">
                  <code className="flex-1 text-xs bg-white dark:bg-gray-900 px-3 py-2 rounded border border-green-200 dark:border-green-700 text-gray-900 dark:text-white font-mono break-all">{createdKey}</code>
                  <button
                    onClick={() => { navigator.clipboard.writeText(createdKey); toast.success('Copied!'); }}
                    className="px-3 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition"
                  >
                    Copy
                  </button>
                </div>
                <button onClick={() => setCreatedKey(null)} className="mt-2 text-xs text-gray-500 hover:text-gray-700">Dismiss</button>
              </div>
            )}

            {apiKeys.length > 0 && (
              <div className="mb-4 space-y-2">
                {apiKeys.map((key: any) => (
                  <div key={key.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div>
                      <p className="text-sm font-medium text-gray-900 dark:text-white">{key.name}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{key.key_prefix}... · Created {new Date(key.created_at).toLocaleDateString()}</p>
                    </div>
                    <button onClick={() => handleDeleteApiKey(key.id)} className="text-red-500 hover:text-red-700 text-sm">
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Key name (e.g. Production)"
                value={newKeyName}
                onChange={(e) => setNewKeyName(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm text-gray-900 dark:text-white bg-white dark:bg-gray-700"
              />
              <button
                onClick={handleCreateApiKey}
                disabled={apiKeyLoading || !newKeyName.trim()}
                className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition disabled:opacity-50"
              >
                {apiKeyLoading ? 'Creating...' : 'Create Key'}
              </button>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

function PlanCard({ plan, currentPlan, onUpgrade, billing }: any) {
  const isCurrent = plan.name.toLowerCase() === currentPlan;
  const isAnnual = billing === 'annual';
  const isFree = plan.name === 'Free';

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg border-2 p-6 ${plan.popular ? 'border-green-600 shadow-lg' : 'border-gray-200 dark:border-gray-700'}`}>
      {plan.popular && (
        <span className="bg-green-600 text-white text-xs font-bold px-3 py-1 rounded-full">POPULAR</span>
      )}
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mt-4">{plan.name}</h3>
      {isAnnual && !isFree ? (
        <div className="mt-4 mb-4">
          <div>
            <span className="text-4xl font-bold text-gray-900 dark:text-white">{plan.annualPrice}</span>
            <span className="text-gray-600 dark:text-gray-400">/year</span>
          </div>
          <div className="flex items-center gap-2 mt-1 flex-wrap">
            <span className="text-sm text-gray-500 dark:text-gray-400">{plan.annualMonthly}/mo</span>
            <span className="text-xs text-gray-400 dark:text-gray-500 line-through">{plan.monthlyPrice}/mo</span>
            <span className="text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 px-2 py-0.5 rounded-full font-medium">Save 20%</span>
          </div>
        </div>
      ) : (
        <div className="mt-4 mb-4">
          <span className="text-4xl font-bold text-gray-900 dark:text-white">{plan.monthlyPrice}</span>
          <span className="text-gray-600 dark:text-gray-400">/mo</span>
        </div>
      )}
      <ul className="space-y-3 mb-6">
        {plan.features.map((feature: string, i: number) => (
          <li key={i} className="flex items-center text-gray-700 dark:text-gray-300">
            <CheckCircle className="h-5 w-5 text-green-600 mr-2 flex-shrink-0" />
            {feature}
          </li>
        ))}
      </ul>
      {isCurrent ? (
        <button disabled className="w-full py-2 border-2 border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 rounded-lg font-medium">
          Current Plan
        </button>
      ) : (
        <button
          onClick={() => onUpgrade(plan.name.toLowerCase())}
          className={`w-full py-2 rounded-lg font-medium transition ${plan.popular ? 'bg-green-600 text-white hover:bg-green-700' : 'border-2 border-green-600 text-green-600 hover:bg-green-50 dark:hover:bg-green-900'}`}
        >
          {currentPlan === 'free' ? 'Upgrade' : 'Switch Plan'}
        </button>
      )}
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between py-2 border-b border-gray-100 dark:border-gray-800 last:border-0">
      <span className="text-gray-600 dark:text-gray-400">{label}</span>
      <span className="font-medium text-gray-900 dark:text-white">{value}</span>
    </div>
  );
}
