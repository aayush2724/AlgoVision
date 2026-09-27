"""Letter Combinations of a Phone Number — one level per digit.

Each digit 2–9 maps to 3 or 4 letters on a phone keypad. The recursion takes
the next digit and branches once per letter it could stand for; after the
last digit, the path spells one combination. The tree's width multiplies at
every level (3 × 3, 3 × 4, …), which is why the answer count grows so fast.

Uses the `tree` view through RecTree with n-ary children; the finished words
glow green.
"""

from app.tracers.recursion_tree import RecTree

MAX_DIGITS = 2
KEYPAD = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno",
          "7": "pqrs", "8": "tuv", "9": "wxyz"}


def trace(digits: str):
    t = RecTree()
    counts = {"calls": 0, "words": 0}
    out: list = []

    t.event(None, f"Digits \"{digits}\": each one could be any of its keypad "
                  f"letters ({', '.join(f'{d}→{KEYPAD[d]}' for d in digits)}). "
                  f"Branch once per letter, one level per digit.", counts)

    def rec(i, prefix, parent):
        counts["calls"] += 1
        nid = t.node(prefix or "·", parent, side=None)
        if i == len(digits):
            counts["words"] += 1
            out.append(prefix)
            t.event(nid, f"All digits used — \"{prefix}\" is a combination.",
                    counts, good=True)
            return
        d = digits[i]
        t.event(nid, f"Next digit {d} can be {', '.join(KEYPAD[d])} — one "
                     f"branch each.", counts)
        for ch in KEYPAD[d]:
            rec(i + 1, prefix + ch, nid)

    rec(0, "", None)
    t.event(None, f"{counts['words']} combinations: {', '.join(out)}. That is "
                  f"the product of the letters per digit.", counts)
    return {
        "meta": {"algorithm": "letter_combinations", "view": "tree",
                 "language": "python", "result": out, "nodes": t.size()},
        "steps": t.steps(),
    }
