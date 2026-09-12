#!/usr/bin/env python3
"""Apply two Mapper-owned corrections to the immutable Pass 01 MAP-004 skeleton."""

import argparse
import importlib.util
import json
from pathlib import Path


def pass01():
    root = Path(__file__).resolve().parents[1].parent / "pass-01/tools/build_map004.py"
    spec = importlib.util.spec_from_file_location("map004_pass01", root)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def build():
    original = pass01()
    schema = original.shared_stock_schema()
    map_data = original.build_map(schema.blank_event)
    w,h = map_data["width"],map_data["height"]

    def put(layer,x,y,tile):
        map_data["data"][layer*w*h+y*w+x] = tile

    # Fix D1: 7048 has stock Inside flag 0xE0F (blocked in all directions).
    # The deliberately passable door tile at (12,16) remains untouched.
    for x in range(4,21):
        if x != 12:
            put(0,x,16,7048)

    # Fix D2: small stock parchment/notice glyph contains no readable names,
    # measurements, geographical shapes or lore. It is purely mundane office
    # recordkeeping detail; no new map event or interaction is added.
    put(3,11,5,91)
    put(2,16,9,116)
    put(3,16,9,91)
    map_data["note"] = "MAP-004 Mapping Pass 02; corrected solid south wall and generic records; inert anchors"
    return map_data,schema


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--sample-zip",type=Path,required=True)
    args=p.parse_args()
    out=Path(__file__).resolve().parents[1]
    data,schema=build()
    (out/"Map004.json").write_text(json.dumps(data,separators=(",",":")),encoding="utf-8")
    full=schema.render_map(data,schema.load_stock_sheets(args.sample_zip.resolve()))
    full.save(out/"MAP-004_full-map.png")
    for name,cx,cy in (("arrival",12,15),("desk",12,9)):
        full.crop(((cx-8)*48,(cy-6)*48,(cx+9)*48,(cy+7)*48)).save(out/f"MAP-004_{name}_816x624.png")
    print("MAP-004 Mapping Pass 02 corrected map and review previews generated")


if __name__ == "__main__":
    main()
