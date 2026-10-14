// Game layer: the level curve is consistent and XP accrues through the public API.
import test from 'node:test';
import assert from 'node:assert/strict';
import { installStorage } from './_setup.mjs';

installStorage();
const Game = await import('../js/game.js');

test('level curve is monotonic and self-consistent', () => {
  let last = 1;
  for (let xp = 0; xp <= 20000; xp += 37) {
    const lv = Game.levelFromXp(xp);
    assert.ok(lv >= last, `level dropped at ${xp} xp`);
    assert.ok(Game.xpForLevel(lv) <= xp, `xpForLevel(${lv}) > ${xp}`);
    assert.ok(Game.xpForLevel(lv + 1) > xp, `already past level ${lv + 1} at ${xp}`);
    last = lv;
  }
  assert.equal(Game.levelFromXp(0), 1);
  assert.equal(Game.xpForLevel(1), 0);
});

test('ranks are valid and never go backwards as levels rise', () => {
  let lastIdx = -1;
  for (let lv = 1; lv <= 200; lv++) {
    const r = Game.rankFor(lv);
    const idx = Game.RANKS.indexOf(r);
    assert.ok(idx >= 0, `level ${lv}: ${r}`);
    assert.ok(idx >= lastIdx, `rank dropped at level ${lv}`);
    lastIdx = idx;
  }
  assert.equal(Game.rankFor(1), Game.RANKS[0]);
  assert.equal(lastIdx, Game.RANKS.length - 1, 'the top rank is reachable');
});

test('traces, problems and predictions award XP and never go negative', () => {
  Game.resetGame();
  const before = Game.state().xp;
  Game.recordTrace('bubble_sort');
  Game.recordProblemDone();
  Game.recordPrediction(true, 1);
  Game.recordPrediction(false, 0);
  const after = Game.state();
  assert.ok(after.xp > before);
  assert.ok(after.level >= 1);
  assert.ok(Array.isArray(after.unlocked));
  const quests = Game.questState();
  assert.ok(quests.length >= 1);
  assert.ok(quests.every(q => q.id && q.name && q.goal > 0 && q.have >= 0 && typeof q.done === 'boolean'));
  assert.equal(quests.find(q => q.id === 'q_trace3')?.have, 1, 'the trace quest counted the run');
  assert.ok(after.tracesRun >= 1, 'the trace run is counted');
  assert.equal(after.correct, 1); assert.equal(after.wrong, 1);
});
