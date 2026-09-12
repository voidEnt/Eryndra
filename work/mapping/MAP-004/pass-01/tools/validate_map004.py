#!/usr/bin/env python3
"""Mapper's static check; never a substitute for separate Validation."""

import json
import re
import sys
import zipfile
from collections import deque
from pathlib import Path


def main():
    here = Path(__file__).resolve().parents[1]
    repo = Path(__file__).resolve().parents[5]
    blueprint = (repo / "docs/design/maps/MAP-004_Brackenford_Survey_Office_Blueprint.md").read_text()
    office = json.loads((here / "Map004.json").read_text())
    expected = [
        (int(i), name, int(x), int(y))
        for i, name, x, y in re.findall(
            r"^\|\s*(\d+)\s*\|\s*`(EV_[^`]+)`\s*\|\s*`\((\d+),(\d+)\)`",
            blueprint, flags=re.M,
        )
    ]
    sample = Path(sys.argv[1])
    with zipfile.ZipFile(sample) as z:
        flags = json.loads(z.read("SampleGenerated/data/Tilesets.json"))[3]["flags"]
    w, h = office["width"], office["height"]
    cells = w*h

    def layer(l, x, y):
        return office["data"][l*cells + y*w + x]

    def free(x, y):
        if not (0 <= x < w and 0 <= y < h):
            return False
        return layer(0,x,y) == 1552 and all(
            (not t or flags[t] & 15 != 15) for t in (layer(i,x,y) for i in range(1,4))
        )

    start = (12,15)
    visited = {start}
    queue = deque([start])
    while queue:
        x,y = queue.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if p not in visited and free(*p):
                queue.append(p); visited.add(p)

    cases = {
        "shape, stock Inside, nonlooping": (w,h,office["tilesetId"],office["scrollType"]) == (25,19,3,0),
        "six correctly sized layers": len(office["data"]) == 6*cells,
        "eight blueprint anchors parsed": len(expected) == 8,
        "anchor IDs/names/positions from approved blueprint": [
            (ev["id"],ev["name"],ev["x"],ev["y"]) for ev in office["events"][1:]
        ] == expected,
        "only inert event pages": all(
            len(ev["pages"]) == 1 and
            [cmd["code"] for cmd in ev["pages"][0]["list"]] == [0] and
            ev["pages"][0]["priorityType"] == 0 and ev["pages"][0]["through"]
            for ev in office["events"][1:]
        ),
        "arrival clear of anchors": start not in {(e["x"],e["y"]) for e in office["events"][1:]},
        "entrance and story staging reachable": all(p in visited for p in (
            (12,16),(16,11),(15,8),(9,11),(12,12))),
        "outside bounds blocked": all(not free(x, y) for x in range(w) for y in (0,h-1)) and
            all(not free(x,y) for y in range(h) for x in (0,w-1)),
        "no encounters, BGM or BGS": not office["encounterList"] and
            not office["autoplayBgm"] and not office["autoplayBgs"],
        "all occupied furniture within interior": all(
            layer(3,x,y) == 0 or (4 <= x <= 20 and 4 <= y <= 15)
            for y in range(h) for x in range(w)
        ),
    }
    for label, success in cases.items():
        print(f"{'PASS' if success else 'FAIL'} {label}")
    print(f"{sum(cases.values())}/{len(cases)} PASS; {len(visited)} traversable cells reachable")
    return 0 if all(cases.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
