#!/usr/bin/env python3
"""Deterministic Brackenford Mapping Pass 01 using stock MZ Outside tiles.

The sample archive is used read-only for the stock tileset flags and preview
sheets. No layout, map IDs or authored content are copied from it.
"""
from __future__ import annotations

import argparse
import io
import json
import zipfile
from pathlib import Path
from PIL import Image

W, H, TILE = 45, 35, 48
LAYERS = 6
GRASS, EARTH, COBBLE, STONE = 1552, 1553, 1560, 1561
ROOF, WALL = 2048 + 52 * 48, 2048 + 60 * 48
ANCHORS = (
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
)


def blank_event(eid: int, name: str, x: int, y: int) -> dict:
    """Blank MZ event, no content or transfer; below-characters/through."""
    return {"id": eid, "name": name, "note": "Mapping anchor only", "x": x, "y": y,
            "pages": [{"conditions": {"actorId": 1, "actorValid": False,
                                      "itemId": 1, "itemValid": False,
                                      "selfSwitchCh": "A", "selfSwitchValid": False,
                                      "switch1Id": 1, "switch1Valid": False,
                                      "switch2Id": 1, "switch2Valid": False,
                                      "variableId": 1, "variableValid": False,
                                      "variableValue": 0},
                       "directionFix": False,
                       "image": {"characterIndex": 0, "characterName": "", "direction": 2,
                                 "pattern": 1, "tileId": 0},
                       "list": [{"code": 0, "indent": 0, "parameters": []}],
                       "moveFrequency": 3,
                       "moveRoute": {"list": [{"code": 0, "parameters": []}],
                                     "repeat": True, "skippable": False, "wait": False},
                       "moveSpeed": 3, "moveType": 0, "priorityType": 0,
                       "stepAnime": False, "through": True, "trigger": 0,
                       "walkAnime": True}]}


