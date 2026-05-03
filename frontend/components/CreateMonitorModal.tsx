'use client';

import { useState } from 'react';
import { X, Loader2, CheckCircle, XCircle, ArrowRight, Zap, Sparkles, Bell } from 'lucide-react';
import { monitorsAPI, aiAPI, assertionsAPI, alertChannelsAPI } from '@/lib/api';
import toast from 'react-hot-toast';

interface CreateMonitorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function CreateMonitorModal({ isOpen, onClose, onSuccess }: CreateMonitorModalProps) {
  const [url, setUrl] = useState('');
  const [method, setMethod] = useState('GET');
  const [expectedStatus, setExpectedStatus] = useState(200);
  const [keyword, setKeyword] = useState('');
  const [keywordPresent, setKeywordPresent] = useState(true);
  const [useRegex, setUseRegex] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [checkResult, setCheckResult] = useState<{ status: string; response_time?: number } | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(true);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [monitorType, setMonitorType] = useState<'http' | 'heartbeat'>('http');
  const [heartbeatInterval, setHeartbeatInterval] = useState(60);
  const [heartbeatGrace, setHeartbeatGrace] = useState(5);
  const [alertThreshold, setAlertThreshold] = useState(1);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState<{
    reasoning: string;
    assertions: { path: string; operator: string; expected: string }[];
  } | null>(null);

  // Alert prompt state (shown after monitor creation)
  const [createdMonitorId, setCreatedMonitorId] = useState<string | null>(null);
  const [showAlertPrompt, setShowAlertPrompt] = useState(false);
  const [alertChannelType, setAlertChannelType] = useState<'email' | 'slack' | 'telegram' | 'discord' | 'webhook'>('email');
  const [alertInput1, setAlertInput1] = useState('');
  const [alertInput2, setAlertInput2] = useState('');
  const [isAddingAlert, setIsAddingAlert] = useState(false);

  if (!isOpen) return null;

