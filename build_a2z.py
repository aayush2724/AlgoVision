"""Regenerate frontend/js/a2z.js from a2z-source.json — the official sheet.

Provenance: a2z-source.json is decoded from the syllabus payload of
https://takeuforward.org/prep-hub/strivers-a2z-dsa-sheet (20 modules,
495 items). Module names, section names, item titles, order and the
basic/core/pro tier are the real sheet; nothing is hand-authored any more.

Ids are APPEND-ONLY: progress.js and a2zTracers.js key off them, so a row
that already exists keeps its id (matched by title, or by ALIAS when the
sheet reworded it). A row the sheet no longer carries simply disappears;
its id is never reused. New rows get "<module>-<n>" above every n that
prefix ever used.

    python build_a2z.py            # rewrites frontend/js/a2z.js, prints a report
"""
import json
import re
import sys

src = json.load(open('a2z-source.json'))
old_js = open('frontend/js/a2z.js').read()

STR = r'"((?:[^"\\]|\\.)*)"'
ROW = re.compile(r'\{\s*id:' + STR + r',\s*section:' + STR + r',\s*title:' + STR +
                 r',\s*difficulty:"([EMH])",\s*viz:' + STR + r',\s*world:' + STR +
                 r',\s*hook:' + STR + r'((?:,\s*(?:traceable:false|learning:true))*)\s*\}')


def unesc(s):
    return s.replace('\\"', '"').replace('\\\\', '\\')


def norm(t):
    return re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()


OLD_BY_ID, OLD_BY_NORM = {}, {}
for m in ROW.finditer(old_js):
    pid, sec, title, diff, viz, world, hook, _flags = m.groups()
    row = dict(id=pid, section=unesc(sec), title=unesc(title), difficulty=diff,
               viz=unesc(viz), world=unesc(world), hook=unesc(hook))
    OLD_BY_ID[pid] = row
    # A title the sheet lists twice (e.g. the iterative and the recursive
    # "Factorial") keeps both ids: the nth occurrence takes the nth old row.
    OLD_BY_NORM.setdefault(norm(row['title']), []).append(row)

# ── the sheet reworded these; keep the old id (and the student's progress) ──
ALIAS = {
    "Check if the Array is Sorted I": "3-3",
    "Isomorphic Strings": "5-17",
    "Valid Anagram": "5-18",
    "Palindrome Check": "1-68",
    "Largest Element": "3-1",
    "Second Largest Element": "3-2",
    "Majority Element-I": "3-18",
    "Majority Element-II": "3-31",
    "Rearrange array elements by sign": "3-22",
    "Print the matrix in spiral manner": "3-28",
    "Pascal's Triangle III": "3-30",
    "Set Matrix Zeroes": "3-26",
    "Sort an array of 0's 1's and 2's": "3-17",
    "Find the repeating and missing number": "3-38",
    "Maximum Product Subarray in an Array": "3-41",
    "Longest Consecutive Sequence in an Array": "3-25",
    "Longest subarray with sum K": "3-15",
    "Largest Subarray with Sum 0": "3-34",
    "Count subarrays with given xor K": "3-35",
    "Single element in sorted array": "4-39",
    "Find Middle of Linked List": "6-37",
    "Inorder Traversal": "13-38",
    "Check for symmetrical BTs": "13-22",
    "Right/Left View of BT": "13-51",
    "Construct a BT from Postorder and Inorder": "13-61",
    "Morris Inorder Traversal": "13-64",
    "Morris Preorder Traversal": "13-63",
    "Search in BST": "14-18",
    "Inorder successor and predecessor in BST": "14-26",
    "Two sum in BST": "14-28",
    "Bipartite graph": "15-58",
    "Dijkstra's algorithm": "15-64",
    "Grid unique paths": "16-57",
    "Cherry pickup II": "16-61",
    "Subset sum equals to target": "16-62",
    "Minimum coins": "16-64",
    "Coin change II": "16-65",
    "Rod cutting problem": "16-66",
    "Minimum insertions to make string palindrome": "16-68",
}
ALIAS = {norm(k): v for k, v in ALIAS.items()}

