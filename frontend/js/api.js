const BASE_URL = window.ALGOVISION_API || "http://localhost:8000";

async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 10000); // 10s timeout
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: { "Content-Type": "application/json", ...options.headers },
    });
    clearTimeout(timer);
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Request failed: ${response.status}`);
    }
    return response.json();
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

export const api = {
  async getAlgorithms() {
    return request("/api/trace/algorithms");
  },

  async postTrace(algorithm, start, graph) {
    return request("/api/trace", {
      method: "POST",
      body: JSON.stringify({ algorithm, start, graph }),
    });
  },

  async explainStep(algorithm, step, level = "beginner", realtWorldMeta = {}) {
    return request("/api/ai/explain", {
      method: "POST",
      body: JSON.stringify({ algorithm, step, level, realworld_meta: realtWorldMeta }),
    });
  },

  async bugFind(language, code) {
    return request("/api/ai/bugfind", {
      method: "POST",
      body: JSON.stringify({ language, code }),
    });
  },

  async detect(code, problem = "") {
    return request("/api/detect", {
      method: "POST",
      body: JSON.stringify({ code, problem }),
    });
  },
};
