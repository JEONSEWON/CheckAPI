'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import CreateAlertChannelModal from '@/components/CreateAlertChannelModal';
import { alertChannelsAPI } from '@/lib/api';
import { Bell, Mail, MessageSquare, Hash, Webhook, Plus, Trash2, FlaskConical } from 'lucide-react';
import toast from 'react-hot-toast';

export default function AlertChannelsPage() {
  const [channels, setChannels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [testingId, setTestingId] = useState<string | null>(null);

  useEffect(() => { loadChannels(); }, []);

  const loadChannels = async () => {
    try {
      const response = await alertChannelsAPI.list();
      setChannels(response);
    } catch (error) {
      toast.error('Failed to load alert channels');
    } finally {
      setLoading(false);
    }
  };

  const handleTest = async (id: string) => {
    setTestingId(id);
    try {
      await alertChannelsAPI.test(id);
      toast.success('Test alert sent! Check your channel.');
    } catch (error) {
      toast.error('Failed to send test alert');
    } finally {
      setTestingId(null);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this alert channel?')) return;
    try {
      await alertChannelsAPI.delete(id);
      toast.success('Channel deleted');
      loadChannels();
    } catch (error) {
      toast.error('Failed to delete channel');
    }
  };

  const channelIcons = {
    email: Mail, slack: MessageSquare, telegram: MessageSquare,
    discord: Hash, webhook: Webhook,
  };

  const channelColors = {
    email: 'bg-blue-100 dark:bg-blue-950 text-blue-600 dark:text-blue-400',
    slack: 'bg-purple-100 dark:bg-purple-950 text-purple-600 dark:text-purple-400',
    telegram: 'bg-cyan-100 dark:bg-cyan-950 text-cyan-600 dark:text-cyan-400',
    discord: 'bg-indigo-100 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400',
    webhook: 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400',
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Alert Channels</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Configure how you want to be notified</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Channel
          </button>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
          {channels.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <Bell className="h-12 w-12 text-gray-400 dark:text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No alert channels</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">Add your first channel to receive notifications</p>
              <button
                onClick={() => setShowModal(true)}
                className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition"
              >
                Add Channel
              </button>
            </div>
          ) : (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {channels.map((channel) => {
                const Icon = channelIcons[channel.type as keyof typeof channelIcons] || Bell;
                const colorClass = channelColors[channel.type as keyof typeof channelColors] || 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400';
                return (
                  <div key={channel.id} className="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className={`p-3 rounded-lg ${colorClass}`}>
                          <Icon className="h-6 w-6" />
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-900 dark:text-white capitalize">{channel.type}</h3>
                          <p className="text-sm text-gray-500 dark:text-gray-400">{getChannelDescription(channel)}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${channel.is_active ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300'}`}>
                          {channel.is_active ? 'Active' : 'Inactive'}
                        </span>
                        <button
                          onClick={() => handleTest(channel.id)}
                          disabled={testingId === channel.id}
                          className="p-2 hover:bg-blue-50 dark:hover:bg-blue-950 rounded-lg transition text-blue-600 dark:text-blue-400 disabled:opacity-50"
                          title="Send test alert"
                        >
                          <FlaskConical className={`h-4 w-4 ${testingId === channel.id ? 'animate-pulse' : ''}`} />
                        </button>
                        <button
                          onClick={() => handleDelete(channel.id)}
                          className="p-2 hover:bg-red-50 dark:hover:bg-red-950 rounded-lg transition text-red-600 dark:text-red-400"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">💡 How to use alert channels</h3>
          <ul className="text-sm text-blue-800 dark:text-blue-400 space-y-1">
            <li>• Create an alert channel (email, Slack, etc.)</li>
            <li>• Go to a monitor's detail page</li>
            <li>• Attach the channel to the monitor</li>
            <li>• Receive alerts when the monitor status changes!</li>
          </ul>
        </div>

        <CreateAlertChannelModal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          onSuccess={loadChannels}
        />
      </div>
    </DashboardLayout>
  );
}

function getChannelDescription(channel: any): string {
  const { type, config } = channel;
  if (type === 'email') return config.email;
  if (type === 'slack') return 'Slack webhook';
  if (type === 'telegram') return `Chat ID: ${config.chat_id}`;
  if (type === 'discord') return 'Discord webhook';
  if (type === 'webhook') return config.url;
  return 'Configured';
}
