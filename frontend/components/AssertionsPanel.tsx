'use client';

import { useState, useEffect } from 'react';
import { assertionsAPI, aiAPI } from '@/lib/api';
import { Plus, Trash2, Play, CheckCircle, XCircle, ChevronDown, Loader2, Sparkles } from 'lucide-react';
import toast from 'react-hot-toast';

const OPERATORS = [
  { value: '==', label: 'equals (==)' },
  { value: '!=', label: 'not equals (!=)' },
  { value: '>', label: 'greater than (>)' },
  { value: '>=', label: 'greater than or equal (>=)' },
  { value: '<', label: 'less than (<)' },
  { value: '<=', label: 'less than or equal (<=)' },
  { value: 'contains', label: 'contains' },
  { value: 'not_contains', label: 'not contains' },
  { value: 'is_null', label: 'is null' },
  { value: 'is_not_null', label: 'is not null' },
  { value: 'exists', label: 'exists' },
];

const NEEDS_VALUE = ['==', '!=', '>', '>=', '<', '<=', 'contains', 'not_contains'];

const DEFAULT_ASSERTION = {
  assertion_type: 'jsonpath',
  path: '',
  operator: '==',
  value: '',
  logic: 'AND',
  is_active: true,
};

interface AssertionsPanelProps {
  monitorId: string;
  monitorUrl?: string;
}

