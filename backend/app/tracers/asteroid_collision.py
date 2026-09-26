"""Asteroid Collision — a stack of survivors.

Each value is an asteroid: the size is |v|, the sign is its direction (+ right,
− left). Only a left-mover meeting a right-mover already on the stack can
collide; the smaller explodes, equal sizes both explode. Right-movers and
left-movers with nothing to hit are simply pushed. Each asteroid is pushed and
popped at most once: O(n).

Reuses the `array` view: the incoming asteroid is `placed`, and asteroids
still alive on the stack are green via `sorted_ranges`. No new renderer.
"""

MAX_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def _dir(v):
    return f"{_fmt(abs(v))}→" if v > 0 else f"←{_fmt(abs(v))}"


def trace(asteroids: list):
    arr = list(asteroids)
    steps: list = []
    counts = {"pushes": 0, "collisions": 0}
    stack: list[int] = []        # indices of survivors so far

    def add(note, placed=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "sorted_ranges": [[j, j] for j in stack],
                "stack": stack[:],
                "stack_values": [arr[j] for j in stack],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    def alive():
        return [_dir(arr[j]) for j in stack] or "(empty)"

    if not arr:
        add("No asteroids — nothing collides.")
        return _result(arr, steps, [])

    add("Positive = moving right, negative = moving left. Only a left-mover "
        "can hit a right-mover already on the stack. Survivors stay green.")

    for i, v in enumerate(arr):
        alive_now = True
        while alive_now and v < 0 and stack and arr[stack[-1]] > 0:
            top = stack[-1]
            counts["collisions"] += 1
            if arr[top] < -v:
                stack.pop()
                add(f"{_dir(v)} hits {_dir(arr[top])} — {_fmt(arr[top])} is "
                    f"smaller and explodes; {_dir(v)} keeps going.", placed=i)
            elif arr[top] == -v:
                stack.pop()
                alive_now = False
                add(f"{_dir(v)} hits {_dir(arr[top])} — same size, both "
                    f"explode.", placed=i)
            else:
                alive_now = False
                add(f"{_dir(v)} hits {_dir(arr[top])} — {_fmt(-v)} is smaller "
                    f"and explodes.", placed=i)
        if alive_now:
            why = ("moving right, nothing can hit it yet" if v > 0
                   else "nothing ahead of it is moving right")
            stack.append(i)
            counts["pushes"] += 1
            add(f"{_dir(v)} survives ({why}) — push it. Alive: {alive()}.",
                placed=i)

    result = [arr[j] for j in stack]
    add(f"Final state: {[_fmt(x) for x in result] or 'nothing survives'}. "
        f"{counts['collisions']} collision(s); every asteroid entered and left "
        f"the stack at most once — O(n).")
    return _result(arr, steps, result)


def _result(arr, steps, result):
    return {
        "meta": {
            "algorithm": "asteroid_collision",
            "view": "array",
            "language": "python",
            "result": result,
        },
        "array": arr,
        "steps": steps,
    }
