from app.config import settings

_TONE = {
    "beginner": "in plain, friendly language using a simple analogy",
    "intermediate": "with the key intuition and the trade-offs",
    "advanced": "with precise complexity analysis and invariants",
}

_SYSTEM_PROMPT = """You are the narrator of AlgoVision — an educational platform
that teaches algorithms through real-world cinematic metaphors.
Your job is to explain each step of an algorithm as if it's happening in the real world.
Be vivid, concise, and use the metaphor provided. Max 2 sentences per step.
Always end with what happens next. Never use jargon without explaining it."""

def explain_step(algorithm: str, step: dict, level: str, realworld_meta: dict = None) -> dict:
    tone = _TONE.get(level, _TONE["beginner"])
    note = step.get("note", "the algorithm makes progress")
    metaphors = realworld_meta.get("metaphors", {}) if realworld_meta else {}
    scene_title = realworld_meta.get("title", algorithm) if realworld_meta else algorithm

    if settings.GROQ_API_KEY:
        try:
            from groq import Groq
            client = Groq(api_key=settings.GROQ_API_KEY)
            node = step.get("node") or step.get("highlight", {}).get("node", "")
            edge = step.get("edge") or step.get("highlight", {}).get("edge")
            node_term = metaphors.get("node", "node")
            edge_term = metaphors.get("edge", "edge")

            user_msg = (
                f"Scene: {scene_title}. "
                f"Algorithm step: {note}. "
                f"In this world, a 'node' is a '{node_term}' and an 'edge' is an '{edge_term}'. "
                f"Current element: {node or edge}. "
                f"Explain this step {tone}. Max 2 sentences."
            )
            resp = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=120,
                temperature=0.7
            )
            return {
                "text": resp.choices[0].message.content.strip(),
                "live": True,
                "level": level,
                "scene": scene_title
            }
        except Exception as e:
            pass  # fall through to offline

    # Offline fallback — still uses real-world language from metaphors
    node_term = metaphors.get("node", "node")
    visit_msg = metaphors.get("visit", "Processing")
    text = f"{visit_msg} {step.get('node', '')} ({node_term}). {note}"
    return {"text": text, "live": False, "level": level, "scene": scene_title}


def find_bug(language: str, code: str) -> dict:
    if settings.GROQ_API_KEY:
        try:
            from groq import Groq
            client = Groq(api_key=settings.GROQ_API_KEY)
            resp = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{
                    "role": "user",
                    "content": (
                        f"You are a DSA code reviewer. Analyze this {language} code for bugs, "
                        f"logical errors, and edge cases. Be specific about line numbers if possible. "
                        f"Give 2-4 concrete hints, not solutions.\n\nCode:\n{code}"
                    )
                }],
                max_tokens=200,
                temperature=0.3
            )
            text = resp.choices[0].message.content.strip()
            hints = [line.strip("- •1234567890.").strip()
                     for line in text.split('\n') if line.strip()]
            hints = [h for h in hints if len(h) > 10][:4]
            return {"hints": hints or [text], "live": True}
        except Exception:
            pass

    # Offline static analysis
    hints = []
    low = code.lower()
    if "while" in low and "visited" not in low and ("graph" in low or "bfs" in low or "dfs" in low):
        hints.append("Your graph traversal may loop forever — track visited nodes.")
    if language.lower() == "python" and "\t" in code and "    " in code:
        hints.append("Mixed tabs and spaces detected — this breaks Python indentation.")
    if "= len(" in code and "- 1" not in code and ("high" in low or "right" in low):
        hints.append("Off-by-one risk: array upper bound may need '- 1'.")
    if not hints:
        hints.append("No obvious issue found. Check boundary conditions and base cases.")
    return {"hints": hints, "live": False}
