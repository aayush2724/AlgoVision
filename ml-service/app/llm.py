from app.config import settings

_TONE = {
    "beginner": "in plain, friendly language",
    "intermediate": "with the key intuition and trade-offs",
    "advanced": "with precise complexity and invariants",
}


def explain_step(algorithm: str, step: dict, level: str) -> dict:
    tone = _TONE.get(level, _TONE["beginner"])
    note = step.get("note", "the algorithm makes progress")
    if settings.has_provider:
        # Plug a live provider (Groq / Gemini) call here.
        pass
    text = (
        f"In {algorithm}, this step means: {note} "
        f"Explained {tone}, it always commits to the best known option next."
    )
    return {"text": text, "live": settings.has_provider, "level": level}


def find_bug(language: str, code: str) -> dict:
    hints = []
    lowered = code.lower()
    if "while" in lowered and "visited" not in lowered:
        hints.append("Your traversal may loop forever \u2014 track visited nodes.")
    if language.lower() == "python" and "\t" in code and "    " in code:
        hints.append("Mixed tabs and spaces can break Python indentation.")
    if not hints:
        hints.append("No obvious issue found. Check boundary conditions and base cases.")
    return {"hints": hints, "live": settings.has_provider}
