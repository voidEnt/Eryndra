#!/usr/bin/env python3
"""Mapper regression: simulate stock MZ directional passage and diff Pass 01."""

import importlib.util
import json
import sys
import zipfile
from collections import deque
from pathlib import Path


def main(sample):
    out=Path(__file__).resolve().parents[1]
    base=out.parent/"pass-01"
    with zipfile.ZipFile(sample) as archive:
        flags=json.loads(archive.read("SampleGenerated/data/Tilesets.json"))[3]["flags"]
    old=json.loads((base/"Map004.json").read_text())
    new=json.loads((out/"Map004.json").read_text())
    w,h=new["width"],new["height"]
    size=w*h

    def passage(x,y,d):
        bit={2:1,4:2,6:4,8:8}[d]
        # Match MZ Game_Map.layeredTiles (z3..z0), checkPassage and
        # Game_CharacterBase.isMapPassable (current and destination tile).
        for z in (3,2,1,0):
            tile=new["data"][z*size+y*w+x]
            flag=flags[tile]
            if flag&0x10: continue
            return not flag&bit
        return False

    def move(x,y,d):
        dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[d]
        nx,ny=x+dx,y+dy
        return 0<=nx<w and 0<=ny<h and passage(x,y,d) and passage(nx,ny,{2:8,4:6,6:4,8:2}[d])

    start=(12,15)
    seen={start}; q=deque([start])
    while q:
        x,y=q.popleft()
        for d,(dx,dy) in ((2,(0,1)),(4,(-1,0)),(6,(1,0)),(8,(0,-1))):
            np=(x+dx,y+dy)
            if np not in seen and move(x,y,d):
                seen.add(np);q.append(np)

    diffs=[(z,i%w,i//w,a,b) for n,(a,b) in enumerate(zip(old["data"],new["data"]))
           if a!=b for z,i in ((n//size,n%size),)]
    allowed={(0,x,16) for x in range(4,21) if x!=12}
    allowed|={(3,11,5),(2,16,9),(3,16,9)}
    checks={
        "unchanged MZ map metadata and anchors": {k:v for k,v in old.items() if k not in ("data","note")} ==
                                                {k:v for k,v in new.items() if k not in ("data","note")},
        "delta limited to two Mapper defects": {(z,x,y) for z,x,y,_,_ in diffs}==allowed,
        "south wall all directions blocked": all(not passage(x,16,d) for x in range(4,21)
                                               if x!=12 for d in (2,4,6,8)),
        "door reachable but no lateral wall walking": (12,16) in seen and all((x,16) not in seen
                                               for x in range(4,21) if x!=12),
        "interior staging traversable": all(p in seen for p in ((16,11),(15,8),(9,11),(12,12))),
        "stock parchment chart and desk record present": new["data"][3*size+5*w+11]==91 and
                                               new["data"][3*size+9*w+16]==91,
        "eight inert anchors and no gameplay additions": len(new["events"])==9 and all(
            e["pages"][0]["list"]==[{"code":0,"indent":0,"parameters":[]}]
            for e in new["events"][1:]),
    }
    for name,ok in checks.items():print(f"{'PASS' if ok else 'FAIL'} {name}")
    print(f"{sum(checks.values())}/{len(checks)} PASS, {len(diffs)} permitted tile changes, {len(seen)} reachable cells")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
