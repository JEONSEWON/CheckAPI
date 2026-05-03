'use client';

import { useState } from 'react';
import { Play, CheckCircle, XCircle, AlertCircle, Save, Trash2, Loader2 } from 'lucide-react';
import { monitorsAPI } from '@/lib/api';
import toast from 'react-hot-toast';

interface RegexTestPanelProps {
  initialPattern?: string;
  initialPresent?: boolean;
  monitorId?: string;
  onSaved?: () => void;
}

export default function RegexTestPanel({ initialPattern = '', initialPresent = true, monitorId, onSaved }: RegexTestPanelProps) {
  const [pattern, setPattern] = useState(initialPattern);
  const [testBody, setTestBody] = useState('');
  const [mustBePresent, setMustBePresent] = useState(initialPresent);
  const [result, setResult] = useState<{ passed: boolean; found: boolean; match: string | null; error: string | null } | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    if (!monitorId || !pattern.trim()) return;
    setIsSaving(true);
    try {
      await monitorsAPI.update(monitorId, { keyword: pattern, keyword_present: mustBePresent, use_regex: true });
      toast.success('Pattern saved!');
      onSaved?.();
    } catch {
      toast.error('Failed to save');
    } finally {
      setIsSaving(false);
    }
  };

  const handleRemove = async () => {
    if (!monitorId) return;
    setIsSaving(true);
    try {
      await monitorsAPI.update(monitorId, { keyword: null, keyword_present: true, use_regex: false });
      setPattern('');
      toast.success('Pattern removed');
      onSaved?.();
    } catch {
      toast.error('Failed to remove');
    } finally {
      setIsSaving(false);
    }
  };

  const runTest = () => {
    if (!pattern.trim()) {
      setResult({ passed: false, found: false, match: null, error: 'Enter a pattern first' });
      return;
    }
    try {
      const regex = new RegExp(pattern);
      const match = testBody.match(regex);
      const found = match !== null;
      const passed = mustBePresent ? found : !found;
      setResult({ passed, found, match: match ? match[0] : null, error: null });
    } catch (e: any) {
      setResult({ passed: false, found: false, match: null, error: `Invalid regex: ${e.message}` });
    }
  };

  const examples = [
    { label: 'status == ok', pattern: '"status":\\s*"ok"', body: '{"status": "ok", "data": {}}' },
    { label: 'error is null', pattern: '"error":\\s*null', body: '{"status": "ok", "error": null}' },
    { label: 'balance > 0', pattern: '"balance":\\s*[1-9]\\d*', body: '{"balance": 150, "currency": "USD"}' },
    { label: 'no error key', pattern: '"error"', body: '{"status": "ok", "data": {"items": []}}' },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <span className="text-orange-500">⚡</span> Regex Live Tester
          </h2>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
            Test your Silent Failure Detection pattern against a real response body.
          </p>
        </div>
      </div>

      <div className="px-6 py-4 space-y-4">
        {/* Quick examples */}
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Quick examples:</p>
          <div className="flex flex-wrap gap-2">
            {examples.map((ex) => (
              <button
                key={ex.label}
                onClick={() => { setPattern(ex.pattern); setTestBody(ex.body); setResult(null); }}
                className="px-2.5 py-1 text-xs border border-gray-200 dark:border-gray-600 rounded-lg hover:border-orange-400 hover:text-orange-600 dark:hover:text-orange-400 transition text-gray-600 dark:text-gray-400 font-mono"
              >
                {ex.label}
              </button>
            ))}
          </div>
        </div>

        {/* Pattern input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Regex Pattern
          </label>
          <input
            type="text"
            value={pattern}
            onChange={e => { setPattern(e.target.value); setResult(null); }}
            placeholder={'"status":\\s*"ok"'}
            className="w-full px-3 py-2 font-mono text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
          />
        </div>

        {/* Must be present/absent */}
        <div className="flex items-center gap-4">
          {[true, false].map((val) => (
            <label key={String(val)} className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
              <input
                type="radio"
                checked={mustBePresent === val}
                onChange={() => { setMustBePresent(val); setResult(null); }}
              />
              {val ? 'Must be present' : 'Must be absent'}
            </label>
          ))}
        </div>

        {/* Test body */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Response Body
          </label>
          <textarea
            value={testBody}
            onChange={e => { setTestBody(e.target.value); setResult(null); }}
            placeholder={'{\n  "status": "ok",\n  "error": null,\n  "data": {}\n}'}
            rows={5}
            className="w-full px-3 py-2 font-mono text-xs border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-orange-500 resize-none"
          />
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={runTest}
            className="flex items-center gap-2 px-4 py-2 bg-orange-500 text-white text-sm rounded-lg hover:bg-orange-600 transition font-medium"
          >
            <Play className="h-4 w-4" />
            Test Pattern
          </button>
          {monitorId && (
            <button
              onClick={handleSave}
              disabled={isSaving || !pattern.trim()}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition font-medium disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
              Save Pattern
            </button>
          )}
          {monitorId && pattern && (
            <button
              onClick={handleRemove}
              disabled={isSaving}
              className="flex items-center gap-2 px-4 py-2 border border-red-200 dark:border-red-800 text-red-500 dark:text-red-400 text-sm rounded-lg hover:bg-red-50 dark:hover:bg-red-950 transition font-medium disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <Trash2 className="h-4 w-4" />
              Remove Pattern
            </button>
          )}
        </div>

        {/* Result */}
        {result && (
          <div className={`rounded-xl p-4 border ${
            result.error
              ? 'bg-yellow-50 dark:bg-yellow-950 border-yellow-200 dark:border-yellow-800'
              : result.passed
                ? 'bg-green-50 dark:bg-green-950 border-green-200 dark:border-green-800'
                : 'bg-red-50 dark:bg-red-950 border-red-200 dark:border-red-800'
          }`}>
            {result.error ? (
              <div className="flex items-center gap-2 text-yellow-700 dark:text-yellow-400 font-semibold text-sm">
                <AlertCircle className="h-4 w-4" />
                {result.error}
              </div>
            ) : (
              <div className="space-y-1">
                <div className={`flex items-center gap-2 font-semibold text-sm ${result.passed ? 'text-green-700 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                  {result.passed ? <CheckCircle className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
                  {result.passed ? 'Pattern check passed ✓' : 'Pattern check failed ✗'}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 space-y-0.5">
                  <p>Pattern <strong>{result.found ? 'found' : 'not found'}</strong> in response body</p>
                  {result.match && (
                    <p>Matched: <code className="bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded text-xs font-mono text-orange-600 dark:text-orange-400">{result.match}</code></p>
                  )}
                  <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                    {mustBePresent
                      ? result.found ? '→ Pattern found, condition met.' : '→ Pattern not found — this would trigger a DEGRADED alert.'
                      : result.found ? '→ Pattern found — this would trigger a DEGRADED alert.' : '→ Pattern absent, condition met.'
                    }
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tip */}
        <div className="text-xs text-gray-400 dark:text-gray-500 bg-gray-50 dark:bg-gray-900 rounded-lg p-3 space-y-1">
          <p className="font-medium text-gray-500 dark:text-gray-400">💡 Regex tips</p>
          <p><code className="font-mono">\s*</code> — matches optional whitespace (handles formatted JSON)</p>
          <p><code className="font-mono">[1-9]\d*</code> — matches positive numbers</p>
          <p><code className="font-mono">(ok|healthy)</code> — matches either value</p>
          <p><code className="font-mono">(?i)error</code> — case-insensitive match</p>
        </div>
      </div>
    </div>
  );
}
