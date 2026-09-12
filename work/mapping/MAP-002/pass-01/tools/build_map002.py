#!/usr/bin/env python3
"""Build MAP-002 Mapping Pass 01 and render stock-tile review composites.

The stock MZ reference archive is opened read-only and supplies only the Inside
tileset preview sheets. No reference map geometry is imported.
"""

from __future__ import annotations

import argparse
import io
import json
import zipfile
from pathlib import Path

from PIL import Image


WIDTH, HEIGHT, TILE = 29, 23, 48
LAYERS = 6

FLOOR_AUTOTILE_TABLE = [
    [[2,4],[1,4],[2,3],[1,3]], [[2,0],[1,4],[2,3],[1,3]], [[2,4],[3,0],[2,3],[1,3]], [[2,0],[3,0],[2,3],[1,3]],
    [[2,4],[1,4],[2,3],[3,1]], [[2,0],[1,4],[2,3],[3,1]], [[2,4],[3,0],[2,3],[3,1]], [[2,0],[3,0],[2,3],[3,1]],
    [[2,4],[1,4],[2,1],[1,3]], [[2,0],[1,4],[2,1],[1,3]], [[2,4],[3,0],[2,1],[1,3]], [[2,0],[3,0],[2,1],[1,3]],
    [[2,4],[1,4],[2,1],[3,1]], [[2,0],[1,4],[2,1],[3,1]], [[2,4],[3,0],[2,1],[3,1]], [[2,0],[3,0],[2,1],[3,1]],
    [[0,4],[1,4],[0,3],[1,3]], [[0,4],[3,0],[0,3],[1,3]], [[0,4],[1,4],[0,3],[3,1]], [[0,4],[3,0],[0,3],[3,1]],
    [[2,2],[1,2],[2,3],[1,3]], [[2,2],[1,2],[2,3],[3,1]], [[2,2],[1,2],[2,1],[1,3]], [[2,2],[1,2],[2,1],[3,1]],
    [[2,4],[3,4],[2,3],[3,3]], [[2,4],[3,4],[2,1],[3,3]], [[2,0],[3,4],[2,3],[3,3]], [[2,0],[3,4],[2,1],[3,3]],
    [[2,4],[1,4],[2,5],[1,5]], [[2,0],[1,4],[2,5],[1,5]], [[2,4],[3,0],[2,5],[1,5]], [[2,0],[3,0],[2,5],[1,5]],
    [[0,4],[3,4],[0,3],[3,3]], [[2,2],[1,2],[2,5],[1,5]], [[0,2],[1,2],[0,3],[1,3]], [[0,2],[1,2],[0,3],[3,1]],
    [[2,2],[3,2],[2,3],[3,3]], [[2,2],[3,2],[2,1],[3,3]], [[2,4],[3,4],[2,5],[3,5]], [[2,0],[3,4],[2,5],[3,5]],
    [[0,4],[1,4],[0,5],[1,5]], [[0,4],[3,0],[0,5],[1,5]], [[0,2],[3,2],[0,3],[3,3]], [[0,2],[1,2],[0,5],[1,5]],
    [[0,4],[3,4],[0,5],[3,5]], [[2,2],[3,2],[2,5],[3,5]], [[0,2],[3,2],[0,5],[3,5]], [[0,0],[1,0],[0,1],[1,1]],
]

WALL_AUTOTILE_TABLE = [
    [[2,2],[1,2],[2,1],[1,1]], [[0,2],[1,2],[0,1],[1,1]], [[2,0],[1,0],[2,1],[1,1]], [[0,0],[1,0],[0,1],[1,1]],
    [[2,2],[3,2],[2,1],[3,1]], [[0,2],[3,2],[0,1],[3,1]], [[2,0],[3,0],[2,1],[3,1]], [[0,0],[3,0],[0,1],[3,1]],
    [[2,2],[1,2],[2,3],[1,3]], [[0,2],[1,2],[0,3],[1,3]], [[2,0],[1,0],[2,3],[1,3]], [[0,0],[1,0],[0,3],[1,3]],
    [[2,2],[3,2],[2,3],[3,3]], [[0,2],[3,2],[0,3],[3,3]], [[2,0],[3,0],[2,3],[3,3]], [[0,0],[3,0],[0,3],[3,3]],
]

