#!/usr/bin/env python3
"""Change only the Pass 02 back-wall notice to a tabular record chart."""

import argparse
import importlib.util
import json
from pathlib import Path


def prior():
    path=Path(__file__).resolve().parents[1].parent / "pass-02/tools/build_map004_pass02.py"
    spec=importlib.util.spec_from_file_location("map004_pass02",path)
    module=importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def build():
    office,schema=prior().build()
    w,h=office["width"],office["height"]
    i=3*w*h+5*w+11
    assert office["data"][i]==91
    # Stock Inside_C tile 329 is a tabular grid with illegible row/column marks.
    # It denotes generic survey-office records, never canonical survey readings.
    office["data"][i]=329
    office["note"]="MAP-004 Mapping Pass 03; solid wall, tabular wall chart, inert anchors"
    return office,schema


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--sample-zip",type=Path,required=True)
    args=parser.parse_args()
    out=Path(__file__).resolve().parents[1]
    office,schema=build()
    (out/"Map004.json").write_text(json.dumps(office,separators=(",",":")),encoding="utf-8")
    full=schema.render_map(office,schema.load_stock_sheets(args.sample_zip.resolve()))
    full.save(out/"MAP-004_full-map.png")
    for name,cx,cy in (("arrival",12,15),("desk",12,9)):
        full.crop(((cx-8)*48,(cy-6)*48,(cx+9)*48,(cy+7)*48)).save(out/f"MAP-004_{name}_816x624.png")
    print("MAP-004 Mapping Pass 03 generated: stock tabular chart only")


if __name__=="__main__":
    main()
