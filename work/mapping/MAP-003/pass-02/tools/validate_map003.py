#!/usr/bin/env python3
"""MAP-003 Pass 02 Mapper self-check; separate independent Validation is still required."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import deque
from pathlib import Path
from build_map003 import ANCHORS, W, H, build


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(mapfile: Path, sample_zip: Path, story_zip: Path) -> list[str]:
    raw = mapfile.read_bytes()
    data = json.loads(raw)
    checks = []
    def check(label: str, condition: bool) -> None:
        checks.append(f"{'PASS' if condition else 'FAIL'}: {label}")
    check("deterministic generated JSON", raw == json.dumps(build(), separators=(",", ":")).encode())
    check("45x35 nonlooping Outside map", (data["width"],data["height"],data["tilesetId"],data["scrollType"]) == (45,35,2,0))
    size = W * H
    check("six schema-sized layers", len(data["data"]) == size * 6)
    events = data["events"]
    blueprint = (Path(__file__).resolve().parents[5] /
                 "docs/design/maps/MAP-003_Brackenford_Blueprint.md").read_text(encoding="utf-8")
    approved = [(int(eid), name, int(x), int(y)) for eid, name, x, y in re.findall(
        r"^\|\s*(\d+)\s*\|\s*`(EV_[^`]+)`\s*\|\s*`\((\d+),(\d+)\)`\s*\|",
        blueprint, flags=re.MULTILINE)]
    check("10 anchors match the approved work order independently of the builder",
          len(approved) == 10 and
          [(e["id"],e["name"],e["x"],e["y"]) for e in events[1:]] == approved)
    check("10 contiguous and inert anchors", len(events) == 11 and events[0] is None and
          [(e["id"],e["name"],e["x"],e["y"]) for e in events[1:]] == list(ANCHORS) and
          all(len(e["pages"]) == 1 and e["pages"][0]["list"] ==
              [{"code":0,"indent":0,"parameters":[]}] and
              e["pages"][0]["priorityType"] == 0 and e["pages"][0]["through"]
              for e in events[1:]))
    check("no encounters, active soundtrack or runtime transfer", not data["encounterList"] and
          not data["autoplayBgm"] and not data["autoplayBgs"] and
          all(e["pages"][0]["list"][0]["code"] == 0 for e in events[1:]))
    with zipfile.ZipFile(sample_zip) as ref:
        tilesets = json.loads(ref.read("SampleGenerated/data/Tilesets.json"))
        flags = tilesets[2]["flags"]
    with zipfile.ZipFile(story_zip) as canon:
        check("locked Prologue source present", "EryndraStory/Acts/PrologueStoryv0.3.pdf" in canon.namelist())

    # MZ top-to-bottom passability rule with star overlays: lower four bits 0
    # means walkable in all directions, 15 means wholly blocked.
    def passable(x: int,y: int) -> bool:
        if not (0 <= x < W and 0 <= y < H): return False
        n=y*W+x
        for layer in (3, 2, 1, 0):
            tid=data["data"][layer*size+n]
            if tid == 0: continue
            bit=flags[tid]
            if bit & 16: continue
            return (bit & 15) == 0
        return False

    starts = ((11,26),(31,16),(22,6))
    check("all three outside arrivals are clear and stock-passable", all(passable(*p) for p in starts) and
          not any((e["x"],e["y"]) in starts for e in events[1:]))
    check("all three door/road anchors have passable approach", all(passable(*p) for p in ((11,25),(31,15),(22,4),(22,5))))
    check("three entrance cells are distinct", len({(events[i]["x"],events[i]["y"]) for i in (1,2,3)}) == 3)
    check("all non-north map boundary is sealed", all(not passable(x,H-1) for x in range(W))
          and all(not passable(x,0) for x in range(W) if x not in (21,22,23))
          and all(not passable(0,y) and not passable(W-1,y) for y in range(H)))

    seen={starts[0]}; todo=deque([starts[0]])
    while todo:
        x,y=todo.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+dx,y+dy)
            if q not in seen and passable(*q):
                seen.add(q); todo.append(q)
    check("home, office, northern exit and return spawn are connected", all(p in seen for p in
          ((11,25),(31,15),(22,4),(22,6))))
    check("principal corridors permit a lateral two-cell walking band", all(passable(21,y) and passable(22,y)
          for y in range(7,17)) and all(passable(x,26) and passable(x,27) for x in range(13,22)))
    check("west/east backdrop houses have no explorable doors", all(not passable(*p)
          for p in ((8,14),(10,14),(37,28),(39,28))))
    check("no combat/battleback/ancient cue assigned", not data["battleback1Name"] and not data["battleback2Name"]
          and not data["bgm"]["name"] and not data["bgs"]["name"])
    checks.append(f"HASH Map003.json SHA-256 {sha(raw)}")
    checks.append(f"HASH immutable EryndraStory.zip SHA-256 {sha(story_zip.read_bytes())}")
    checks.append(f"HASH immutable SampleGenerated.zip SHA-256 {sha(sample_zip.read_bytes())}")
    passed=sum(row.startswith("PASS:") for row in checks)
    total=sum(row.startswith(("PASS:","FAIL:")) for row in checks)
    checks.append(f"SUMMARY: {passed}/{total} self-checks PASS; independent Mapping Validation pending")
    return checks


def main() -> None:
    p=argparse.ArgumentParser()
    for name in ("mapfile","sample_zip","story_zip","output"):
        p.add_argument("--"+name.replace("_","-"), type=Path, required=True)
    a=p.parse_args()
    rows=run(a.mapfile,a.sample_zip,a.story_zip)
    a.output.write_text("\n".join(rows)+"\n",encoding="utf-8")
    print("\n".join(rows))
    if any(row.startswith("FAIL:") for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
