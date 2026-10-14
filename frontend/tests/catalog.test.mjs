// The catalog modules are plain data: everything the pages rely on must agree.
//   node --no-warnings --test frontend/tests/
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const F = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DATA = await import(path.join(F, 'js/data.js'));
const { A2Z_TRACER } = await import(path.join(F, 'js/a2zTracers.js'));
const { A2Z_STEPS } = await import(path.join(F, 'js/a2z.js'));
const ids = DATA.ALGORITHMS.map(a => a.id);
const idSet = new Set(ids);

test('every algorithm has a unique id and the fields the pages read', () => {
  assert.equal(idSet.size, ids.length, 'duplicate ids');
  for (const a of DATA.ALGORITHMS) {
    for (const k of ['id', 'name', 'category', 'emoji', 'complexity', 'input', 'hook']) {
      assert.ok(typeof a[k] === 'string' && a[k].trim(), `${a.id}.${k}`);
    }
    assert.ok(DATA.ALGO_CATEGORIES.includes(a.category), `${a.id}: unknown category ${a.category}`);
    assert.ok(['graph', 'array', 'text', 'number'].includes(a.input), `${a.id}: input ${a.input}`);
  }
});

test('every algorithm has a complexity card whose reading is a sentence', () => {
  for (const id of ids) {
    const card = DATA.COMPLEXITY[id];
    assert.ok(card, `${id}: no card`);
    assert.ok(Array.isArray(card.rows) && card.rows.length >= 2, `${id}: rows`);
    for (const row of card.rows) assert.ok(row.length === 2 && row[0] && row[1], `${id}: row ${row}`);
    for (const [counts, sizes] of [
      [{ comparisons: 3, swaps: 1 }, { n: 6, V: 0, E: 0 }],
      [{}, { n: 0, V: 0, E: 0 }],
      [{ relaxations: 4, visits: 1 }, { n: 7, V: 7, E: 8 }],
    ]) {
      const text = card.reading(counts, sizes);
      assert.ok(typeof text === 'string' && text.length > 10, `${id}: reading`);
      assert.ok(!/undefined|NaN|\[object/.test(text), `${id}: ${text}`);
    }
  }
});

test('derived lists resolve to catalog entries', () => {
  assert.ok(DATA.GRAPH_ALGORITHMS.length >= 10);
  assert.equal(DATA.SORT_ALGORITHMS.length, 6);
  for (const a of [...DATA.GRAPH_ALGORITHMS, ...DATA.SORT_ALGORITHMS]) assert.ok(idSet.has(a.id));
  for (const id of ids) assert.ok(DATA.capLabel(DATA.ALGORITHMS.find(a => a.id === id)).length <= 5, `${id}: cap label`);
});

test('every A2Z link, offline sample and pseudocode entry points at a real algorithm', () => {
  const rows = A2Z_STEPS.flatMap(s => s.problems);
  const rowIds = new Set(rows.map(r => r.id));
  assert.equal(rowIds.size, rows.length, 'duplicate A2Z row ids');
  for (const [row, algo] of Object.entries(A2Z_TRACER)) {
    assert.ok(rowIds.has(row), `A2Z_TRACER row ${row} is not on the sheet`);
    assert.ok(idSet.has(algo), `A2Z_TRACER ${row} -> ${algo}`);
  }
  const offline = new Set(readdirSync(path.join(F, 'offline')).filter(f => f.endsWith('.json')).map(f => f.slice(0, -5)));
  for (const id of ids) assert.ok(offline.has(id), `${id}: no offline sample`);
  const pseudo = JSON.parse(readFileSync(path.join(F, 'data/pseudocode.json'), 'utf8'));
  delete pseudo._about;
  for (const [id, lines] of Object.entries(pseudo)) {
    assert.ok(idSet.has(id), `pseudocode for unknown ${id}`);
    assert.ok(lines.some(l => l.when), `${id}: no line is ever lit`);
    for (const l of lines) if (l.when) assert.doesNotThrow(() => new RegExp(l.when, 'i'), `${id}: bad regex ${l.when}`);
  }
  for (const id of ids) assert.ok(pseudo[id], `${id}: no pseudocode`);
});

test('hooks read as a story, not an input format', () => {
  const instruction = /rows split by|comma|separated|\bup to \d|\(up to|split by|\| |Ops:|^Pairs:|^Edges:|^Input:|format|e\.g\.|^Words:|^Text then|^Array,|^Values:|^Numbers:/i;
  for (const a of DATA.ALGORITHMS) assert.ok(!instruction.test(a.hook), `${a.id}: ${a.hook}`);
});

test('the site facts the legal pages read are present', () => {
  assert.ok(existsSync(path.join(F, 'js/site.js')));
});
