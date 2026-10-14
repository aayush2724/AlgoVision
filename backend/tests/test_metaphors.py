"""Every algorithm narrates in a real scene (app/metaphors.py).

REALWORLD_META in routes/detect.py was partly generated with placeholder
vocabulary (node / link / cost) and hooks that merely described the input
format. app/metaphors.py overwrites those at import time; these tests keep the
catalog from sliding back.
"""
import re
from pathlib import Path

from app import metaphors
from app.routes import detect

ROOT = Path(__file__).resolve().parents[2]
DATA_JS = (ROOT / "frontend/js/data.js").read_text()
IDS = set(re.findall(r'^  \{ id: "([^"]+)"', DATA_JS, flags=re.M))
INSTRUCTION = re.compile(
  r"rows split by|comma|separated|\bup to \d|\(up to|split by|\| |Ops:|^Pairs:|^Edges:|^Input:|"
  r"format|e\.g\.|^Words:|^Text then|^Array,|^Values:|^Numbers:", re.I)
NEEDED = {"node", "edge", "weight", "visit", "start", "done"}


def test_every_story_is_a_catalog_algorithm_with_a_known_kit():
  for aid, spec in metaphors.STORIES.items():
    assert aid in IDS, aid
    assert spec[2] in metaphors.KITS, (aid, spec[2])
    assert spec[0] and spec[1].endswith("."), aid


def test_kits_carry_the_vocabulary_the_narrators_read():
  for name, kit in metaphors.KITS.items():
    assert NEEDED <= set(kit), (name, NEEDED - set(kit))


def test_no_algorithm_narrates_with_placeholder_vocabulary():
  leftovers = [a for a, m in detect.REALWORLD_META.items() if m.get("metaphors") == metaphors.GENERIC]
  assert leftovers == []


def test_hooks_tell_a_story_not_the_input_format():
  meta = [a for a, m in detect.REALWORLD_META.items() if INSTRUCTION.search(m.get("hook", ""))]
  assert meta == []
  cards = [m.group(1) for m in re.finditer(r'\{ id: "([^"]+)",.*?hook: "((?:[^"\\]|\\.)*)"', DATA_JS, re.S)
           if INSTRUCTION.search(m.group(2))]
  assert cards == []


def test_every_catalog_algorithm_has_a_scene():
  for aid in IDS:
    m = detect.REALWORLD_META.get(aid) or detect.REALWORLD_META.get("dynamic_programming")
    assert m and m.get("scene") and m.get("hook") and NEEDED <= set(m.get("metaphors", {})), aid
