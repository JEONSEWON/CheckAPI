// API Client for API Health Monitor

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app';

// Token management
let accessToken: string | null = null;
let refreshToken: string | null = null;
let isRefreshing = false;
let refreshPromise: Promise<boolean> | null = null;

export function setTokens(access: string, refresh: string) {
  // Keep in-memory only — tokens are also stored as HttpOnly cookies by the server.
  // localStorage is no longer used to prevent XSS token theft.
  accessToken = access;
  refreshToken = refresh;
  // Migrate: remove legacy localStorage tokens on next setTokens call
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

export function getAccessToken(): string | null {
  // In-memory only; no localStorage fallback (migration: old tokens are cleared above)
  return accessToken;
}

export function getRefreshToken(): string | null {
  return refreshToken;
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

// API request helper with auto token refresh
async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<any> {
  const token = getAccessToken();
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: 'include',
  });

  // If 401, always try to refresh (cookie-based fallback works even after page reload)
  if (response.status === 401) {
    if (!isRefreshing) {
      isRefreshing = true;
      refreshPromise = refreshAccessToken().finally(() => {
        isRefreshing = false;
        refreshPromise = null;
      });
    }
    const refreshed = await refreshPromise!;
    if (refreshed) {
      headers['Authorization'] = `Bearer ${getAccessToken()}`;
      response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
        credentials: 'include',
      });
    } else {
      clearTokens();
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
      throw new Error('Authentication failed');
    }
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}

async function refreshAccessToken(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // Send in-memory token in body if available; backend falls back to HttpOnly cookie
      body: JSON.stringify({ refresh_token: getRefreshToken() || null }),
      credentials: 'include',
    });

    if (response.ok) {
      const data = await response.json();
      setTokens(data.access_token, data.refresh_token);
      return true;
    }
  } catch (error) {
    console.error('Token refresh failed:', error);
  }

  return false;
}

