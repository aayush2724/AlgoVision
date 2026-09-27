"""Palindrome Partitioning — cut a string into pieces that are all palindromes.

Each call owns the rest of the string from `start`. It loops over every
possible next piece s[start..end]; only pieces that read the same both ways
become children (the others are never built), and the child continues from
end+1. Reaching the end of the string means every piece was a palindrome —
the root-to-leaf path is one partition.

Uses the `tree` view through RecTree with n-ary children; each node is
labelled with the piece it cut, answer leaves glow green.
"""

from app.tracers.recursion_tree import RecTree

MAX_LEN = 6
MAX_NODES = 45


def trace(text: str):
    s = text
    t = RecTree()
    counts = {"calls": 0, "pieces_rejected": 0, "partitions": 0}
    out: list = []

    t.event(None, f"Cut \"{s}\" into pieces that are all palindromes. Each "
                  f"call tries every next piece; only palindromic pieces get "
                  f"a branch.", counts)

    def rec(start, parts, parent, label):
        counts["calls"] += 1
        nid = t.node(label, parent, side=None)
        if start == len(s):
            counts["partitions"] += 1
            out.append(list(parts))
            t.event(nid, f"Reached the end: {' | '.join(parts)} — every piece "
                         f"is a palindrome.", counts, good=True)
            return
        bad = [s[start:end + 1] for end in range(start, len(s))
               if s[start:end + 1] != s[start:end + 1][::-1]]
        counts["pieces_rejected"] += len(bad)
        where = "the start" if not parts else f"after {' | '.join(parts)}"
        t.event(nid, f"Cutting {where}: try each next piece of "
                     f"\"{s[start:]}\"."
                     + (f" Not palindromes, so no branch: {', '.join(bad)}."
                        if bad else " Every prefix is a palindrome."),
                counts)
        for end in range(start, len(s)):
            piece = s[start:end + 1]
            if piece == piece[::-1]:
                parts.append(piece)
                rec(end + 1, parts, nid, piece)
                parts.pop()

    rec(0, [], None, "·")
    shown = "; ".join(" | ".join(p) for p in out)
    t.event(None, f"{counts['partitions']} partition(s): {shown}. "
                  f"{counts['pieces_rejected']} non-palindromic pieces were "
                  f"never branched on.", counts)
    return {
        "meta": {"algorithm": "palindrome_partition", "view": "tree",
                 "language": "python", "result": out, "nodes": t.size()},
        "steps": t.steps(),
    }
