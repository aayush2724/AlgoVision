const BASE_URL = window.ALGOVISION_API || "http://localhost:8000";

async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Request failed: ${response.status}`);
  }

  return response.json();
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

  async explainStep(algorithm, step, level = "beginner") {
    return request("/api/ai/explain", {
      method: "POST",
      body: JSON.stringify({ algorithm, step, level }),
    });
  },

  async bugFind(language, code) {
    return request("/api/ai/bugfind", {
      method: "POST",
      body: JSON.stringify({ language, code }),
    });
  }
};
