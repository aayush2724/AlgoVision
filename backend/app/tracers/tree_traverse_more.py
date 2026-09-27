"""Tree traversals without recursion — the stack made visible.

Recursion keeps its pending work on the call stack; these walks keep it on an
explicit stack you can watch:

* iter_preorder — pop a node, visit it, push right then left (so left pops
  first).
* iter_inorder — slide left pushing every node; when you can't, pop, visit,
  then step right.
* postorder_two_stacks — stack 1 produces root-right-left; pouring it into
  stack 2 reverses that into left-right-root.
* postorder_one_stack — slide left; at the top of the stack, go right if the
  right child hasn't been done yet, otherwise visit and pop.
* zigzag_traversal — level order, but every other level is read right to left.

Uses the `tree` view via bt_common: the node being handled is orange, visited
nodes are green; the note shows the stack and the output so far.
"""

from collections import deque

from app.tracers import bt_common as bt

TITLES = {
    "iter_preorder": "Iterative Preorder Traversal",
    "iter_inorder": "Iterative Inorder Traversal",
    "postorder_two_stacks": "Postorder With Two Stacks",
    "postorder_one_stack": "Postorder With One Stack",
    "zigzag_traversal": "Zigzag Level Order Traversal",
}


def run(algo, text, target=None):
    return trace(algo, bt.build(bt.parse(text)))


def trace(algo, nodes):
    s = bt.Stepper(nodes)
    s.counts = {"pushes": 0, "pops": 0}
    V = lambda i: bt.val(nodes, i)
    out: list = []
    done: list = []

    def show(stack):
        return "[" + ", ".join(str(V(i)) for i in stack) + "]"

    if algo == "iter_preorder":
        stack = [0]
        s.counts["pushes"] += 1
        s.add(f"Preorder is root, left, right. Start with the root on the "
              f"stack. Stack {show(stack)}.", 0)
        while stack:
            n = stack.pop()
            s.counts["pops"] += 1
            out.append(V(n))
            done.append(n)
            for c in (nodes[n]["right"], nodes[n]["left"]):
                if c is not None:
                    stack.append(c)
                    s.counts["pushes"] += 1
            s.add(f"Pop {V(n)} and visit it. Push its right child, then its left "
                  f"(so the left comes off first). Stack {show(stack)}. "
                  f"Output {out}.", n, done)
    elif algo == "iter_inorder":
        stack: list = []
        cur = 0
        s.add("Inorder is left, root, right. Slide left pushing every node; "
              "when you can't go further, pop and visit, then turn right.")
        while cur is not None or stack:
            if cur is not None:
                stack.append(cur)
                s.counts["pushes"] += 1
                s.add(f"Push {V(cur)} and keep going left. Stack {show(stack)}.",
                      cur, done)
                cur = nodes[cur]["left"]
            else:
                n = stack.pop()
                s.counts["pops"] += 1
                out.append(V(n))
                done.append(n)
                s.add(f"Nothing further left — pop {V(n)} and visit it, then "
                      f"try its right subtree. Output {out}.", n, done)
                cur = nodes[n]["right"]
    elif algo == "postorder_two_stacks":
        s1, s2 = [0], []
        s.add("Postorder is left, right, root. Stack 1 pops root first and pushes "
              "left then right, producing root-right-left into stack 2 — which "
              "reads back as left-right-root.", 0)
        while s1:
            n = s1.pop()
            s.counts["pops"] += 1
            s2.append(n)
            for c in (nodes[n]["left"], nodes[n]["right"]):
                if c is not None:
                    s1.append(c)
                    s.counts["pushes"] += 1
            s.add(f"Move {V(n)} from stack 1 to stack 2; push its children onto "
                  f"stack 1. Stack 1 {show(s1)}, stack 2 {show(s2)}.", n, done)
        while s2:
            n = s2.pop()
            out.append(V(n))
            done.append(n)
            s.add(f"Empty stack 2: {V(n)} comes out. Output {out}.", n, done)
    elif algo == "postorder_one_stack":
        stack: list = []
        cur, last = 0, None
        s.add("One stack: slide left pushing nodes. At the top, go right if that "
              "subtree isn't done yet; otherwise the node is finished — visit it.")
        while cur is not None or stack:
            if cur is not None:
                stack.append(cur)
                s.counts["pushes"] += 1
                s.add(f"Push {V(cur)}, keep going left. Stack {show(stack)}.",
                      cur, done)
                cur = nodes[cur]["left"]
                continue
            top = stack[-1]
            r = nodes[top]["right"]
            if r is not None and last != r:
                s.add(f"Top is {V(top)}: its right child {V(r)} isn't done — go "
                      f"there first.", top, done)
                cur = r
            else:
                stack.pop()
                s.counts["pops"] += 1
                out.append(V(top))
                done.append(top)
                last = top
                s.add(f"Top is {V(top)} and both its subtrees are done — visit "
                      f"and pop it. Output {out}.", top, done)
    else:
        q = deque([0])
        left_to_right = True
        level = 0
        s.add("Zigzag: an ordinary level-order queue, but every other level is "
              "written out right to left.")
        while q:
            ids = list(q)
            q.clear()
            for n in ids:
                q.extend(bt.kids(nodes, n))
            row = [V(n) for n in ids]
            if not left_to_right:
                row.reverse()
            out.append(row)
            done.extend(ids)
            s.add(f"Level {level} read "
                  f"{'left → right' if left_to_right else 'right → left'}: {row}.",
                  ids[-1 if left_to_right else 0], done)
            left_to_right = not left_to_right
            level += 1
    s.add(f"Done: {out}. Every node was pushed and popped at most "
          f"{'twice' if algo == 'postorder_two_stacks' else 'once'} — O(n).",
          None, done)
    return bt.result(algo, s.steps, out)