  if (showUpgradeModal) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl w-full max-w-md p-8 text-center">
          <div className="w-14 h-14 bg-orange-100 dark:bg-orange-900 rounded-full flex items-center justify-center mx-auto mb-4">
            <Zap className="h-7 w-7 text-orange-500" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Monitor limit reached</h2>
          <p className="text-gray-500 dark:text-gray-400 mb-2">
            You've used all <span className="font-semibold text-gray-700 dark:text-gray-300">10 monitors</span> on the Free plan.
          </p>
          <p className="text-gray-500 dark:text-gray-400 mb-6 text-sm">
            Upgrade to <span className="text-green-600 font-semibold">Starter</span> for 20 monitors and 1-minute checks, or <span className="text-green-600 font-semibold">Pro</span> for 100 monitors and faster intervals.
          </p>
          <div className="flex flex-col gap-3">
            <a
              href="/dashboard/settings?tab=billing"
              className="flex items-center justify-center gap-2 w-full px-4 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition font-semibold"
            >
              Upgrade Now
              <ArrowRight className="h-4 w-4" />
            </a>
            <button
              onClick={() => { setShowUpgradeModal(false); onClose(); }}
              className="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 transition text-sm"
            >
              Maybe later
            </button>
          </div>
        </div>
      </div>
    );
  }

  const handleAnalyze = async () => {
    if (!url) return;
    setIsAnalyzing(true);
    setAiSuggestion(null);
    try {
      const result = await aiAPI.analyzeEndpoint(url);
      setMethod(result.method);
      setExpectedStatus(result.expected_status);
      if (result.keyword) {
        setKeyword(result.keyword);
        setKeywordPresent(result.keyword_present);
      }
      setAiSuggestion({ reasoning: result.reasoning, assertions: result.assertions });
      setShowAdvanced(true);
    } catch (e: any) {
      toast.error(e.message || 'AI analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const generateName = (rawUrl: string) => {
    try {
      const { hostname, pathname } = new URL(rawUrl);
      const path = pathname === '/' ? '' : pathname;
      return `${hostname}${path}`;
    } catch {
      return rawUrl;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setCheckResult(null);
    try {
      if (monitorType === 'heartbeat') {
        const monitor = await monitorsAPI.create({
          name: url || 'Heartbeat Monitor',
          url: 'heartbeat',
          method: 'GET',
          interval: heartbeatInterval * 60,
          timeout: 30,
          expected_status: 200,
          monitor_type: 'heartbeat',
          heartbeat_interval: heartbeatInterval,
          heartbeat_grace: heartbeatGrace,
        } as any);
        toast.success('Heartbeat monitor created!');
        onSuccess();
        handleClose();
        return;
      }

      const monitor = await monitorsAPI.create({
        name: generateName(url),
        url,
        method,
        interval: 300,
        timeout: 30,
        expected_status: expectedStatus,
        ...(keyword ? { keyword, keyword_present: keywordPresent, use_regex: useRegex } : {}),
        alert_threshold: alertThreshold,
      });

      try {
        await monitorsAPI.checkNow(monitor.id);
        let result = null;
        for (let i = 0; i < 8; i++) {
          await new Promise(r => setTimeout(r, 1000));
          const checks = await monitorsAPI.checks(monitor.id, { page: 1, page_size: 1 });
          if (checks.checks && checks.checks.length > 0) {
            result = checks.checks[0];
            break;
          }
        }
        if (result) {
          setCheckResult({ status: result.status, response_time: result.response_time });
        }
      } catch {
        // instant check failure is OK
      }

      // Save AI-suggested assertions if any
      if (aiSuggestion?.assertions?.length) {
        try {
          await assertionsAPI.save(monitor.id, aiSuggestion.assertions.map((a) => ({
            type: 'json_path',
            path: a.path,
            operator: a.operator,
            expected: a.expected,
          })));
        } catch {
          // Non-critical — monitor already created
        }
      }

      toast.success('Monitor created!');
      onSuccess();
      setCreatedMonitorId(monitor.id);
      setShowAlertPrompt(true);
    } catch (error: any) {
      if (error.message && error.message.includes('Monitor limit reached')) {
        setShowUpgradeModal(true);
      } else {
        toast.error(error.message || 'Failed to create monitor');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setUrl('');
    setMethod('GET');
    setExpectedStatus(200);
    setKeyword('');
    setKeywordPresent(true);
    setUseRegex(false);
    setCheckResult(null);
    setShowAdvanced(true);
    setMonitorType('http');
    setHeartbeatInterval(60);
    setHeartbeatGrace(5);
    setAiSuggestion(null);
    setCreatedMonitorId(null);
    setShowAlertPrompt(false);
    setAlertChannelType('email');
    setAlertInput1('');
    setAlertInput2('');
    onClose();
  };

  const handleAddAlert = async () => {
    if (!createdMonitorId) return;
    const type = alertChannelType;
    let config: Record<string, string> = {};
    let name = '';
    if (type === 'email') {
      if (!alertInput1) return;
      config = { email: alertInput1 };
      name = `Email — ${alertInput1}`;
    } else if (type === 'slack') {
      if (!alertInput1) return;
      config = { webhook_url: alertInput1 };
      name = 'Slack Webhook';
    } else if (type === 'telegram') {
      if (!alertInput1 || !alertInput2) return;
      config = { bot_token: alertInput1, chat_id: alertInput2 };
      name = `Telegram — ${alertInput2}`;
    } else if (type === 'discord') {
      if (!alertInput1) return;
      config = { webhook_url: alertInput1 };
      name = 'Discord Webhook';
    } else if (type === 'webhook') {
      if (!alertInput1) return;
      config = { url: alertInput1 };
      name = 'Custom Webhook';
    }
    setIsAddingAlert(true);
    try {
      const channel = await alertChannelsAPI.create({ name, type, config });
      await alertChannelsAPI.linkToMonitor(createdMonitorId, channel.id);
      toast.success('Alert channel added!');
      handleClose();
    } catch (e: any) {
      toast.error(e.message || 'Failed to add alert channel');
    } finally {
      setIsAddingAlert(false);
    }
  };

  const CHANNEL_TABS = [
    { type: 'email', label: '📧 Email' },
    { type: 'slack', label: '💬 Slack' },
    { type: 'telegram', label: '✈️ Telegram' },
    { type: 'discord', label: '🎮 Discord' },
    { type: 'webhook', label: '🔗 Webhook' },
  ] as const;

  if (showAlertPrompt) {
    return (
      <div className="fixed inset-0 z-50 overflow-y-auto">
        <div className="fixed inset-0 bg-black bg-opacity-50 transition-opacity" onClick={handleClose} />
        <div className="flex min-h-full items-center justify-center p-4">
          <div className="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-green-600" />
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Get notified</h2>
              </div>
              <button onClick={handleClose} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition">
                <X className="h-5 w-5 dark:text-gray-400" />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <div className="flex items-start gap-3 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg p-3">
                <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-green-700 dark:text-green-400">Monitor created!</p>
                  <p className="text-xs text-green-600 dark:text-green-500 mt-0.5">Add an alert channel to get notified when it goes down.</p>
                </div>
              </div>

              {/* Channel type tabs */}
              <div className="flex gap-1 flex-wrap">
                {CHANNEL_TABS.map((tab) => (
                  <button
                    key={tab.type}
                    type="button"
                    onClick={() => { setAlertChannelType(tab.type); setAlertInput1(''); setAlertInput2(''); }}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                      alertChannelType === tab.type
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Channel-specific input */}
              <div className="space-y-2">
                {alertChannelType === 'email' && (
                  <input
                    type="email" autoFocus
                    value={alertInput1} onChange={e => setAlertInput1(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700 text-sm"
                  />
                )}
                {(alertChannelType === 'slack' || alertChannelType === 'discord') && (
                  <input
                    type="url" autoFocus
                    value={alertInput1} onChange={e => setAlertInput1(e.target.value)}
                    placeholder={alertChannelType === 'slack' ? 'https://hooks.slack.com/services/...' : 'https://discord.com/api/webhooks/...'}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700 text-sm"
                  />
                )}
                {alertChannelType === 'webhook' && (
                  <input
                    type="url" autoFocus
                    value={alertInput1} onChange={e => setAlertInput1(e.target.value)}
                    placeholder="https://your-server.com/webhook"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700 text-sm"
                  />
                )}
                {alertChannelType === 'telegram' && (
                  <>
                    <input
                      type="text" autoFocus
                      value={alertInput1} onChange={e => setAlertInput1(e.target.value)}
                      placeholder="Bot Token (from @BotFather)"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700 text-sm"
                    />
                    <input
                      type="text"
                      value={alertInput2} onChange={e => setAlertInput2(e.target.value)}
                      placeholder="Chat ID (e.g. -100123456789)"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700 text-sm"
                    />
                  </>
                )}
              </div>

              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={handleAddAlert}
                  disabled={isAddingAlert || !alertInput1 || (alertChannelType === 'telegram' && !alertInput2)}
                  className="flex-1 bg-green-600 text-white py-2.5 px-4 rounded-lg hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-medium text-sm"
                >
                  {isAddingAlert ? <Loader2 className="animate-spin h-4 w-4" /> : <Bell className="h-4 w-4" />}
                  {isAddingAlert ? 'Adding...' : 'Add & Connect'}
                </button>
                <button
                  type="button"
                  onClick={handleClose}
                  className="px-4 py-2.5 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 transition text-sm"
                >
                  Skip
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="fixed inset-0 bg-black bg-opacity-50 transition-opacity" onClick={handleClose} />
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Add Monitor</h2>
            <button onClick={handleClose} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition">
              <X className="h-5 w-5 dark:text-gray-400" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-4">
            {/* Monitor Type Tabs */}
            <div className="flex gap-2 p-1 bg-gray-100 dark:bg-gray-900 rounded-lg">
              {[
                { type: 'http', label: '🌐 HTTP Monitor', desc: 'Check URL uptime' },
                { type: 'heartbeat', label: '💓 Heartbeat / Cron', desc: 'Cron job monitoring' },
              ].map((t) => (
                <button
                  key={t.type}
                  type="button"
                  onClick={() => setMonitorType(t.type as 'http' | 'heartbeat')}
                  className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition text-left ${
                    monitorType === t.type
                      ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  <div>{t.label}</div>
                  <div className="text-xs font-normal opacity-60">{t.desc}</div>
                </button>
              ))}
            </div>

            {/* ── HEARTBEAT UI ── */}
            {monitorType === 'heartbeat' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Monitor Name *</label>
                  <input
                    type="text"
                    required
                    value={url}
                    onChange={e => setUrl(e.target.value)}
                    placeholder="e.g. Daily Backup Job"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Expected every (min)</label>
                    <input
                      type="number" min={1} max={10080}
                      value={heartbeatInterval}
                      onChange={e => setHeartbeatInterval(Number(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Grace period (min)</label>
                    <input
                      type="number" min={1} max={1440}
                      value={heartbeatGrace}
                      onChange={e => setHeartbeatGrace(Number(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                    />
                  </div>
                </div>
                <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-3 text-sm text-blue-700 dark:text-blue-300">
                  Alert fires if no ping received within <strong>{heartbeatInterval + heartbeatGrace} minutes</strong> ({heartbeatInterval}m + {heartbeatGrace}m grace).
                </div>
              </div>
            )}

            {/* ── HTTP UI ── */}
            {monitorType === 'http' && (
              <>
                {/* URL */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">API URL *</label>
                  <div className="flex gap-2">
                    <input
                      type="url" required value={url}
                      onChange={(e) => { setUrl(e.target.value); setAiSuggestion(null); }}
                      className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                      placeholder="https://api.example.com/health"
                    />
                    <button
                      type="button"
                      onClick={handleAnalyze}
                      disabled={!url || isAnalyzing}
                      className="flex items-center gap-1.5 px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition disabled:opacity-40 disabled:cursor-not-allowed text-sm font-medium whitespace-nowrap"
                    >
                      {isAnalyzing
                        ? <Loader2 className="h-4 w-4 animate-spin" />
                        : <Sparkles className="h-4 w-4" />}
                      {isAnalyzing ? 'Analyzing...' : 'AI Auto-detect'}
                    </button>
                  </div>
                </div>

                {/* AI Suggestion Banner */}
                {aiSuggestion && (
                  <div className="bg-purple-50 dark:bg-purple-950 border border-purple-200 dark:border-purple-800 rounded-lg p-3 space-y-1.5">
                    <p className="text-xs font-semibold text-purple-700 dark:text-purple-300 flex items-center gap-1">
                      <Sparkles className="h-3.5 w-3.5" /> AI auto-filled your settings
                    </p>
                    <p className="text-xs text-purple-600 dark:text-purple-400">{aiSuggestion.reasoning}</p>
                    {aiSuggestion.assertions.length > 0 && (
                      <p className="text-xs text-purple-500 dark:text-purple-500">
                        + {aiSuggestion.assertions.length} JSON Path assertion{aiSuggestion.assertions.length > 1 ? 's' : ''} will be saved automatically
                      </p>
                    )}
                  </div>
                )}

                {/* Check Result */}
                {checkResult && (
                  <div className={`flex items-center gap-3 p-3 rounded-lg ${
                    checkResult.status === 'up'
                      ? 'bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800'
                      : 'bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800'
                  }`}>
                    {checkResult.status === 'up'
                      ? <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
                      : <XCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
                    }
                    <div>
                      <p className={`font-semibold text-sm ${checkResult.status === 'up' ? 'text-green-700 dark:text-green-400' : 'text-red-700 dark:text-red-400'}`}>
                        {checkResult.status === 'up' ? '✅ Your API is up and running!' : '❌ Your API returned an error'}
                      </p>
                      {checkResult.response_time && (
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Response time: {checkResult.response_time}ms</p>
                      )}
                    </div>
                  </div>
                )}

                {/* Advanced options */}
                <button
                  type="button"
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="text-sm text-gray-500 dark:text-gray-400 hover:text-green-600 transition"
                >
                  {showAdvanced ? '▲ Hide advanced options' : '▼ Advanced options'}
                </button>

                {showAdvanced && (
                  <div className="space-y-4 pt-2 border-t border-gray-100 dark:border-gray-700">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">HTTP Method</label>
                      <select
                        value={method} onChange={(e) => setMethod(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                      >
                        <option value="GET">GET</option>
                        <option value="POST">POST</option>
                        <option value="PUT">PUT</option>
                        <option value="DELETE">DELETE</option>
                        <option value="HEAD">HEAD</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Expected Status Code</label>
                      <input
                        type="number" min={100} max={599} value={expectedStatus}
                        onChange={(e) => setExpectedStatus(Number(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-orange-600 dark:text-orange-400 mb-2">
                        ⚡ Silent Failure Detection <span className="text-gray-400 font-normal text-xs">(optional)</span>
                      </label>
                      <input
                        type="text" value={keyword}
                        onChange={(e) => setKeyword(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                        placeholder='e.g. "status":"ok"'
                      />
                      {keyword && (
                        <div className="mt-2 space-y-2">
                          <div className="flex items-center gap-3">
                            <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                              <input type="radio" checked={keywordPresent} onChange={() => setKeywordPresent(true)} />
                              Must be present
                            </label>
                            <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                              <input type="radio" checked={!keywordPresent} onChange={() => setKeywordPresent(false)} />
                              Must be absent
                            </label>
                          </div>
                          <label className="flex items-center gap-2 text-sm text-orange-600 dark:text-orange-400 cursor-pointer">
                            <input type="checkbox" checked={useRegex} onChange={(e) => setUseRegex(e.target.checked)} className="rounded" />
                            Use as Regex pattern
                          </label>
                          {useRegex && (
                            <p className="text-xs text-gray-400 dark:text-gray-500">
                              e.g. <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">"status":\s*"ok"</code> or <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">[1-9]\d*</code>
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Alert after how many failures?
                      </label>
                      <select
                        value={alertThreshold}
                        onChange={(e) => setAlertThreshold(Number(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                      >
                        <option value={1}>1 failure (immediately)</option>
                        <option value={2}>2 consecutive failures</option>
                        <option value={3}>3 consecutive failures</option>
                        <option value={5}>5 consecutive failures</option>
                      </select>
                      <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                        Prevents alert spam from brief flickers. Recovery always notifies immediately.
                      </p>
                    </div>
                  </div>
                )}
              </>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-green-600 text-white py-2.5 px-4 rounded-lg hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center font-medium"
            >
              {isLoading ? (
                <>
                  <Loader2 className="animate-spin h-4 w-4 mr-2" />
                  {monitorType === 'heartbeat' ? 'Creating...' : 'Checking your API...'}
                </>
              ) : (
                monitorType === 'heartbeat' ? 'Create Heartbeat Monitor' : 'Start Monitoring'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