export default function AssertionsPanel({ monitorId, monitorUrl }: AssertionsPanelProps) {
  const [assertions, setAssertions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [testBody, setTestBody] = useState('');
  const [testResults, setTestResults] = useState<any>(null);
  const [testing, setTesting] = useState(false);
  const [showTest, setShowTest] = useState(false);
  const [aiGenerating, setAiGenerating] = useState(false);

  useEffect(() => { loadAssertions(); }, [monitorId]);

  const loadAssertions = async () => {
    try {
      const data = await assertionsAPI.list(monitorId);
      setAssertions(data.length > 0 ? data : []);
    } catch {
      setAssertions([]);
    } finally {
      setLoading(false);
    }
  };

  const addAssertion = () => {
    if (assertions.length >= 10) {
      toast.error('Maximum 10 assertions allowed');
      return;
    }
    const logic = assertions.length > 0 ? assertions[0].logic : 'AND';
    setAssertions([...assertions, { ...DEFAULT_ASSERTION, logic }]);
  };

  const removeAssertion = (i: number) => {
    setAssertions(assertions.filter((_, idx) => idx !== i));
  };

  const updateAssertion = (i: number, field: string, val: any) => {
    const updated = [...assertions];
    updated[i] = { ...updated[i], [field]: val };
    // Sync logic across all assertions
    if (field === 'logic') {
      updated.forEach(a => a.logic = val);
    }
    setAssertions(updated);
  };

  const handleAIGenerate = async () => {
    if (!monitorUrl) return;
    setAiGenerating(true);
    try {
      const result = await aiAPI.analyzeEndpoint(monitorUrl);
      const suggested: any[] = result.assertions ?? [];

      if (suggested.length === 0) {
        toast('이 URL은 JSON 응답이 아니라 JSON Path 어설션을 생성할 수 없어요.\nJSON API 엔드포인트를 입력해보세요.', { duration: 4000 });
        return;
      }

      const existingPaths = new Set(assertions.map((a: any) => a.path));
      const toAdd = suggested.filter((s: any) => !existingPaths.has(s.path));
      const available = 10 - assertions.length;
      if (available <= 0) {
        toast.error('최대 10개 어설션까지 추가할 수 있어요');
        return;
      }
      const adding = toAdd.slice(0, available);
      if (adding.length < toAdd.length) {
        toast.error('최대 10개 한도로 일부만 추가됐어요');
      }
      if (adding.length === 0) {
        toast('AI가 추천한 어설션이 이미 모두 추가돼 있어요');
        return;
      }
      const logic = assertions.length > 0 ? assertions[0].logic : 'AND';
      setAssertions([...assertions, ...adding.map((s: any) => ({ ...DEFAULT_ASSERTION, ...s, logic }))]);
      toast.success(`AI가 ${adding.length}개 어설션을 추가했어요`);
    } catch (e: any) {
      toast.error(e.message || 'AI 분석에 실패했어요');
    } finally {
      setAiGenerating(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const payload = assertions.map((a, i) => ({
        assertion_type: a.assertion_type,
        path: a.path || null,
        operator: a.operator,
        value: parseValue(a.value, a.operator),
        logic: a.logic || 'AND',
        order: i,
        is_active: a.is_active !== false,
      }));
      await assertionsAPI.save(monitorId, payload);
      toast.success('Assertions saved!');
      loadAssertions();
    } catch (e: any) {
      toast.error(e.message || 'Failed to save');
    } finally {
      setSaving(false);
    }
  };

  const parseValue = (val: any, operator: string) => {
    if (!NEEDS_VALUE.includes(operator)) return null;
    if (val === '' || val === null || val === undefined) return null;
    if (val === 'null') return null;
    if (val === 'true') return true;
    if (val === 'false') return false;
    const num = Number(val);
    if (!isNaN(num) && val !== '') return num;
    return val;
  };

  const handleTest = async () => {
    if (!testBody.trim()) {
      toast.error('Paste a response body first');
      return;
    }
    setTesting(true);
    setTestResults(null);
    try {
      const payload = assertions.map((a, i) => ({
        assertion_type: a.assertion_type,
        path: a.path || null,
        operator: a.operator,
        value: parseValue(a.value, a.operator),
        logic: a.logic || 'AND',
        order: i,
        is_active: true,
      }));
      const result = await assertionsAPI.test(monitorId, testBody, payload);
      setTestResults(result);
    } catch (e: any) {
      toast.error(e.message || 'Test failed');
    } finally {
      setTesting(false);
    }
  };

  if (loading) return <div className="text-sm text-gray-500 dark:text-gray-400 py-4">Loading...</div>;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">JSON Path Assertions</h2>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Validate response body fields. Fires alert if any assertion fails.</p>
        </div>
        <div className="flex items-center gap-3">
          {monitorUrl && (
            <button
              onClick={handleAIGenerate}
              disabled={aiGenerating || assertions.length >= 10}
              className="flex items-center gap-1.5 bg-green-600 hover:bg-green-700 text-white text-xs px-3 py-1 rounded-lg transition disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {aiGenerating
                ? <Loader2 className="h-3 w-3 animate-spin" />
                : <Sparkles className="h-3 w-3" />}
              Auto-generate with AI
            </button>
          )}
          <span className="text-sm text-gray-500 dark:text-gray-400">{assertions.length} / 10</span>
        </div>
      </div>

      <div className="px-6 py-4 space-y-3">
        {/* Logic selector */}
        {assertions.length > 1 && (
          <div className="flex items-center gap-3 mb-2">
            <span className="text-sm text-gray-500 dark:text-gray-400">Logic:</span>
            {['AND', 'OR'].map(l => (
              <button
                key={l}
                onClick={() => updateAssertion(0, 'logic', l)}
                className={`px-3 py-1 rounded-lg text-sm font-semibold transition ${
                  (assertions[0]?.logic || 'AND') === l
                    ? 'bg-green-600 text-white'
                    : 'border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-green-500'
                }`}
              >
                {l}
              </button>
            ))}
            <span className="text-xs text-gray-400 dark:text-gray-500">
              {(assertions[0]?.logic || 'AND') === 'AND' ? 'All assertions must pass' : 'Any assertion must pass'}
            </span>
          </div>
        )}

        {/* Assertion rows */}
        {assertions.length === 0 ? (
          <div className="text-center py-8 text-gray-400 dark:text-gray-500">
            <p className="text-sm mb-1">No assertions yet.</p>
            <p className="text-xs">Add rules to validate response body content.</p>
          </div>
        ) : (
          assertions.map((a, i) => (
            <div key={i} className="grid grid-cols-12 gap-2 items-center">
              {/* Type */}
              <select
                value={a.assertion_type}
                onChange={e => updateAssertion(i, 'assertion_type', e.target.value)}
                className="col-span-2 px-2 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-green-500"
              >
                <option value="jsonpath">JSON Path</option>
                <option value="keyword">Keyword</option>
                <option value="header">Header</option>
              </select>

              {/* Path */}
              <input
                type="text"
                value={a.path || ''}
                onChange={e => updateAssertion(i, 'path', e.target.value)}
                placeholder={
                  a.assertion_type === 'jsonpath' ? '$.data.status' :
                  a.assertion_type === 'header' ? 'Content-Type' :
                  'keyword'
                }
                className="col-span-3 px-2 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-green-500 font-mono"
              />

              {/* Operator */}
              <select
                value={a.operator}
                onChange={e => updateAssertion(i, 'operator', e.target.value)}
                className="col-span-3 px-2 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-green-500"
              >
                {OPERATORS.map(op => (
                  <option key={op.value} value={op.value}>{op.label}</option>
                ))}
              </select>

              {/* Value */}
              {NEEDS_VALUE.includes(a.operator) ? (
                <input
                  type="text"
                  value={a.value ?? ''}
                  onChange={e => updateAssertion(i, 'value', e.target.value)}
                  placeholder="expected value"
                  className="col-span-3 px-2 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-green-500"
                />
              ) : (
                <div className="col-span-3 px-2 py-1.5 text-xs text-gray-400 dark:text-gray-500 italic">—</div>
              )}

              {/* Delete */}
              <button
                onClick={() => removeAssertion(i)}
                className="col-span-1 p-1.5 hover:bg-red-50 dark:hover:bg-red-950 rounded-lg transition text-red-400 flex justify-center"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </button>
            </div>
          ))
        )}

        {/* Add button */}
        <button
          onClick={addAssertion}
          className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400 hover:text-green-700 transition mt-2"
        >
          <Plus className="h-4 w-4" />
          Add assertion
        </button>

        {/* Save button */}
        <div className="pt-2 flex gap-3">
          <button
            onClick={handleSave}
            disabled={saving}
            className="px-4 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Assertions'}
          </button>
          {assertions.length > 0 && (
            <button
              onClick={() => setShowTest(!showTest)}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-700 dark:text-gray-300"
            >
              <Play className="h-3.5 w-3.5" />
              Live Test
              <ChevronDown className={`h-3.5 w-3.5 transition-transform ${showTest ? 'rotate-180' : ''}`} />
            </button>
          )}
        </div>

        {/* Live Test panel */}
        {showTest && (
          <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 space-y-3">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Paste a sample response body to test assertions:</p>
            <textarea
              value={testBody}
              onChange={e => setTestBody(e.target.value)}
              placeholder={'{\n  "status": "ok",\n  "data": { "balance": 150 },\n  "error": null\n}'}
              rows={6}
              className="w-full px-3 py-2 text-xs font-mono border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
            />
            <button
              onClick={handleTest}
              disabled={testing}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition disabled:opacity-50"
            >
              <Play className="h-3.5 w-3.5" />
              {testing ? 'Testing...' : 'Run Test'}
            </button>

            {/* Test results */}
            {testResults && (
              <div className="space-y-2">
                <div className={`flex items-center gap-2 font-semibold text-sm ${testResults.passed ? 'text-green-600 dark:text-green-400' : 'text-red-500'}`}>
                  {testResults.passed
                    ? <><CheckCircle className="h-4 w-4" /> All assertions passed</>
                    : <><XCircle className="h-4 w-4" /> Some assertions failed</>
                  }
                </div>
                {testResults.results?.map((r: any, i: number) => (
                  <div key={i} className={`flex items-start gap-3 p-2 rounded-lg text-xs ${r.passed ? 'bg-green-50 dark:bg-green-950' : 'bg-red-50 dark:bg-red-950'}`}>
                    {r.passed
                      ? <CheckCircle className="h-3.5 w-3.5 text-green-500 flex-shrink-0 mt-0.5" />
                      : <XCircle className="h-3.5 w-3.5 text-red-500 flex-shrink-0 mt-0.5" />
                    }
                    <div className="flex-1 min-w-0">
                      <span className="font-mono text-gray-700 dark:text-gray-300">
                        {r.path} {r.operator} {r.expected !== null && r.expected !== undefined ? JSON.stringify(r.expected) : ''}
                      </span>
                      {!r.passed && (
                        <div className="text-gray-500 dark:text-gray-400 mt-0.5">
                          Got: <span className="font-mono">{JSON.stringify(r.actual)}</span>
                          {r.error && <span className="text-red-400 ml-2">{r.error}</span>}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
