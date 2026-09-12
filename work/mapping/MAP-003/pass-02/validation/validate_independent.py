#!/usr/bin/env python3
"""Pass 02 independent regression on MAP-003 using Pass 01's fixed-blueprint audit.

No Mapper-owned files or immutable inputs are modified. The reused audit's
coordinates are literal blueprint requirements, not imported Mapper constants.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
MAPROOT = ROOT / "repo_stage/work/mapping/MAP-003"
CURRENT = MAPROOT / "pass-02"
PRIOR = MAPROOT / "pass-01"
OUT = CURRENT / "validation/independent_results.txt"
PREV_AUDIT = PRIOR / "validation/validate_independent.py"


def main() -> int:
    checks: list[tuple[str, bool]] = []
    def check(name: str, ok: bool) -> None:
        checks.append((name, bool(ok)))

    old = json.loads((PRIOR / "Map003.json").read_bytes())
    new = json.loads((CURRENT / "Map003.json").read_bytes())
    check("Pass 01 vs 02 tile grid identical", old["data"] == new["data"])
    check("only map note changes outside events", {k: v for k, v in old.items() if k not in ("note", "events")} ==
          {k: v for k, v in new.items() if k not in ("note", "events")} and
          old["note"] == "MAP-003 Mapping Pass 01: spatial skeleton and inert anchors" and
          new["note"] == "MAP-003 Mapping Pass 02: spatial skeleton and inert anchors")
    old7 = old["events"][7]
    new7 = new["events"][7]
    check("only event ID 7 changes between passes", len(old["events"]) == len(new["events"]) == 11 and
          all(old["events"][i] == new["events"][i] for i in range(11) if i != 7))
    check("Latch moves from home to approved northern-road cell and retains inert page", 
          (old7["x"], old7["y"], new7["x"], new7["y"]) == (12, 26, 21, 8) and
          {k: v for k, v in old7.items() if k not in ("x", "y")} ==
          {k: v for k, v in new7.items() if k not in ("x", "y")})
    images = ("MAP-003_full-map.png", "MAP-003_home_816x624.png",
              "MAP-003_office_816x624.png", "MAP-003_north-road_816x624.png")
    check("all four camera/overall previews unchanged byte-for-byte", all(
          (PRIOR / f).read_bytes() == (CURRENT / f).read_bytes() for f in images))
    old_source = (PRIOR / "tools/build_map003.py").read_text()
    new_source = (CURRENT / "tools/build_map003.py").read_text()
    check("builder changed only Latch coordinate and pass-number note", old_source.replace(
          '(7, "EV_NPC_Latch_Departure", 12, 26)',
          '(7, "EV_NPC_Latch_Departure", 21, 8)').replace(
          'MAP-003 Mapping Pass 01: spatial skeleton and inert anchors',
          'MAP-003 Mapping Pass 02: spatial skeleton and inert anchors') == new_source)
    check("Pass 02 self-check asserts approved blueprint rather than builder only", 
          'anchors match the approved work order independently of the builder' in
          (CURRENT / "tools/validate_map003.py").read_text())

    spec = importlib.util.spec_from_file_location("independent_pass01", PREV_AUDIT)
    assert spec and spec.loader
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    validator.PACKAGE = CURRENT
    validator.MAPFILE = CURRENT / "Map003.json"
    validator.BUILDER = CURRENT / "tools/build_map003.py"
    validator.OUT = CURRENT / "validation/full_independent_results.txt"
    base_status = validator.main()
    check("full independent static/directional/rebuild audit passes", base_status == 0)
    rows = [f"{'PASS' if ok else 'FAIL'}: {name}" for name, ok in checks]
    rows.append(f"SHA256 Map003.json {validator.digest(CURRENT / 'Map003.json')}")
    rows.append(f"SUMMARY: {sum(ok for _, ok in checks)}/{len(checks)} regression checks PASS; "
                f"{'PASS' if all(ok for _, ok in checks) else 'FAIL'}")
    OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("\n".join(rows))
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