EVENTS = [
    (1, "EV_Story_MorningController", 14, 13),
    (2, "EV_Story_EveningController", 14, 13),
    (3, "EV_Spawn_Morning", 14, 14),
    (4, "EV_Spawn_Evening", 14, 19),
    (5, "EV_NPC_Davren", 21, 13),
    (6, "EV_NPC_Elira", 7, 13),
    (7, "EV_NPC_Nessa", 13, 12),
    (8, "EV_NPC_Latch_Morning", 13, 18),
    (9, "EV_NPC_Latch_EveningThreshold", 19, 9),
    (10, "EV_Prop_CrookedLatch", 14, 19),
    (11, "EV_Prop_FieldKit", 21, 12),
    (12, "EV_Prop_CalibrationWeight", 22, 12),
    (13, "EV_Prop_SupperTable", 14, 12),
    (14, "EV_Prop_MarekBed", 21, 5),
    (15, "EV_Transfer_Brackenford", 14, 20),
    (16, "EV_Camera_CommonRoom", 14, 13),
    (17, "EV_Camera_MarekRoom", 20, 6),
]


def blank_event(event_id: int, name: str, x: int, y: int) -> dict:
    page = {
        "conditions": {"actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False,
                       "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1,
                       "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                       "variableId": 1, "variableValid": False, "variableValue": 0},
        "directionFix": False,
        "image": {"characterIndex": 0, "characterName": "", "direction": 2,
                  "pattern": 1, "tileId": 0},
        "list": [{"code": 0, "indent": 0, "parameters": []}],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True,
                      "skippable": False, "wait": False},
        "moveSpeed": 3,
        "moveType": 0,
        "priorityType": 0,
        "stepAnime": False,
        "through": True,
        "trigger": 0,
        "walkAnime": True,
    }
    return {"id": event_id, "name": name, "note": "", "pages": [page], "x": x, "y": y}


def build_map() -> dict:
    size = WIDTH * HEIGHT
    layers = [[0] * size for _ in range(LAYERS)]

    def put(layer: int, x: int, y: int, tile_id: int) -> None:
        assert 0 <= x < WIDTH and 0 <= y < HEIGHT
        layers[layer][y * WIDTH + x] = tile_id

    # Impassable dark buffer is explicit on every cell until a floor replaces it.
    for y in range(HEIGHT):
        for x in range(WIDTH):
            put(0, x, y, 1536)

    # Original Venn-home footprint. A5 wood floors avoid hidden autotile assumptions.
    for y in range(4, 17):
        for x in range(5, 24):
            put(0, x, y, 1552)
    for y in range(17, 20):
        for x in range(11, 18):
            put(0, x, y, 1552)
    put(0, 14, 20, 1552)

    # Stock Inside A4 timber/plaster shell. IDs are stock schema dependencies.
    for x in range(4, 25):
        put(0, x, 2, 6785)
        put(0, x, 3, 7048)
    put(0, 4, 2, 6787); put(0, 24, 2, 6789)
    for y in range(3, 18):
        put(0, 4, y, 6784); put(0, 24, y, 6784)

    # Bedroom dividers.
    for x in (10, 15):
        for y in range(3, 8):
            put(0, x, y, 6784)

    # Bedroom-to-hall wall with exact door gaps.
    for x in range(4, 25):
        if x not in (8, 13, 19):
            put(0, x, 8, 6785)
    put(0, 8, 8, 1552); put(0, 13, 8, 1552); put(0, 19, 8, 1552)

    # Lower house closes around the centered mud entry.
    for x in list(range(4, 11)) + list(range(18, 25)):
        put(0, x, 17, 6785)
    for y in range(17, 21):
        put(0, 10, y, 6784); put(0, 18, y, 6784)
    for x in range(10, 19):
        if x != 14:
            put(0, x, 20, 6785)

    # Furniture and functional footprints. These are tiles, never event logic.
    furniture = {
        # Parents' shared bed and storage.
        (6, 5): 169, (7, 5): 170, (6, 6): 177, (7, 6): 178, (9, 5): 137,
        # Nessa's modest single bed and dresser.
        (12, 5): 171, (12, 6): 179, (14, 5): 204,
        # Marek's simple bed and neutral survey-preparation work surface.
        (21, 5): 172, (21, 6): 180, (18, 6): 116,
        # Kitchen and ordinary storage.
        (6, 11): 186, (6, 12): 194, (7, 12): 201, (8, 12): 202,
        (9, 12): 203, (9, 11): 184, (7, 15): 212, (9, 15): 248,
        # Common/supper table and four modest stools.
        (14, 12): 112, (15, 12): 113, (13, 12): 120, (16, 12): 120,
        (14, 11): 120, (15, 13): 120,
        # Repair nook, field-kit staging and small calibration-weight box.
        (20, 13): 116, (21, 11): 402, (22, 14): 220, (22, 15): 232,
    }
    for (x, y), tile_id in furniture.items():
        put(3, x, y, tile_id)

    events = [None] + [blank_event(*spec) for spec in EVENTS]
    data = [tile for layer in layers for tile in layer]
    return {
        "autoplayBgm": False, "autoplayBgs": False,
        "battleback1Name": "", "battleback2Name": "",
        "bgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "disableDashing": False, "displayName": "Brackenford - Venn Home",
        "encounterList": [], "encounterStep": 30, "height": HEIGHT,
        "note": "MAP-002 Mapping Pass 01; blank anchors only",
        "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": "",
        "parallaxShow": True, "parallaxSx": 0, "parallaxSy": 0,
        "scrollType": 0, "specifyBattleback": False, "tilesetId": 3,
        "width": WIDTH, "data": data, "events": events,
    }


