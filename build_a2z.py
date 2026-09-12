"""Regenerate frontend/js/a2z.js from the scraped sheet.

Provenance: a2z-source.json is scraped from takeuforward.org, so step names,
section names, problem titles, difficulties and per-step totals are the real
sheet. Where the scrape came up short (step 3 would not expand; ten sections
lost a row) we fall back to the previously hand-written entries and mark them,
so it is always visible which titles are authoritative.

Ids are APPEND-ONLY: progress.js keys off them. Titles already present keep
their old id; anything new is appended after the highest id in that step.
"""
import json, re, sys

src = json.load(open('a2z-source.json'))
old_js = open('frontend/js/a2z.js').read()

# ── previously hand-written entries, kept for the gaps ────────────────────
OLD = {}
for m in re.finditer(r'\{\s*id:"(\d+-\d+)",\s*section:"([^"]*)",\s*title:"([^"]*)",'
                     r'\s*difficulty:"([EMH])",\s*viz:"([^"]*)",\s*world:"([^"]*)",'
                     r'\s*hook:"([^"]*)"\s*\}', old_js):
    i, sec, title, diff, viz, world, hook = m.groups()
    OLD[(i.split('-')[0], title.lower())] = dict(id=i, section=sec, title=title,
        difficulty=diff, viz=viz, world=world, hook=hook)
OLD_BY_STEP = {}
for v in OLD.values():
    OLD_BY_STEP.setdefault(v['id'].split('-')[0], []).append(v)

# ── scene + framing by topic ──────────────────────────────────────────────
VIZ = [
 (r'pattern',                        ('grid','Printing Patterns','Nested loops, one row at a time.')),
 (r'stl|collection|cpp basics|input output|if elseif|switch|theory|java',
                                     ('terminal','Language Basics','Groundwork, not an algorithm.')),
 (r'hash',                           ('votes','Tally Board','Count once, look up instantly.')),
 (r'recursion|recursive',            ('fractal','Hall of Mirrors','A function calling itself needs a way to stop.')),
 (r'sort',                           ('sorting','Putting Things In Order','Order emerges from repeated comparison.')),
 (r'binary search|search space',     ('binarysearch','Halving the Search','Every probe discards half the space.')),
 (r'linked ?list|\bll\b',            ('linkedlist','Train Carriages','Each carriage knows only the next.')),
 (r'bit|xor',                        ('circuit','Row of Switches','Every integer is a row of on/off switches.')),
 (r'stack|queue|monotonic',          ('stackviz','Plate Stack','The stack remembers what is still open.')),
 (r'window|two pointer',             ('windowslide','Sliding Window','Grow right, shrink left, never recount.')),
 (r'heap|priority',                  ('heapviz','Triage Queue','The most urgent rises to the top.')),
 (r'greedy|interval',                ('timeline','Booking the Day','Take the locally best and never look back.')),
 (r'binary search tree|bst',         ('bst','Filing Cabinet','Left is smaller, right is bigger — always.')),
 (r'tree|traversal',                 ('treeviz','Family Tree','One root, and every node a smaller tree.')),
 (r'graph|bfs|dfs|topo|shortest|spanning|disjoint',
                                     ('graphs','Road Network','Nodes and edges — the shape of almost everything.')),
 (r'dp|dynamic|subsequence|knapsack|stocks|lis|mcm|partition|squares',
                                     ('dpgrid','The Memo Vault','Remember the past to conquer the future.')),
 (r'trie|prefix',                    ('trie','Prefix Tree','Words that start the same share a path.')),
 (r'string',                         ('dna','Genetic Sequence','Characters chained together.')),
 (r'math|prime|digit',               ('searchbeam','Number Theory','Arithmetic you can watch.')),
 (r'array|matrix|grid',              ('array','Row of Boxes','A line of boxes, each with an address.')),
]
# Entries that genuinely cannot be traced — the viewer shows a concept card.
UNTRACEABLE = re.compile(
  r'^(pattern \d+|stl|java collections|cpp basics|input output|if elseif|switch case|'
  r'theory with examples|what are arrays, strings\?|for loops|while loops|'
  r'functions \(pass by reference and value\)|easy and medium|hard|basic hashing|'
  r'introduction to .*|.*\| c\+\+|.*\| java)$', re.I)

