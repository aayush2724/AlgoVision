const BASE_URL = (() => {
  if (typeof window === 'undefined') return '';
  const api = window.ALGOVISION_API;
  return (api !== undefined && api !== null) ? api : '';
})();

// Safe user-facing error messages — never expose server internals
const SAFE_ERRORS = {
  400: 'Invalid request. Please check your input.',
  413: 'Input too large. Please reduce the code length.',
  429: 'Too many requests. Please wait a moment and try again.',
  500: 'Server error. Please try again shortly.',
  503: 'Service temporarily unavailable.',
};

async function request(path, options = {}) {
  const url      = `${BASE_URL}${path}`;
  const controller = new AbortController();
  const timer    = setTimeout(() => controller.abort(), 12000);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json', ...options.headers },
    });
    clearTimeout(timer);

    if (!response.ok) {
      // Use safe message — never expose response.json() detail to UI
      const safeMsg = SAFE_ERRORS[response.status]
        || `Request failed (${response.status}).`;
      // Log full detail to console only (not shown to user)
      response.json()
        .then(d => console.warn(`API ${path} error:`, d.detail || d))
        .catch(() => {});
      throw new ApiError(safeMsg, response.status);
    }

    return response.json();

  } catch (err) {
    clearTimeout(timer);
    if (err instanceof ApiError) throw err;
    if (err.name === 'AbortError') {
      throw new ApiError('Request timed out. Check your connection.', 0);
    }
    // Network error — safe message only
    console.warn(`API ${path} network error:`, err.message);
    throw new ApiError('Could not reach the server. Using offline mode.', 0);
  }
}

// Custom error class so callers can distinguish API errors from
// programming errors without exposing server detail strings
export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name   = 'ApiError';
    this.status = status;
  }
}

export const api = {
  async getAlgorithms() {
    return request('/api/trace/algorithms');
  },

  async postTrace(algorithm, start, graph) {
    return request('/api/trace', {
      method: 'POST',
      body: JSON.stringify({ algorithm, start, graph }),
    });
  },

  async explainStep(algorithm, step, level = 'beginner', realWorldMeta = {}) {
    return request('/api/ai/explain', {
      method: 'POST',
      body: JSON.stringify({
        algorithm, step, level,
        realworld_meta: realWorldMeta,
      }),
    });
  },

  async bugFind(language, code) {
    // Client-side size guard before even sending
    if (code.length > 7500) {
      throw new ApiError(
        'Code is too long. Please paste under 200 lines.', 0
      );
    }
    return request('/api/ai/bugfind', {
      method: 'POST',
      body: JSON.stringify({ language, code }),
    });
  },

  async detect(code, problem = '') {
    if (code.length > 7500) {
      // Fall back to client-side detection silently — don't show error
      return null;
    }
    return request('/api/detect', {
      method: 'POST',
      body: JSON.stringify({ code, problem }),
    });
  },
};
