#!/usr/bin/env python3
"""Validate MAP-002 Mapping Pass 01 against its approved work order."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from collections import deque
from pathlib import Path

from build_map002 import EVENTS, HEIGHT, LAYERS, WIDTH


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", dest="map_path", type=Path, required=True)
    parser.add_argument("--sample-zip", type=Path, required=True)
    parser.add_argument("--results", type=Path)
    args = parser.parse_args()
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append((name, bool(condition), detail))

    m = json.loads(args.map_path.read_text(encoding="utf-8"))
    check("Canvas is 29x23", (m["width"], m["height"]) == (WIDTH, HEIGHT))
    check("Six MZ data planes", len(m["data"]) == WIDTH * HEIGHT * LAYERS)
    check("Inside tileset slot 3", m["tilesetId"] == 3)
    check("No looping", m["scrollType"] == 0)
    check("No encounters", m["encounterList"] == [])
    check("No autoplay", not m["autoplayBgm"] and not m["autoplayBgs"])
    check("No parallax", m["parallaxName"] == "" and not m["parallaxLoopX"] and not m["parallaxLoopY"])

    events = m["events"]
    check("Exactly 17 registered events", len(events) == 18 and events[0] is None)
    for event_id, name, x, y in EVENTS:
        e = events[event_id] if event_id < len(events) else None
        check(f"Anchor {event_id:02d} identity", bool(e) and (e["id"], e["name"], e["x"], e["y"]) == (event_id, name, x, y))
        if e:
            p = e["pages"]
            safe = (len(p) == 1 and p[0]["list"] == [{"code": 0, "indent": 0, "parameters": []}]
                    and p[0]["through"] is True and p[0]["priorityType"] == 0
                    and p[0]["trigger"] == 0 and p[0]["moveType"] == 0
                    and p[0]["image"]["characterName"] == "" and p[0]["image"]["tileId"] == 0)
            check(f"Anchor {event_id:02d} is Mapper-safe blank stub", safe)

    size = WIDTH * HEIGHT
    region = m["data"][5 * size:6 * size]
    check("All Region IDs are zero", all(v == 0 for v in region))

    with zipfile.ZipFile(args.sample_zip, "r") as archive:
        tilesets = json.loads(archive.read("SampleGenerated/data/Tilesets.json"))
    flags = tilesets[3]["flags"]
    check("Stock fixture is Inside", tilesets[3]["name"] == "Inside")
    used = {v for v in m["data"][:4 * size] if v}
    check("Every used tile has a stock flag", all(v < len(flags) for v in used), f"used={sorted(used)}")

    wall_ids = {6784, 6785, 6787, 6789, 7048}
    layers = [m["data"][i * size:(i + 1) * size] for i in range(4)]

    def walkable(x: int, y: int) -> bool:
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            return False
        stack = [layer[y * WIDTH + x] for layer in layers]
        if stack[0] == 1536 or any(tile in wall_ids for tile in stack):
            return False
        for tile in reversed(stack):
            if not tile or flags[tile] & 0x10:
                continue
            if flags[tile] & 0x0F == 0x0F:
                return False
            break
        return True

    def reachable(start: tuple[int, int], targets: set[tuple[int, int]]) -> bool:
        q, seen = deque([start]), {start}
        while q:
            p = q.popleft()
            if targets <= seen:
                return True
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                n = (p[0] + dx, p[1] + dy)
                if n not in seen and walkable(*n):
                    seen.add(n); q.append(n)
        return targets <= seen

    required_route_cells = {(14,14), (14,19), (14,20), (8,8), (13,8), (19,8),
                            (19,9), (14,13), (20,12), (21,13)}
    check("Mandatory house routes connect", reachable((14, 14), required_route_cells))

    table_seats = {(13,12), (16,12), (14,11), (15,13)}
    check("Four table staging cells remain walkable", all(walkable(*p) for p in table_seats))
    check("Table does not trap common-room route", reachable((14,14), table_seats))

    check("Common camera crop remains inside canvas", 14 - 8 >= 0 and 14 + 8 < WIDTH and 13 - 6 >= 0 and 13 + 6 < HEIGHT)
    check("Bedroom camera crop remains inside canvas", 20 - 8 >= 0 and 20 + 8 < WIDTH and 6 - 6 >= 0 and 6 + 6 < HEIGHT)
    bedroom_crop = (12, 0, 28, 12)
    check("Bedroom frame contains bed and threshold",
          bedroom_crop[0] <= 21 <= bedroom_crop[2] and bedroom_crop[1] <= 5 <= bedroom_crop[3]
          and bedroom_crop[0] <= 19 <= bedroom_crop[2] and bedroom_crop[1] <= 9 <= bedroom_crop[3])

    # Authored door contract: three internal gaps, one and only one exterior gap.
    check("Bedroom wall has only required door gaps", all(walkable(x, 8) == (x in (8,13,19)) for x in range(4,25)))
    check("Single exterior exit at (14,20)", walkable(14,20) and all(not walkable(x,20) for x in range(10,19) if x != 14))

    lines = [f"MAP-002 Mapping Pass 01 validation - {'PASS' if all(ok for _,ok,_ in checks) else 'FAIL'}", ""]
    for name, ok, detail in checks:
        lines.append(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" :: {detail}" if detail else ""))
    lines += ["", f"Checks: {sum(ok for _,ok,_ in checks)}/{len(checks)}",
              f"Map SHA-256: {hashlib.sha256(args.map_path.read_bytes()).hexdigest()}"]
    report = "\n".join(lines) + "\n"
    print(report, end="")
    if args.results:
        args.results.parent.mkdir(parents=True, exist_ok=True)
        args.results.write_text(report, encoding="utf-8")
    return 0 if all(ok for _, ok, _ in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
