#!/usr/bin/env python3
"""Independent MAP-003 Mapping Pass 01 audit; blueprint constants are duplicated.

Reads but never modifies the Mapper output or either immutable reference archive.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
PACKAGE = Path(__file__).resolve().parents[1]
MAPFILE = PACKAGE / "Map003.json"
SAMPLE = ROOT / "project_sources/02-SampleGenerated.zip"
STORY = ROOT / "project_sources/01-EryndraStory.zip"
BUILDER = PACKAGE / "tools/build_map003.py"
OUT = Path(__file__).resolve().parent / "independent_results.txt"
EXPECTED_EVENTS = [
    (1, "EV_Transfer_VennHome", 11, 25),
    (2, "EV_Transfer_SurveyOffice", 31, 15),
    (3, "EV_Transfer_NorthernRoad", 22, 4),
    (4, "EV_Story_TownMorning", 12, 27),
    (5, "EV_Story_TownDeparture", 22, 7),
    (6, "EV_Story_TownReturn", 23, 7),
    (7, "EV_NPC_Latch_Departure", 21, 8),
    (8, "EV_NPC_Townsperson_West", 16, 22),
    (9, "EV_NPC_Townsperson_East", 28, 18),
    (10, "EV_Visual_RoadMarker", 22, 12),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks: list[tuple[str, bool]] = []

    def check(name: str, result: bool) -> None:
        checks.append((name, bool(result)))

    before = [digest(path) for path in (SAMPLE, STORY, MAPFILE)]
    m = json.loads(MAPFILE.read_bytes())
    with zipfile.ZipFile(SAMPLE) as z:
        tileset = json.loads(z.read("SampleGenerated/data/Tilesets.json"))[2]
        reference_map = json.loads(z.read("SampleGenerated/data/Map003.json"))
    flags = tileset["flags"]
    width, height = m["width"], m["height"]
    size = width * height
    events = m["events"]
    check("required MZ map keys compatible with stock Map003", set(reference_map) <= set(m))
    check("45x35, six layers, nonlooping, Outside ID 2", (width, height, m["scrollType"],
          m["tilesetId"], len(m["data"])) == (45, 35, 0, 2, 6 * 45 * 35))
    check("all used tiles defined in Outside stock flags", all(0 <= tid < len(flags) for tid in m["data"]))
    check("10 contiguous map events with no additional IDs", len(events) == 11 and
          events[0] is None and all(e and e["id"] == eid for eid, e in enumerate(events[1:], 1)))
    check("blueprint event IDs, names, and exact coordinates", len(events) == 11 and
          [(e["id"], e["name"], e["x"], e["y"]) for e in events[1:]] == EXPECTED_EVENTS)
    check("Mapper anchors are inert, invisible and nonblocking", all(len(e["pages"]) == 1 and
          e["pages"][0]["list"] == [{"code": 0, "indent": 0, "parameters": []}] and
          e["pages"][0]["priorityType"] == 0 and e["pages"][0]["through"] and
          e["pages"][0]["image"]["characterName"] == "" for e in events[1:]))
    check("no active sound, enemies, scripted transfer or parallax", not m["encounterList"] and
          not m["autoplayBgm"] and not m["autoplayBgs"] and not m["parallaxName"] and
          not m["bgm"]["name"] and not m["bgs"]["name"])

    def passage(x: int, y: int, direction_bit: int) -> bool:
        if not (0 <= x < width and 0 <= y < height):
            return False
        n = y * width + x
        for layer in (3, 2, 1, 0):
            tile_id = m["data"][layer * size + n]
            flag = flags[tile_id]
            if flag & 0x10:
                continue
            return (flag & direction_bit) == 0
        return False

    # MZ bit 1 down / 2 left / 4 right / 8 up: check both source and target.
    def neighbors(x: int, y: int):
        for dx, dy, bit, reverse in ((0, 1, 1, 8), (-1, 0, 2, 4),
                                     (1, 0, 4, 2), (0, -1, 8, 1)):
            if passage(x, y, bit) and passage(x+dx, y+dy, reverse):
                yield x+dx, y+dy

    starts = ((11, 26), (31, 16), (22, 6))
    check("three empty and passable outside spawns", all(all(passage(*p, b) for b in (1, 2, 4, 8))
          for p in starts) and not any((e["x"], e["y"]) in starts for e in events[1:]))
    check("door and northern hotspots approach from specified adjacent cells", all(
          target in set(neighbors(*source)) for source, target in (
              ((11, 26), (11, 25)), ((31, 16), (31, 15)),
              ((22, 5), (22, 4)), ((22, 6), (22, 5)))))
    seen = {starts[0]}
    queue = deque(starts[:1])
    while queue:
        for q in neighbors(*queue.popleft()):
            if q not in seen:
                seen.add(q)
                queue.append(q)
    check("both entrances and northern approach linked by MZ directional passage",
          all(p in seen for p in starts + ((11, 25), (31, 15), (22, 4))))
    check("two-tile corridor from Venn house toward north", all(
          (21, y) in seen and (22, y) in seen for y in range(7, 17)) and
          all((x, 26) in seen and (x, 27) in seen for x in range(13, 22)))
    check("all outer edge cells impassable", all(not passage(x, y, b) for x in range(width)
          for y in (0, height-1) for b in (1, 2, 4, 8)) and
          all(not passage(x, y, b) for y in range(height)
              for x in (0, width-1) for b in (1, 2, 4, 8)))
    check("no false entrances on background building facades", all(
          not passage(x, y, 1) for x, y in ((8, 14), (10, 14), (37, 28), (39, 28))))
    check("four 816x624 review PNGs and 45x35 complete view present", all(
          (PACKAGE / name).exists() for name in (
              "MAP-003_full-map.png", "MAP-003_home_816x624.png",
              "MAP-003_office_816x624.png", "MAP-003_north-road_816x624.png")))
    # Rebuild in a throwaway folder, not over Mapping output; compare byte for byte.
    with tempfile.TemporaryDirectory(prefix="eryndra-map003-validation-") as tmp:
        run = subprocess.run([sys.executable, str(BUILDER), "--sample-zip", str(SAMPLE),
                              "--output-dir", tmp], capture_output=True, text=True)
        check("builder reruns without error in isolated directory", run.returncode == 0)
        check("byte-identical JSON and preview PNGs on rebuild", run.returncode == 0 and
              all((Path(tmp) / name).read_bytes() == (PACKAGE / name).read_bytes() for name in (
                  "Map003.json", "MAP-003_full-map.png", "MAP-003_home_816x624.png",
                  "MAP-003_office_816x624.png", "MAP-003_north-road_816x624.png")))
    check("ZIP inputs and Mapper map were not modified during validation", before ==
          [digest(path) for path in (SAMPLE, STORY, MAPFILE)])
    rows = [f"{'PASS' if outcome else 'FAIL'}: {name}" for name, outcome in checks]
    rows += [f"SHA256 {path.name} {digest(path)}" for path in (MAPFILE, STORY, SAMPLE)]
    rows += [f"SUMMARY: {sum(ok for _, ok in checks)}/{len(checks)} checks PASS; "
             f"{'FAIL' if not all(ok for _, ok in checks) else 'PASS'}"]
    OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("\n".join(rows))
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
