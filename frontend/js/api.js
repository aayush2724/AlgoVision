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

// A sleeping free-tier backend (Render) takes 20–30 s to answer its first
// request. Tracing and the reachability probe wait that out; everything else
// (detect, narration, bug finder) keeps the short budget.
const DEFAULT_TIMEOUT = 12000;
const WAKE_TIMEOUT = 45000;

// The backend's own 400s are hand-written for students ("Max 16 numbers —
// the trace is unreadable beyond that"). Those are worth showing verbatim;
// anything longer, markup-like or non-400 stays behind the generic message.
function displayableDetail(status, detail) {
  if (status !== 400 || typeof detail !== 'string') return null;
  const text = detail.trim();
  if (!text || text.length > 200 || /[<>]/.test(text)) return null;
  return text;
}

async function request(path, options = {}, timeoutMs = DEFAULT_TIMEOUT) {
  const url      = `${BASE_URL}${path}`;
  const controller = new AbortController();
  const timer    = setTimeout(() => controller.abort(), timeoutMs);
  // Callers can hand in their own signal (e.g. to drop a stale detect when
  // the user keeps typing); either side aborting cancels the fetch.
  const { signal: outer, ...rest } = options;
  if (outer) {
    if (outer.aborted) controller.abort();
    else outer.addEventListener('abort', () => controller.abort(), { once: true });
  }

  try {
    const response = await fetch(url, {
      ...rest,
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json', ...rest.headers },
    });
    clearTimeout(timer);

    if (!response.ok) {
      let detail = null;
      try { detail = (await response.json())?.detail; } catch { /* no body */ }
      // Full detail goes to the console only; the UI gets a safe message.
      console.warn(`API ${path} error:`, detail ?? response.status);
      const safeMsg = displayableDetail(response.status, detail)
        || SAFE_ERRORS[response.status]
        || `Request failed (${response.status}).`;
      throw new ApiError(safeMsg, response.status);
    }

    return response.json();

  } catch (err) {
    clearTimeout(timer);
    if (err instanceof ApiError) throw err;
    if (err.name === 'AbortError') {
      if (outer?.aborted) throw new ApiError('Request cancelled.', 0, true);
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
  constructor(message, status, cancelled = false) {
    super(message);
    this.name   = 'ApiError';
    this.status = status;
    this.cancelled = cancelled;
  }
}

export const api = {
  async getAlgorithms() {
    return request('/api/trace/algorithms', {}, WAKE_TIMEOUT);
  },

  // payload: { start, graph } for graph algorithms,
  //          { array, target } for array algorithms.
  async postTrace(algorithm, payload) {
    return request('/api/trace', {
      method: 'POST',
      body: JSON.stringify({ algorithm, ...payload }),
    }, WAKE_TIMEOUT);
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

  async detect(code, problem = '', { signal } = {}) {
    if (code.length > 7500) {
      // Fall back to client-side detection silently — don't show error
      return null;
    }
    return request('/api/detect', {
      method: 'POST',
      body: JSON.stringify({ code, problem }),
      signal,
    });
  },
};
