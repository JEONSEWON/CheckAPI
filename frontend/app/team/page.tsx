'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { UserPlus, Trash2, Mail, CheckCircle, Clock, Crown, Loader2 } from 'lucide-react';
import { teamsAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';

interface TeamMember {
  id: string;
  invited_email: string;
  role: string;
  status: string;
  created_at: string;
  accepted_at: string | null;
}

export default function TeamPage() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [inviteEmail, setInviteEmail] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isInviting, setIsInviting] = useState(false);

  const isPlanAllowed = user?.plan === 'pro' || user?.plan === 'business';

  useEffect(() => {
    if (!user) { router.push('/login'); return; }
    if (isPlanAllowed) fetchMembers();
    else setIsLoading(false);
  }, [user]);

  const fetchMembers = async () => {
    try {
      const data = await teamsAPI.listMembers();
      setMembers(data);
    } catch {
      toast.error('Failed to load team members');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInvite = async () => {
    if (!inviteEmail.trim()) return;
    setIsInviting(true);
    try {
      await teamsAPI.invite(inviteEmail.trim());
      toast.success(`Invitation sent to ${inviteEmail}`);
      setInviteEmail('');
      fetchMembers();
    } catch (e: any) {
      toast.error(e.response?.data?.detail || 'Failed to send invitation');
    } finally {
      setIsInviting(false);
    }
  };

  const handleRemove = async (memberId: string, email: string) => {
    if (!confirm(`Remove ${email} from your team?`)) return;
    try {
      await teamsAPI.removeMember(memberId);
      toast.success('Member removed');
      fetchMembers();
    } catch {
      toast.error('Failed to remove member');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-green-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-10">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Team</h1>
          <p className="text-gray-500 mt-1">Invite members to access your monitors.</p>
        </div>

        {/* Upgrade prompt */}
        {!isPlanAllowed && (
          <div className="bg-white rounded-xl border border-gray-200 p-8 text-center">
            <Crown className="h-10 w-10 text-yellow-500 mx-auto mb-3" />
            <h2 className="text-lg font-semibold text-gray-900 mb-1">Pro or Business plan required</h2>
            <p className="text-gray-500 text-sm mb-4">Upgrade to invite team members and collaborate.</p>
            <button
              onClick={() => router.push('/#pricing')}
              className="bg-green-600 text-white px-5 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium"
            >
              Upgrade Plan
            </button>
          </div>
        )}

        {isPlanAllowed && (
          <>
            {/* Invite box */}
            <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
              <h2 className="text-sm font-semibold text-gray-700 mb-3">Invite a member</h2>
              <div className="flex gap-3">
                <input
                  type="email"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleInvite()}
                  placeholder="colleague@example.com"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900"
                />
                <button
                  onClick={handleInvite}
                  disabled={isInviting || !inviteEmail.trim()}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition disabled:opacity-50 flex items-center gap-2 text-sm font-medium"
                >
                  {isInviting ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <UserPlus className="h-4 w-4" />
                  )}
                  Invite
                </button>
              </div>
              {user?.plan === 'pro' && (
                <p className="text-xs text-gray-400 mt-2">Pro plan: up to 5 members</p>
              )}
            </div>

            {/* Members list */}
            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100">
                <h2 className="text-sm font-semibold text-gray-700">
                  Members <span className="text-gray-400 font-normal">({members.length})</span>
                </h2>
              </div>

              {members.length === 0 ? (
                <div className="px-6 py-10 text-center text-gray-400 text-sm">
                  No members yet. Invite someone above.
                </div>
              ) : (
                <ul className="divide-y divide-gray-100">
                  {members.map((m) => (
                    <li key={m.id} className="flex items-center justify-between px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center">
                          <Mail className="h-4 w-4 text-gray-400" />
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">{m.invited_email}</p>
                          <p className="text-xs text-gray-400">
                            Invited {new Date(m.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        {m.status === 'active' ? (
                          <span className="flex items-center gap-1 text-xs text-green-600 font-medium">
                            <CheckCircle className="h-3.5 w-3.5" /> Active
                          </span>
                        ) : (
                          <span className="flex items-center gap-1 text-xs text-yellow-600 font-medium">
                            <Clock className="h-3.5 w-3.5" /> Pending
                          </span>
                        )}
                        <button
                          onClick={() => handleRemove(m.id, m.invited_email)}
                          className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