def load_stock_sheets(sample_zip: Path) -> dict[int, Image.Image]:
    names = {0: "Inside_A1", 1: "Inside_A2", 3: "Inside_A4", 4: "Inside_A5",
             5: "Inside_B", 6: "Inside_C"}
    with zipfile.ZipFile(sample_zip, "r") as archive:
        return {
            slot: Image.open(io.BytesIO(archive.read(f"SampleGenerated/img/tilesets/{name}.png"))).convert("RGBA")
            for slot, name in names.items()
        }


def draw_normal(canvas: Image.Image, sheets: dict[int, Image.Image], tile_id: int, x: int, y: int) -> None:
    if 1536 <= tile_id < 2048:
        slot = 4
    else:
        slot = 5 + tile_id // 256
    sheet = sheets.get(slot)
    if sheet is None:
        return
    sx = ((tile_id // 128 % 2) * 8 + tile_id % 8) * TILE
    sy = ((tile_id % 256) // 8 % 16) * TILE
    part = sheet.crop((sx, sy, sx + TILE, sy + TILE))
    canvas.alpha_composite(part, (x * TILE, y * TILE))


def draw_autotile(canvas: Image.Image, sheets: dict[int, Image.Image], tile_id: int, x: int, y: int) -> None:
    kind = (tile_id - 2048) // 48
    shape = (tile_id - 2048) % 48
    tx, ty = kind % 8, kind // 8
    table = FLOOR_AUTOTILE_TABLE
    if 2816 <= tile_id < 4352:
        slot, bx, by = 1, tx * 2, (ty - 2) * 3
    elif 5888 <= tile_id:
        slot = 3
        bx = tx * 2
        by = int((ty - 10) * 2.5 + (0.5 if ty % 2 else 0))
        if ty % 2:
            table = WALL_AUTOTILE_TABLE
            shape %= 16
    else:
        return
    sheet = sheets[slot]
    for i, (qx, qy) in enumerate(table[shape]):
        sx, sy = (bx * 2 + qx) * 24, (by * 2 + qy) * 24
        part = sheet.crop((sx, sy, sx + 24, sy + 24))
        canvas.alpha_composite(part, (x * TILE + (i % 2) * 24, y * TILE + (i // 2) * 24))


def render_map(map_data: dict, sheets: dict[int, Image.Image]) -> Image.Image:
    canvas = Image.new("RGBA", (WIDTH * TILE, HEIGHT * TILE), (8, 8, 10, 255))
    size = WIDTH * HEIGHT
    for layer in range(4):
        values = map_data["data"][layer * size:(layer + 1) * size]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                tile_id = values[y * WIDTH + x]
                if tile_id <= 0:
                    continue
                if 2048 <= tile_id < 8192:
                    draw_autotile(canvas, sheets, tile_id, x, y)
                else:
                    draw_normal(canvas, sheets, tile_id, x, y)
    return canvas.convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-zip", type=Path, required=True,
                        help="Read-only SampleGenerated.zip, used only for stock preview sheets")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)

    map_data = build_map()
    (out / "Map002.json").write_text(json.dumps(map_data, separators=(",", ":")), encoding="utf-8")

    sheets = load_stock_sheets(args.sample_zip.resolve())
    full = render_map(map_data, sheets)
    full.save(out / "MAP-002_full-map.png")

    def camera_crop(cx: int, cy: int) -> Image.Image:
        left, top = (cx - 8) * TILE, (cy - 6) * TILE
        return full.crop((left, top, left + 816, top + 624))

    camera_crop(14, 13).save(out / "MAP-002_common-room_816x624.png")
    camera_crop(20, 6).save(out / "MAP-002_marek-bedroom_816x624.png")
    print(f"Built {out / 'Map002.json'} and three review composites")


if __name__ == "__main__":
    main()
