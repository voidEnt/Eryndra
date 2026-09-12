#!/usr/bin/env python3
"""Mapper regression against the Pass 02 map and stock directional flags."""

import json
import sys
import zipfile
from collections import deque
from pathlib import Path


def main(sample):
    here=Path(__file__).resolve().parents[1]
    prev=json.loads((here.parent/"pass-02/Map004.json").read_text())
    curr=json.loads((here/"Map004.json").read_text())
    with zipfile.ZipFile(sample) as z:
        flags=json.loads(z.read("SampleGenerated/data/Tilesets.json"))[3]["flags"]
    w,h=curr["width"],curr["height"]
    cells=w*h
    differences=[n for n,(a,b) in enumerate(zip(prev["data"],curr["data"])) if a!=b]

    def passage(x,y,d):
        bit={2:1,4:2,6:4,8:8}[d]
        for layer in (3,2,1,0):
            flag=flags[curr["data"][layer*cells+y*w+x]]
            if flag&0x10:continue
            return not flag&bit
        return False

    def canmove(x,y,d):
        dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[d]
        nx,ny=x+dx,y+dy
        return (0<=nx<w and 0<=ny<h and passage(x,y,d)
                and passage(nx,ny,{2:8,4:6,6:4,8:2}[d]))

    seen={(12,15)}; q=deque(seen)
    while q:
        x,y=q.popleft()
        for d,(dx,dy) in ((2,(0,1)),(4,(-1,0)),(6,(1,0)),(8,(0,-1))):
            dest=(x+dx,y+dy)
            if dest not in seen and canmove(x,y,d):
                seen.add(dest);q.append(dest)
    chartidx=3*cells+5*w+11
    checks={
        "only approved chart layer changed from Pass 02": differences==[chartidx] and
           prev["data"][chartidx]==91 and curr["data"][chartidx]==329,
        "stock chart is impassable and desk record unchanged": flags[329]&15==15 and
           prev["data"][3*cells+9*w+16]==curr["data"][3*cells+9*w+16]==91,
        "door single reachable south-boundary tile": {(x,16) for x in range(4,21) if (x,16) in seen}=={(12,16)},
        "south wall blocks every direction": all(not passage(x,16,d) for x in range(4,21)
           if x!=12 for d in (2,4,6,8)),
        "desk and Edrin scene route retained": all(pt in seen for pt in ((12,12),(16,11),(15,8),(9,11))),
        "exact same eight inert event anchors": prev["events"]==curr["events"] and len(curr["events"])==9,
        "all map metadata unchanged except note": all(prev[k]==curr[k] for k in prev if k not in ("data","note")),
        "same 194 walkable cells reachable": len(seen)==194,
    }
    for title,ok in checks.items():print(f"{'PASS' if ok else 'FAIL'} {title}")
    print(f"{sum(checks.values())}/{len(checks)} PASS; {len(seen)} reachable cells")
    return 0 if all(checks.values()) else 1


if __name__=="__main__":
    sys.exit(main(Path(sys.argv[1])))
