// Minimal browser shims so the storage-backed modules can run under node:test.
// Import this before progress.js / game.js.
export function installStorage({ blocked = false } = {}) {
  const store = new Map();
  globalThis.localStorage = {
    getItem: (k) => { if (blocked) throw new Error('blocked'); return store.has(k) ? store.get(k) : null; },
    setItem: (k, v) => { if (blocked) throw new Error('blocked'); store.set(k, String(v)); },
    removeItem: (k) => { if (blocked) throw new Error('blocked'); store.delete(k); },
    clear: () => store.clear(),
  };
  if (!globalThis.window) globalThis.window = globalThis;
  if (!globalThis.document) globalThis.document = { dispatchEvent() { return true; } };
  if (!globalThis.CustomEvent) globalThis.CustomEvent = class CustomEvent { constructor(type, init) { this.type = type; this.detail = init?.detail; } };
  return store;
}
