#!/usr/bin/env python3
"""Build the original MAP-004 survey-office spatial skeleton, without story logic.

Only stock tile-sheet images are inspected from the immutable sample archive.
The shared MAP-002 stock renderer/event schema is reused; no MAP-002 geometry is.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

WIDTH, HEIGHT, TILE, LAYERS = 25, 19, 48, 6
ANCHORS = [
    (1, "EV_Story_SurveyAssignment", 5, 5),
    (2, "EV_Story_SurveyReport", 6, 5),
    (3, "EV_NPC_Joren", 16, 8),
    (4, "EV_NPC_Edrin", 9, 11),
    (5, "EV_Transfer_Brackenford", 12, 16),
    (6, "EV_Prop_SurveyLedger", 16, 9),
    (7, "EV_Visual_RecordStorage", 19, 7),
    (8, "EV_Camera_WorkFloor", 12, 10),
]


def shared_stock_schema():
    path = Path(__file__).resolve().parents[2].parent / "MAP-002/pass-01/tools/build_map002.py"
    spec = importlib.util.spec_from_file_location("mz_stock_schema", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    module.WIDTH, module.HEIGHT = WIDTH, HEIGHT
    return module


def build_map(blank_event):
    size = WIDTH * HEIGHT
    layers = [[0] * size for _ in range(LAYERS)]

    def put(layer, x, y, tile):
        assert 0 <= x < WIDTH and 0 <= y < HEIGHT
        layers[layer][y * WIDTH + x] = tile

    # Dark, blocked backdrop. No entrances on the edges of the canvas.
    for y in range(HEIGHT):
        for x in range(WIDTH):
            put(0, x, y, 1536)
    # One enclosed public-facing office, no extra corridor or room.
    for y in range(4, 16):
        for x in range(4, 21):
            put(0, x, y, 1552)
    for x in range(3, 22):
        put(0, x, 2, 6785)
        put(0, x, 3, 7048)
        if x != 12:
            put(0, x, 16, 6785)
    for y in range(3, 17):
        put(0, 3, y, 6784)
        put(0, 21, y, 6784)
    put(0, 12, 16, 1552)

    # Recordkeeping furniture on edges. Counter is reachable from west around
    # its left end; arrival and actor-facing middle floor remain unobstructed.
    furniture = {
        (6, 6): 137, (8, 6): 137, (19, 7): 137,
        (15, 9): 116, (16, 9): 116, (17, 9): 116, (18, 9): 116,
        (6, 12): 116, (7, 12): 116, (19, 13): 137,
        (12, 11): 120, (11, 11): 120,
    }
    for (x, y), tile in furniture.items():
        put(3, x, y, tile)
    events = [None] + [blank_event(*a) for a in ANCHORS]
    return {
        "autoplayBgm": False, "autoplayBgs": False,
        "battleback1Name": "", "battleback2Name": "",
        "bgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "disableDashing": False, "displayName": "Brackenford - Survey Office",
        "encounterList": [], "encounterStep": 30, "height": HEIGHT,
        "note": "MAP-004 Mapping Pass 01; no executable event logic",
        "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": "",
        "parallaxShow": True, "parallaxSx": 0, "parallaxSy": 0,
        "scrollType": 0, "specifyBattleback": False, "tilesetId": 3,
        "width": WIDTH, "data": [tile for layer in layers for tile in layer],
        "events": events,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-zip", type=Path, required=True)
    args = parser.parse_args()
    out = Path(__file__).resolve().parents[1]
    schema = shared_stock_schema()
    office = build_map(schema.blank_event)
    (out / "Map004.json").write_text(json.dumps(office, separators=(",", ":")), encoding="utf-8")
    sheets = schema.load_stock_sheets(args.sample_zip.resolve())
    full = schema.render_map(office, sheets)
    full.save(out / "MAP-004_full-map.png")
    for name, cx, cy in [("arrival", 12, 15), ("desk", 12, 9)]:
        # PIL crop gracefully pads camera area that lies outside map canvas.
        full.crop(((cx-8)*TILE, (cy-6)*TILE, (cx+9)*TILE, (cy+7)*TILE)).save(
            out / f"MAP-004_{name}_816x624.png")
    print(f"Generated {out / 'Map004.json'} and three preview images")


if __name__ == "__main__":
    main()
