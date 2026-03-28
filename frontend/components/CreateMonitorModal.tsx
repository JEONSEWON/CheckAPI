'use client';

import { useState } from 'react';
import { X, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { monitorsAPI } from '@/lib/api';
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
  const [isLoading, setIsLoading] = useState(false);
  const [checkResult, setCheckResult] = useState<{ status: string; response_time?: number } | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(true);

  if (!isOpen) return null;

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
      const monitor = await monitorsAPI.create({
        name: generateName(url),
        url,
        method,
        interval: 300, // Free plan default
        timeout: 30,
        expected_status: expectedStatus,
        ...(keyword ? { keyword, keyword_present: keywordPresent } : {}),
      });

      // Trigger instant check
      try {
        await monitorsAPI.checkNow(monitor.id);
        // Poll for result (wait up to 8 seconds)
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
        // 즉시 체크 실패해도 모니터는 생성됨
      }

      toast.success('Monitor created!');
      onSuccess();
    } catch (error: any) {
      toast.error(error.message || 'Failed to create monitor');
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
    setCheckResult(null);
    setShowAdvanced(false);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={handleClose}
      />

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Add Monitor
            </h2>
            <button
              onClick={handleClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"
            >
              <X className="h-5 w-5 dark:text-gray-400" />
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6 space-y-4">

            {/* URL */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                API URL *
              </label>
              <input
                type="url"
                required
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                placeholder="https://api.example.com/health"
              />
            </div>

            {/* Check Result */}
            {checkResult && (
              <div className={`flex items-center gap-3 p-3 rounded-lg ${
                checkResult.status === 'up'
                  ? 'bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800'
                  : 'bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800'
              }`}>
                {checkResult.status === 'up' ? (
                  <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
                )}
                <div>
                  <p className={`font-semibold text-sm ${checkResult.status === 'up' ? 'text-green-700 dark:text-green-400' : 'text-red-700 dark:text-red-400'}`}>
                    {checkResult.status === 'up' ? '✅ Your API is up and running!' : '❌ Your API returned an error'}
                  </p>
                  {checkResult.response_time && (
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                      Response time: {checkResult.response_time}ms
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Advanced toggle */}
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="text-sm text-gray-500 dark:text-gray-400 hover:text-green-600 transition"
            >
              {showAdvanced ? '▲ Hide advanced options' : '▼ Advanced options'}
            </button>

            {showAdvanced && (
              <div className="space-y-4 pt-2 border-t border-gray-100 dark:border-gray-700">
                {/* Method */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    HTTP Method
                  </label>
                  <select
                    value={method}
                    onChange={(e) => setMethod(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                  >
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                    <option value="PUT">PUT</option>
                    <option value="DELETE">DELETE</option>
                    <option value="HEAD">HEAD</option>
                  </select>
                </div>

                {/* Expected Status */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Expected Status Code
                  </label>
                  <input
                    type="number"
                    min={100}
                    max={599}
                    value={expectedStatus}
                    onChange={(e) => setExpectedStatus(Number(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                  />
                </div>

                {/* Keyword Check */}
                <div>
                  <label className="block text-sm font-medium text-orange-600 dark:text-orange-400 mb-2">
                    ⚡ Silent Failure Detection <span className="text-gray-400 font-normal text-xs">(optional)</span>
                  </label>
                  <input
                    type="text"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                    placeholder='e.g. "status":"ok"'
                  />
                  {keyword && (
                    <div className="mt-2 flex items-center gap-3">
                      <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <input
                          type="radio"
                          checked={keywordPresent}
                          onChange={() => setKeywordPresent(true)}
                        />
                        Must be present
                      </label>
                      <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <input
                          type="radio"
                          checked={!keywordPresent}
                          onChange={() => setKeywordPresent(false)}
                        />
                        Must be absent
                      </label>
                    </div>
                  )}
                </div>
              </div>
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
                  Checking your API...
                </>
              ) : (
                'Start Monitoring'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