def build() -> dict:
    size = W * H
    layers = [[0] * size for _ in range(LAYERS)]

    def put(layer: int, x: int, y: int, tid: int) -> None:
        if not (0 <= x < W and 0 <= y < H):
            raise ValueError((x, y))
        layers[layer][y * W + x] = tid

    def rect(layer: int, x0: int, y0: int, x1: int, y1: int, tid: int) -> None:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                put(layer, x, y, tid)

    # Terrain is fully authored; the black A5/rock cliff boundary is sealed.
    rect(0, 0, 0, W - 1, H - 1, GRASS)
    rect(0, 0, 0, W - 1, 1, 1648)
    rect(0, 0, H - 2, W - 1, H - 1, 1648)
    rect(0, 0, 0, 1, H - 1, 1648)
    rect(0, W - 2, 0, W - 1, H - 1, 1648)

    # Home -> crossroads -> office, and crossroads -> north, all 2+ tiles wide.
    rect(0, 10, 25, 23, 27, EARTH)
    rect(0, 21, 2, 23, 27, EARTH)
    rect(0, 21, 16, 32, 18, EARTH)
    rect(0, 29, 15, 32, 18, EARTH)
    rect(0, 21, 2, 23, 6, COBBLE)
    rect(0, 20, 16, 24, 18, COBBLE)
    rect(0, 29, 15, 32, 16, STONE)
    # Light patches are deterministic, neutral wear (not encoded mystery).
    for x, y in ((9, 27), (17, 25), (18, 26), (26, 18), (24, 20),
                 (20, 11), (25, 13), (32, 19), (12, 29)):
        put(0, x, y, EARTH)

    # Non-enterable, ordinary house facades. Roof/wall use MZ A3 wall autotiles.
    buildings = [
        (7, 18, 16, 25, 11, ROOF, WALL),   # Venn family house
        (27, 8, 36, 15, 31, ROOF, WALL),   # survey office
        (5, 8, 13, 14, None, 2048 + 51 * 48, WALL),
        (35, 22, 41, 28, None, 2048 + 52 * 48, 2048 + 60 * 48),
    ]
    for x0, y0, x1, y1, door, roof, wall in buildings:
        split = y0 + 3
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if door == x and y == y1:  # accessible future doorway hotspot
                    continue
                kind = roof if y < split else wall
                left = (x == x0)
                top = (y == y0 or y == split)
                right = (x == x1)
                bottom = (y == split - 1 or y == y1)
                shape = int(left) + 2 * int(top) + 4 * int(right) + 8 * int(bottom)
                put(0, x, y, kind + shape)

    # Ordinary facade windows on an overlay layer; behind them stock A3 walls
    # remain solid. Door graphics are reserved for Eventwright: their stock B
    # tiles are impassable and would invalidate the future touch transfer.
    def b_id(x: int, y: int) -> int:
        return (x // 8) * 128 + y * 8 + (x % 8)

    for x, y in ((9, 23), (14, 23), (29, 13), (34, 13),
                 (7, 12), (11, 12), (37, 26), (40, 26)):
        put(3, x, y, b_id(0, 12))
    # Three entrances remain on walkable ground immediately to the south.
    # Small neutral plants make the streets less diagrammatic without blocking
    # the main route or introducing a lore-significant landmark.
    for x, y in ((6, 17), (15, 17), (5, 20), (38, 19),
                 (7, 27), (15, 28), (34, 27), (31, 29)):
        put(3, x, y, b_id(8, 3))

    events = [None] + [blank_event(*a) for a in ANCHORS]
    return {"autoplayBgm": False, "autoplayBgs": False,
            "battleback1Name": "", "battleback2Name": "",
            "bgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
            "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
            "disableDashing": False, "displayName": "Brackenford",
            "encounterList": [], "encounterStep": 30, "height": H,
            "note": "MAP-003 Mapping Pass 02: spatial skeleton and inert anchors",
            "parallaxLoopX": False, "parallaxLoopY": False,
            "parallaxName": "", "parallaxShow": True,
            "parallaxSx": 0, "parallaxSy": 0, "scrollType": 0,
            "specifyBattleback": False, "tilesetId": 2,
            "width": W, "data": [tid for layer in layers for tid in layer],
            "events": events}


def render(data: dict, sample_zip: Path, target: Path) -> None:
    # MZ's stock tile formulas are used only for previews. Zero external writes.
    from importlib.util import module_from_spec, spec_from_file_location
    helper = Path(__file__).resolve().parents[3] / "MAP-002/pass-01/tools/build_map002.py"
    spec = spec_from_file_location("map002_tile_preview", helper)
    module = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    names = {2: "Outside_A3", 4: "Outside_A5", 5: "Outside_B", 6: "Outside_C"}
    with zipfile.ZipFile(sample_zip, "r") as archive:
        sheets = {slot: Image.open(io.BytesIO(archive.read(
            f"SampleGenerated/img/tilesets/{name}.png"))).convert("RGBA")
                  for slot, name in names.items()}
    canvas = Image.new("RGBA", (W*TILE, H*TILE), (50, 65, 45, 255))
    size = W*H
    for layer in range(4):
        for idx, tid in enumerate(data["data"][layer*size:(layer+1)*size]):
            if not tid:
                continue
            x, y = idx % W, idx // W
            if 4352 <= tid < 5888:
                kind, shape = (tid-2048)//48, (tid-2048)%48
                tx, ty = kind % 8, kind // 8
                bx, by = tx*2, (ty-6)*2
                for i, (qx, qy) in enumerate(module.WALL_AUTOTILE_TABLE[shape]):
                    part = sheets[2].crop(((bx*2+qx)*24, (by*2+qy)*24,
                                           (bx*2+qx+1)*24, (by*2+qy+1)*24))
                    canvas.alpha_composite(part, (x*48+(i%2)*24, y*48+(i//2)*24))
            else:
                module.draw_normal(canvas, sheets, tid, x, y)
    full = canvas.convert("RGB")
    def save_preview(image: Image.Image, path: Path) -> None:
        image.quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)
    save_preview(full, target / "MAP-003_full-map.png")
    for label, cx, cy in (("home", 11, 23), ("office", 31, 13), ("north-road", 22, 8)):
        left, top = (cx-8)*TILE, (cy-6)*TILE
        save_preview(full.crop((left,top,left+816,top+624)), target / f"MAP-003_{label}_816x624.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-zip", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1])
    a = parser.parse_args()
    dest = a.output_dir.resolve(); dest.mkdir(parents=True, exist_ok=True)
    data = build()
    (dest/"Map003.json").write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    render(data, a.sample_zip.resolve(), dest)
    print(f"Built {dest/'Map003.json'} and four review composites")


if __name__ == "__main__":
    main()
