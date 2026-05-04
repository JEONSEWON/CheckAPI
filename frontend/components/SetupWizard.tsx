'use client';

import { useState } from 'react';
import { CheckCircle, Bell, Rocket, X, ArrowRight, ExternalLink } from 'lucide-react';
import { authAPI } from '@/lib/api';
import CreateMonitorModal from './CreateMonitorModal';
import CreateAlertChannelModal from './CreateAlertChannelModal';

interface SetupWizardProps {
  onComplete: () => void;
}

const STEPS = [
  {
    id: 1,
    icon: Rocket,
    title: 'Create your first monitor',
    description: 'Paste your API URL and let CheckAPI watch it 24/7. Takes 30 seconds.',
    cta: 'Add Monitor',
    color: 'green',
  },
  {
    id: 2,
    icon: Bell,
    title: 'Set up an alert channel',
    description: 'Get notified via Email, Slack, Telegram, Discord, or Webhook when your API goes down.',
    cta: 'Add Alert Channel',
    color: 'blue',
  },
  {
    id: 3,
    icon: CheckCircle,
    title: "You're all set!",
    description: 'Your first check will run within minutes. We\'ll alert you the moment anything goes wrong.',
    cta: "Let's go!",
    color: 'purple',
  },
];

export default function SetupWizard({ onComplete }: SetupWizardProps) {
  const [step, setStep] = useState(1);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());
  const [showMonitorModal, setShowMonitorModal] = useState(false);
  const [showAlertModal, setShowAlertModal] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);

  const markStepDone = (s: number) =>
    setCompletedSteps((prev) => new Set(Array.from(prev).concat(s)));

  const handleFinish = async () => {
    setIsCompleting(true);
    try {
      await authAPI.completeOnboarding();
    } catch {
      // Non-critical — proceed regardless
    } finally {
      onComplete();
    }
  };

  const handleSkip = async () => {
    setIsCompleting(true);
    try {
      await authAPI.completeOnboarding();
    } catch {
      // Non-critical
    } finally {
      onComplete();
    }
  };

  return (
    <>
      {/* Overlay */}
      <div className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm" />

      {/* Wizard card */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-lg">
          {/* Header */}
          <div className="flex items-center justify-between px-6 pt-6 pb-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                Welcome to CheckAPI! 👋
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                Get started in 3 quick steps
              </p>
            </div>
            <button
              onClick={handleSkip}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition"
              title="Skip setup"
            >
              <X className="h-5 w-5 text-gray-400" />
            </button>
          </div>

          {/* Progress bar */}
          <div className="px-6 mb-6">
            <div className="flex items-center gap-2">
              {STEPS.map((s, i) => (
                <div key={s.id} className="flex items-center gap-2 flex-1">
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                      completedSteps.has(s.id)
                        ? 'bg-green-500 text-white'
                        : step === s.id
                        ? 'bg-green-600 text-white ring-4 ring-green-100 dark:ring-green-900'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-400'
                    }`}
                  >
                    {completedSteps.has(s.id) ? '✓' : s.id}
                  </div>
                  {i < STEPS.length - 1 && (
                    <div
                      className={`flex-1 h-1 rounded-full transition-all ${
                        completedSteps.has(s.id)
                          ? 'bg-green-500'
                          : 'bg-gray-200 dark:bg-gray-700'
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Step content */}
          {STEPS.map((s) => {
            if (s.id !== step) return null;
            const Icon = s.icon;
            return (
              <div key={s.id} className="px-6 pb-6 space-y-5">
                <div className="flex items-start gap-4">
                  <div
                    className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${
                      s.color === 'green'
                        ? 'bg-green-100 dark:bg-green-900'
                        : s.color === 'blue'
                        ? 'bg-blue-100 dark:bg-blue-900'
                        : 'bg-purple-100 dark:bg-purple-900'
                    }`}
                  >
                    <Icon
                      className={`h-6 w-6 ${
                        s.color === 'green'
                          ? 'text-green-600'
                          : s.color === 'blue'
                          ? 'text-blue-600'
                          : 'text-purple-600'
                      }`}
                    />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      {s.title}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      {s.description}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {/* Main CTA */}
                  {step === 1 && (
                    <button
                      onClick={() => setShowMonitorModal(true)}
                      className="flex items-center gap-2 px-4 py-2.5 bg-green-600 text-white rounded-xl hover:bg-green-700 transition font-medium text-sm"
                    >
                      {s.cta}
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  )}
                  {step === 2 && (
                    <button
                      onClick={() => setShowAlertModal(true)}
                      className="flex items-center gap-2 px-4 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition font-medium text-sm"
                    >
                      {s.cta}
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  )}
                  {step === 3 && (
                    <button
                      onClick={handleFinish}
                      disabled={isCompleting}
                      className="flex items-center gap-2 px-4 py-2.5 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition font-medium text-sm disabled:opacity-50"
                    >
                      {s.cta}
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  )}

                  {/* Skip step (steps 1 & 2 only) */}
                  {step < 3 && (
                    <button
                      onClick={() => {
                        if (step === 2) {
                          if (!window.confirm("Alert channel 없이 진행하시겠어요?\n모니터가 다운돼도 알림을 받을 수 없어요.")) return;
                        }
                        markStepDone(step);
                        setStep(step + 1);
                      }}
                      className="text-sm text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition"
                    >
                      Skip this step
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Monitor modal */}
      <CreateMonitorModal
        isOpen={showMonitorModal}
        onClose={() => setShowMonitorModal(false)}
        onSuccess={() => {
          setShowMonitorModal(false);
          markStepDone(1);
          setStep(2);
        }}
      />

      {/* Alert channel modal */}
      <CreateAlertChannelModal
        isOpen={showAlertModal}
        onClose={() => setShowAlertModal(false)}
        onSuccess={() => {
          setShowAlertModal(false);
          markStepDone(2);
          setStep(3);
        }}
      />
    </>
  );
}