# ── scene + framing by topic (only used for rows that are new to the app) ──
VIZ = [
 (r'pattern',                        ('grid', 'Printing Patterns', 'Nested loops, one row at a time.')),
 (r'fundamentals of programming|language basics|librar|complexity|concept basics|learn c\+\+|learn java|learn python|theory',
                                     ('terminal', 'Language Basics', 'Groundwork, not an algorithm.')),
 (r'hash|frequen',                   ('votes', 'Tally Board', 'Count once, look up instantly.')),
 (r'recursion|recursive',            ('fractal', 'Hall of Mirrors', 'A function calling itself needs a way to stop.')),
 (r'sort',                           ('sorting', 'Putting Things In Order', 'Order emerges from repeated comparison.')),
 (r'binary search|search space|on answers',
                                     ('binarysearch', 'Halving the Search', 'Every probe discards half the space.')),
 (r'linked ?list|\bll\b|\bdll\b',    ('linkedlist', 'Train Carriages', 'Each carriage knows only the next.')),
 (r'bit|xor',                        ('circuit', 'Row of Switches', 'Every integer is a row of on/off switches.')),
 (r'stack|queue|monotonic',          ('stackviz', 'Plate Stack', 'The stack remembers what is still open.')),
 (r'window|two pointer|2 pointer',   ('windowslide', 'Sliding Window', 'Grow right, shrink left, never recount.')),
 (r'heap|priority',                  ('heapviz', 'Triage Queue', 'The most urgent rises to the top.')),
 (r'greedy|interval|scheduling',     ('timeline', 'Booking the Day', 'Take the locally best and never look back.')),
 (r'binary search tree|bst',         ('bst', 'Filing Cabinet', 'Left is smaller, right is bigger — always.')),
 (r'tree|traversal',                 ('treeviz', 'Family Tree', 'One root, and every node a smaller tree.')),
 (r'graph|bfs|dfs|topo|shortest|spanning|disjoint|island',
                                     ('graphs', 'Road Network', 'Nodes and edges — the shape of almost everything.')),
 (r'dp|dynamic|subsequence|knapsack|stocks|lis|mcm|partition|squares|grids',
                                     ('dpgrid', 'The Memo Vault', 'Remember the past to conquer the future.')),
 (r'trie|prefix',                    ('trie', 'Prefix Tree', 'Words that start the same share a path.')),
 (r'string|palindrome',              ('dna', 'Genetic Sequence', 'Characters chained together.')),
 (r'math|prime|digit|lcm|gcd|sieve', ('searchbeam', 'Number Theory', 'Arithmetic you can watch.')),
 (r'array|matrix|grid',              ('array', 'Row of Boxes', 'A line of boxes, each with an address.')),
]
# Practice rows with nothing to trace: the 22 printing patterns and the two
# theory items the sheet files under practice.
UNTRACEABLE = re.compile(r'^(pattern[ -]?\d+|requirements needed to construct a unique bt|'
                         r'traversal techniques)$', re.I)
TIER = {'basic': 'E', 'core': 'M', 'pro': 'H'}


def frame(module, section, title):
    hay = f'{title} {section} {module}'.lower()
    for pat, val in VIZ:
        if re.search(pat, hay):
            return val
    return ('array', 'Step Through It', 'Watch it run, one step at a time.')


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


# ── every n each prefix has ever used, so new ids never collide ────────────
used = {}
for pid in OLD_BY_ID:
    p, n = pid.split('-')
    used[p] = max(used.get(p, 0), int(n))