// Auth API
export const authAPI = {
  register: (email: string, password: string, name?: string) =>
    apiRequest('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    }),

  login: (email: string, password: string) =>
    apiRequest('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  me: () => apiRequest('/api/v1/auth/me'),

  completeOnboarding: () =>
    apiRequest('/api/v1/auth/complete-onboarding', { method: 'POST' }),
};

// Monitors API
export const monitorsAPI = {
  list: () => apiRequest('/api/v1/monitors/'),
  
  get: (id: string) => apiRequest(`/api/v1/monitors/${id}`),
  
  create: (data: {
    name: string;
    url: string;
    method?: string;
    monitor_type?: string;
    interval?: number;
    timeout?: number;
    expected_status?: number;
    keyword?: string;
    keyword_present?: boolean;
    use_regex?: boolean;
    alert_threshold?: number;
    heartbeat_interval?: number;
    heartbeat_grace?: number;
  }) =>
    apiRequest('/api/v1/monitors/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: string, data: any) =>
    apiRequest(`/api/v1/monitors/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: string) =>
    apiRequest(`/api/v1/monitors/${id}`, {
      method: 'DELETE',
    }),

  toggle: (id: string, enabled: boolean) =>
    apiRequest(`/api/v1/monitors/${id}/toggle`, {
      method: 'POST',
      body: JSON.stringify({ enabled }),
    }),

  checkNow: (id: string) =>
    apiRequest(`/api/v1/monitors/${id}/check-now`, {
      method: 'POST',
    }),

  checks: (id: string, params?: { page?: number; page_size?: number; hours?: number }) => {
    const query = new URLSearchParams();
    if (params?.page) query.set('page', params.page.toString());
    if (params?.page_size) query.set('page_size', params.page_size.toString());
    if (params?.hours) query.set('hours', params.hours.toString());
    return apiRequest(`/api/v1/monitors/${id}/checks?${query.toString()}`);
  },

  pause: (id: string) =>
    apiRequest(`/api/v1/monitors/${id}/toggle`, {
      method: 'POST',
      body: JSON.stringify({ enabled: false }),
    }),

  resume: (id: string) =>
    apiRequest(`/api/v1/monitors/${id}/toggle`, {
      method: 'POST',
      body: JSON.stringify({ enabled: true }),
    }),
};

// Alert Channels API
export const alertChannelsAPI = {
  list: () => apiRequest('/api/v1/alert-channels/'),
  
  create: (data: {
    name: string;
    type: string;
    config: Record<string, any>;
  }) =>
    apiRequest('/api/v1/alert-channels/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  delete: (id: string) =>
    apiRequest(`/api/v1/alert-channels/${id}`, {
      method: 'DELETE',
    }),

  test: (id: string) =>
    apiRequest(`/api/v1/alert-channels/${id}/test`, {
      method: 'POST',
    }),

  linkToMonitor: (monitorId: string, channelId: string) =>
    apiRequest(`/api/v1/alert-channels/${channelId}/attach/${monitorId}`, {
      method: 'POST',
    }),

  unlinkFromMonitor: (monitorId: string, channelId: string) =>
    apiRequest(`/api/v1/alert-channels/${channelId}/detach/${monitorId}`, {
      method: 'POST',
    }),
};

// Analytics API
export const analyticsAPI = {
  overview: () => apiRequest('/api/v1/analytics/overview'),
  
  monitorStats: (monitorId: string, days: number = 7) =>
    apiRequest(`/api/v1/analytics/monitors/${monitorId}?days=${days}`),
  
  monitor: (monitorId: string, days: number = 7) =>
    apiRequest(`/api/v1/analytics/monitors/${monitorId}?days=${days}`),
  
  incidents: (days: number = 7) =>
    apiRequest(`/api/v1/analytics/incidents?days=${days}`),
  percentiles: (monitorId: string, hours: number = 24) =>
    apiRequest(`/api/v1/analytics/monitors/${monitorId}/percentiles?hours=${hours}`),
};

// Subscription API
export const subscriptionAPI = {
  current: () => apiRequest('/api/v1/subscription/'),
  
  get: () => apiRequest('/api/v1/subscription/'),
  
  createCheckout: (variantId: string) =>
    apiRequest('/api/v1/subscription/checkout', {
      method: 'POST',
      body: JSON.stringify({ variant_id: variantId }),
    }),
  
  checkout: (plan: string, billing: string = 'monthly') =>
    apiRequest(`/api/v1/subscription/checkout?plan=${plan}&billing=${billing}`, {
      method: 'POST',
    }),

  cancel: () =>
    apiRequest('/api/v1/subscription/cancel', {
      method: 'POST',
    }),

  billingPortal: () =>
    apiRequest('/api/v1/subscriptions/billing-portal', {
      method: 'POST',
    }),
};

// Public API (no auth)
export const publicApi = {
  statusPage: (username: string) =>
    fetch(`${API_URL}/api/v1/public/${username}/status`).then(r => r.json()),
};

// Legacy aliases for backward compatibility
export const auth = authAPI;

// Maintenance Windows API
export const maintenanceAPI = {
  list: () => apiRequest('/api/v1/maintenance/'),
  create: (data: any) => apiRequest('/api/v1/maintenance/', { method: 'POST', body: JSON.stringify(data) }),
  toggle: (id: string) => apiRequest(`/api/v1/maintenance/${id}/toggle`, { method: 'PATCH' }),
  delete: (id: string) => apiRequest(`/api/v1/maintenance/${id}`, { method: 'DELETE' }),
};


// Assertions API
export const assertionsAPI = {
  list: (monitorId: string) => apiRequest(`/api/v1/monitors/${monitorId}/assertions`),
  save: (monitorId: string, assertions: any[]) =>
    apiRequest(`/api/v1/monitors/${monitorId}/assertions`, {
      method: 'POST',
      body: JSON.stringify(assertions),
    }),
  test: (monitorId: string, responseBody: string, assertions: any[]) =>
    apiRequest(`/api/v1/monitors/${monitorId}/assertions/test`, {
      method: 'POST',
      body: JSON.stringify({ response_body: responseBody, assertions }),
    }),
};

export const monitors = monitorsAPI;
export const alertChannels = alertChannelsAPI;
export const analytics = analyticsAPI;
export const subscriptions = subscriptionAPI;

export default {
  authAPI,
  monitorsAPI,
  alertChannelsAPI,
  analyticsAPI,
  subscriptionAPI,
  publicApi,
};

// AI API
export const aiAPI = {
  analyzeEndpoint: (url: string): Promise<{
    method: string;
    expected_status: number;
    keyword: string | null;
    keyword_present: boolean;
    assertions: { path: string; operator: string; expected: string }[];
    reasoning: string;
    actual_status: number;
  }> =>
    apiRequest('/api/v1/ai/analyze-endpoint', {
      method: 'POST',
      body: JSON.stringify({ url }),
    }),
};

export const teamsAPI = {
  listMembers: () => apiRequest('/api/v1/teams/members'),
  invite: (email: string) =>
    apiRequest('/api/v1/teams/invite', {
      method: 'POST',
      body: JSON.stringify({ email }),
    }),
  removeMember: (memberId: string) =>
    apiRequest(`/api/v1/teams/members/${memberId}`, { method: 'DELETE' }),
  acceptInvite: (token: string) =>
    apiRequest('/api/v1/teams/accept', {
      method: 'POST',
      body: JSON.stringify({ token }),
    }),
  myTeam: () => apiRequest('/api/v1/teams/my-team'),
};
