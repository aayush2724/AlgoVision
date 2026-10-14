// Progress store: survives reloads, rejects bad imports, and works with storage blocked.
import test from 'node:test';
import assert from 'node:assert/strict';
import { installStorage } from './_setup.mjs';

const store = installStorage();
const P = await import('../js/progress.js');

test('viewing, completing and tracing update the stats and persist', () => {
  P.resetAll();
  P.markViewed('2-1');
  assert.equal(P.getStatus('2-1'), 'viewed');
  P.toggleCompleted('2-1');
  assert.equal(P.getStatus('2-1'), 'completed');
  P.recordTraceRun('bubble_sort');
  P.recordTraceRun('bubble_sort');
  P.recordTraceRun('merge_sort');
  const s = P.stats();
  assert.equal(s.completed, 1);
  assert.equal(s.tracesRun, 3);
  assert.equal(s.algorithmsTraced, 2);
  assert.ok(s.streak >= 1);
  assert.ok(store.get('algovision.progress.v1').includes('"2-1":"completed"'));
  assert.equal(P.toggleCompleted('2-1'), 'viewed', 'toggling again un-completes');
});

test('export/import round-trips and garbage is refused without touching the store', () => {
  P.resetAll();
  P.markViewed('3-8');
  P.recordTraceRun('dfs');
  const dump = P.exportJSON();
  const parsed = JSON.parse(dump);
  assert.deepEqual(Object.keys(parsed).sort(), ['days', 'exported', 'problems', 'traces', 'version']);
  P.resetAll();
  assert.equal(P.stats().tracesRun, 0);
  assert.equal(P.importJSON(dump).ok, true);
  assert.equal(P.getStatus('3-8'), 'viewed');
  assert.equal(P.stats().tracesRun, 1);
  assert.equal(P.importJSON('{not json').ok, false);
  assert.equal(P.importJSON('{"hello": 1}').ok, false);
  assert.equal(P.getStatus('3-8'), 'viewed', 'a refused import leaves the store alone');
  const hostile = P.importJSON(JSON.stringify({ problems: { ['x'.repeat(40)]: 'completed', '1-1': 'hacked' }, traces: { bfs: 1e12, dfs: 'NaN' } }));
  assert.equal(hostile.ok, true);
  assert.equal(P.getStatus('1-1'), 'unseen', 'unknown statuses are dropped');
  assert.ok(P.stats().tracesRun <= 100000, 'trace counts are clamped');
});

test('with storage blocked nothing throws and reads fall back to empty state', async () => {
  installStorage({ blocked: true });
  assert.doesNotThrow(() => { P.markViewed('1-1'); P.recordTraceRun('bfs'); P.toggleCompleted('1-1'); });
  assert.equal(P.getStatus('1-1'), 'unseen');
  assert.equal(P.stats().tracesRun, 0);
  assert.equal(P.hasAnyActivity(), false);
  installStorage();
});
