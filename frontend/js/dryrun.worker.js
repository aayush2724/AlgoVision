// ── DRY RUN WORKER ─────────────────────────────────────────────────────────
//
// Runs a student's Python inside their own browser (Pyodide, CPython compiled
// to WebAssembly) and records every line it executes, the way a student would
// on paper: which line, what every variable holds, who called whom, what got
// printed. Nothing is sent to a server.
//
// It lives in a worker so a runaway program can't freeze the page: the page
// keeps a timer and terminates this worker if a run takes too long. Inside,
// a step cap stops infinite loops long before that.
//
// Protocol
//   page → worker  { type: 'run', id, code, call, maxSteps }
//   worker → page  { type: 'status', text }           while Pyodide loads
//                  { type: 'result', id, ...trace }   see HARNESS below
//                  { type: 'fatal', id, message }     Pyodide failed to load

const PYODIDE_VERSION = '0.29.5';
const INDEX_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

// The tracer, in Python. Kept as a string so the page needs no extra request.
const HARNESS = String.raw`
import sys, io, json, builtins, contextlib, traceback

_FN = "<your code>"

class _StepLimit(Exception):
    pass

def _no_input(*a, **k):
    raise RuntimeError("input() can't ask you for a value in a dry run - "
                       "put the values in the 'Then run' line instead.")

def _short(text, n=160):
    return text if len(text) <= n else text[:n - 1] + "…"

def _describe(v):
    try:
        r = repr(v)
    except Exception:
        r = "<unprintable>"
    d = {"r": _short(r), "t": type(v).__name__}
    if isinstance(v, (list, tuple)) and len(v) <= 24 and all(
            isinstance(x, (int, float, str, bool)) or x is None for x in v):
        d["items"] = [_short(repr(x), 12) for x in v]
    return d

def _visible(name, v):
    if name.startswith("__"):
        return False
    t = type(v).__name__
    return t not in ("module", "function", "builtin_function_or_method", "type")

def _frames(frame):
    out = []
    f = frame
    while f is not None:
        if f.f_code.co_filename == _FN:
            is_mod = f.f_code.co_name == "<module>"
            src = f.f_globals if is_mod else f.f_locals
            vars_ = {}
            for k, v in list(src.items()):
                if _visible(k, v):
                    vars_[k] = _describe(v)
                    if len(vars_) >= 40:
                        break
            out.append({"name": "main program" if is_mod else f.f_code.co_name + "()",
                        "line": f.f_lineno, "vars": vars_})
        f = f.f_back
    out.reverse()           # outermost first
    return out[-12:]

def _run(code, call, max_steps):
    program = code.rstrip("\n")
    call_line = None
    if call.strip():
        program += "\n" + call.strip()
        call_line = program.count("\n") + 1
    steps, out = [], io.StringIO()
    result = {"steps": steps, "lines": program.split("\n"), "callLine": call_line,
              "truncated": False, "error": None, "output": ""}

    # While an exception unwinds, Python reports a "return None" and a fresh
    # "exception" for every frame it leaves. To a student that reads as the
    # function returning None and the error happening three times, so record
    # only where it was raised; a later "line" event means it was caught.
    unwinding = [False]

    def record(frame, event, arg=None):
        if event == "line":
            unwinding[0] = False
        elif unwinding[0]:
            return
        elif event == "exception":
            unwinding[0] = True
        if len(steps) >= max_steps:
            raise _StepLimit()
        s = {"line": frame.f_lineno, "event": event, "frames": _frames(frame),
             "out": len(out.getvalue())}
        if event == "return":
            s["ret"] = _describe(arg)
            s["fn"] = frame.f_code.co_name
        elif event == "exception":
            s["exc"] = _short(arg[0].__name__ + ": " + str(arg[1]), 200)
        steps.append(s)

    def local_trace(frame, event, arg):
        if event in ("line", "return", "exception"):
            record(frame, event, arg)
        return local_trace

    def global_trace(frame, event, arg):
        if frame.f_code.co_filename != _FN:
            return None     # never step through Python's own library code
        return local_trace

    g = {"__name__": "__main__", "__builtins__": builtins}
    try:
        compiled = compile(program, _FN, "exec")
    except SyntaxError as e:
        result["error"] = {"type": "SyntaxError", "message": e.msg, "line": e.lineno}
        return json.dumps(result)

    real_input = builtins.input
    builtins.input = _no_input
    try:
        with contextlib.redirect_stdout(out):
            sys.settrace(global_trace)
            try:
                exec(compiled, g)
            finally:
                sys.settrace(None)
    except _StepLimit:
        result["truncated"] = True
    except RecursionError:
        result["error"] = {"type": "RecursionError",
                           "message": "maximum recursion depth exceeded - is there a base case?",
                           "line": steps[-1]["line"] if steps else None}
    except BaseException as e:
        tb = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == _FN]
        result["error"] = {"type": type(e).__name__, "message": _short(str(e), 300),
                           "line": tb[-1].lineno if tb else None}
    finally:
        builtins.input = real_input
    result["output"] = _short(out.getvalue(), 20000)
    return json.dumps(result)
`;

let pyodide = null;
let loading = null;

function load() {
  if (loading) return loading;
  loading = (async () => {
    self.postMessage({ type: 'status', text: 'Loading Python in your browser (first time only, ~10 MB)…' });
    importScripts(`${INDEX_URL}pyodide.js`);
    pyodide = await self.loadPyodide({ indexURL: INDEX_URL });
    pyodide.runPython(HARNESS);
  })();
  return loading;
}

self.onmessage = async (e) => {
  const msg = e.data || {};
  if (msg.type !== 'run') return;
  try {
    await load();
  } catch (err) {
    loading = null;
    self.postMessage({ type: 'fatal', id: msg.id, message: String(err?.message || err) });
    return;
  }
  self.postMessage({ type: 'status', text: 'Running your code…' });
  const run = pyodide.globals.get('_run');
  try {
    const json = run(String(msg.code || ''), String(msg.call || ''), Number(msg.maxSteps) || 1500);
    self.postMessage({ type: 'result', id: msg.id, ...JSON.parse(json) });
  } catch (err) {
    self.postMessage({ type: 'fatal', id: msg.id, message: String(err?.message || err) });
  } finally {
    run.destroy();
  }
};