steps_out, taken = [], set()
stats = dict(title=0, alias=0, new=0, untraceable=0, learning=0)
new_rows = []
for mi, mod in enumerate(src['modules'], start=1):
    prefix = str(mi)
    rows = []
    for sec in mod['sections']:
        section = sec['name'].strip() or 'Problems'
        for it in sec['items']:
            t = it['title'].strip()
            k = norm(t)
            old = next((r for r in OLD_BY_NORM.get(k, []) if r['id'] not in taken), None)
            how = 'title'
            if old is None and k in ALIAS and ALIAS[k] not in taken:
                old, how = OLD_BY_ID.get(ALIAS[k]), 'alias'
            if old is not None:
                pid, viz, world, hook = old['id'], old['viz'], old['world'], old['hook']
                stats[how] += 1
            else:
                used[prefix] = used.get(prefix, 0) + 1
                pid = f'{prefix}-{used[prefix]}'
                viz, world, hook = frame(mod['name'], section, t)
                stats['new'] += 1
                new_rows.append((pid, it['kind'], t, section, mod['name']))
            taken.add(pid)
            diff = TIER.get(it.get('difficulty')) or (old or {}).get('difficulty') or 'E'
            learning = it['kind'] != 'practice'
            traceable = not learning and not UNTRACEABLE.match(t)
            if learning:
                stats['learning'] += 1
            if not traceable:
                stats['untraceable'] += 1
            rows.append(dict(id=pid, section=section, title=t, difficulty=diff, viz=viz,
                             world=world, hook=hook, traceable=traceable,
                             learning=learning))
    steps_out.append(dict(step=f'Step {mi}', title=mod['name'].strip(),
                          official=len(rows), problems=rows))

lines = ['''// ── STRIVER'S A2Z SHEET ────────────────────────────────────────────────────
//
// GENERATED by build_a2z.py from a2z-source.json — do not hand-edit; edit the
// generator or refresh the source instead.
//
// Provenance: a2z-source.json is the syllabus of the official sheet at
// takeuforward.org/prep-hub/strivers-a2z-dsa-sheet — 20 modules, 495 items,
// in the sheet's own order, with its section names and basic/core/pro tiers
// (shown as E/M/H). Every row is from the sheet; nothing is hand-authored.
//
// `learning:true` marks the sheet's lecture rows (theory, language basics,
// library tours). `traceable:false` means the row has no algorithm to
// visualise — the lecture rows and the 22 printing patterns — so the viewer
// shows a concept card. A lecture row can still be linked to a tracer in
// a2zTracers.js when one tells its story honestly.
//
// Ids are APPEND-ONLY: progress.js keys off them, so renumbering silently
// reassigns a student's completed work to a different problem. A row keeps
// the id it had on the previous sheet; the numeric prefix is therefore the
// module a row FIRST appeared in, not necessarily where it sits now.

const S = (step, title, official, problems) => ({ step, title, official, progress: 0, problems });

export const A2Z_STEPS = [''']
for st in steps_out:
    lines.append(f'  S("{st["step"]}", "{esc(st["title"])}", {st["official"]}, [')
    last = None
    for r in st['problems']:
        if r['section'] != last:
            lines.append(f'    // {r["section"]}')
            last = r['section']
        extra = ('' if r['traceable'] else ', traceable:false') + (', learning:true' if r['learning'] else '')
        lines.append(
            f'    {{ id:"{r["id"]}", section:"{esc(r["section"])}", title:"{esc(r["title"])}", '
            f'difficulty:"{r["difficulty"]}", viz:"{r["viz"]}", world:"{esc(r["world"])}", '
            f'hook:"{esc(r["hook"])}"{extra} }},')
    lines.append('  ]),')
lines.append('];\n\nexport default A2Z_STEPS;')
open('frontend/js/a2z.js', 'w').write('\n'.join(lines) + '\n')

total = sum(len(s['problems']) for s in steps_out)
gone = sorted((pid for pid in OLD_BY_ID if pid not in taken),
              key=lambda p: tuple(int(x) for x in p.split('-')))
print(f"modules {len(steps_out)} | rows {total} | official {src['officialTotal']}")
print(f"kept by title {stats['title']} | kept by alias {stats['alias']} | new {stats['new']} "
      f"| lecture rows {stats['learning']} | untraceable {stats['untraceable']}")
print(f"old rows no longer on the sheet: {len(gone)}")
if '--report' in sys.argv:
    for pid in gone:
        print(f"  gone {pid:7s} {OLD_BY_ID[pid]['title']}")
    for pid, kind, t, sec, modn in new_rows:
        print(f"  new  {pid:7s} [{kind[:4]}] {t}   ({modn} / {sec})")