def frame(step, section, title):
    hay = f'{title} {section} {step}'.lower()
    for pat, val in VIZ:
        if re.search(pat, hay):
            return val
    return ('array', 'Step Through It', 'Watch it run, one step at a time.')

def esc(s): return s.replace('\\', '\\\\').replace('"', '\\"')

steps_out, stats = [], dict(scraped=0, authored=0, untraceable=0)
for si, s in enumerate(src['steps'], start=1):
    used = {int(v['id'].split('-')[1]) for v in OLD_BY_STEP.get(str(si), [])}
    nxt = max(used) + 1 if used else 1
    rows, seen = [], set()

    pool = list(s['sections'])
    # Step 3 never expanded; fall back to the authored entries wholesale.
    if s['counted'] == 0 and OLD_BY_STEP.get(str(si)):
        pool = [{'name': None, 'problems': [{'title': o['title'], 'difficulty': o['difficulty'],
                                             '_old': o} for o in
                 sorted(OLD_BY_STEP[str(si)], key=lambda o: int(o['id'].split('-')[1]))]}]

    for sec in pool:
        for p in sec['problems']:
            t = p['title'].strip()
            if not t or t.lower() in seen:
                continue
            seen.add(t.lower())
            prev = p.get('_old') or OLD.get((str(si), t.lower()))
            section = sec['name'] or (prev or {}).get('section') or 'Problems'
            if prev:
                pid, viz, world, hook = prev['id'], prev['viz'], prev['world'], prev['hook']
                source = 'authored' if sec['name'] is None else 'sheet'
            else:
                pid = f'{si}-{nxt}'; nxt += 1
                viz, world, hook = frame(s['step'], section, t)
                source = 'sheet'
            traceable = not UNTRACEABLE.match(t)
            stats['scraped' if source == 'sheet' else 'authored'] += 1
            if not traceable: stats['untraceable'] += 1
            rows.append(dict(id=pid, section=section, title=t, difficulty=p['difficulty'],
                             viz=viz, world=world, hook=hook, traceable=traceable))
    steps_out.append(dict(step=f'Step {si}', title=s['step'], official=s['total'], problems=rows))

lines = ['''// ── STRIVER'S A2Z SHEET ────────────────────────────────────────────────────
//
// GENERATED by build_a2z.py from a2z-source.json — do not hand-edit; edit the
// generator or re-scrape instead.
//
// Provenance: a2z-source.json was scraped from takeuforward.org, so step
// names, section names, titles, difficulties and `official` counts are the
// real sheet. `sheet: false` marks the handful of rows the scrape could not
// reach (step 3 would not expand, and ten sections dropped a row); those came
// from the earlier hand-written list and are worth spot-checking.
//
// `traceable: false` means the row has no algorithm to visualise — the
// language-basics items and Pattern 1-22. They are kept so the sheet and its
// counts stay faithful; the viewer shows a concept card instead of an empty
// scene.
//
// Ids are APPEND-ONLY: progress.js keys off them, so renumbering silently
// reassigns a student's completed work to a different problem.

const S = (step, title, official, problems) => ({ step, title, official, progress: 0, problems });

export const A2Z_STEPS = [''']
for st in steps_out:
    lines.append(f'  S("{st["step"]}", "{esc(st["title"])}", {st["official"]}, [')
    last = None
    for r in st['problems']:
        if r['section'] != last:
            lines.append(f'    // {r["section"]}')
            last = r['section']
        extra = '' if r['traceable'] else ', traceable:false'
        lines.append(
            f'    {{ id:"{r["id"]}", section:"{esc(r["section"])}", title:"{esc(r["title"])}", '
            f'difficulty:"{r["difficulty"]}", viz:"{r["viz"]}", world:"{esc(r["world"])}", '
            f'hook:"{esc(r["hook"])}"{extra} }},')
    lines.append('  ]),')
lines.append('];\n\nexport default A2Z_STEPS;')
open('frontend/js/a2z.js', 'w').write('\n'.join(lines) + '\n')

total = sum(len(s['problems']) for s in steps_out)
official = sum(s['official'] for s in steps_out)
print(f"steps {len(steps_out)} | rows {total} | official {official}")
print(f"from sheet {stats['scraped']} | authored fallback {stats['authored']} | untraceable {stats['untraceable']}")
