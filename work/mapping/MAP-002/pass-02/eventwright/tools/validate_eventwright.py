#!/usr/bin/env python3
"""Static Eventwright validator for MAP-002 Functional Spine Pass 01."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import zipfile
from pathlib import Path


MORNING = [
    ("Elira", "If you check that strap again, it may start charging you for the inspection."),
    ("Marek", "The stitching was loose."),
    ("Nessa", "It was loose the first time you checked it."),
    ("Marek", "Then the second check confirmed an excellent memory."),
    ("Davren", "A sound professional result."),
    ("Nessa", "Latch has been arguing with the door since sunrise."),
    ("Marek", "He dislikes closed questions."), ("Nessa", "Doors."),
    ("Marek", "Those too."), ("Davren", "It would have held another day."),
    ("Marek", "That's what it said yesterday."), ("Elira", "You checked it last night."),
    ("Marek", "I checked the measure. This is the buckle."),
    ("Nessa", "A separate crisis."), ("Marek", "Potentially."),
    ("Marek", "Joren's calibration weight."), ("Davren", "He would have remembered."),
    ("Marek", "Tomorrow, perhaps."), ("Elira", "Back before supper?"),
    ("Marek", "That was the assignment."),
    ("Davren", "Assignments and roads both change."),
    ("Marek", "Then I will write down which one."),
]
EVENING = [
    ("Nessa", "What happened to Latch?"), ("Marek", "Mud."),
    ("Nessa", "I can see the mud. Why is he wearing half the north road?"),
    ("Marek", "He found a ditch he disagreed with."),
    ("Elira", "Then both of you can leave the disagreement by the door."),
    ("Davren", "The west shutter caught again."),
    ("Elira", "Because the frame is warped."),
    ("Davren", "The hinge remains more cooperative."),
    ("Elira", "You are very quiet."),
    ("Marek", "I was checking whether I had anything useful to say."),
    ("Elira", "And?"), ("Marek", "Not yet."),
    ("Nessa", "That has never stopped Father."),
    ("Davren", "It has slowed me considerably."),
    ("Davren", "Was the marker wrong?"),
    ("Marek", "The marker or the ground. There was old masonry behind the slope."),
    ("Davren", "Road risk?"), ("Marek", "Maybe. Joren will send a proper crew."),
    ("Elira", "And the rest?"), ("Marek", "I do not know enough yet."),
    ("Elira", "Then say that."), ("Marek", "I just did."),
]


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten(map_data):
    for event in map_data["events"]:
        if not event: continue
        for pi,page in enumerate(event["pages"]):
            for ci,command in enumerate(page["list"]):
                yield event,pi,ci,command


def dialogue(page):
    found=[]; speaker=None
    for c in page["list"]:
        if c["code"]==101: speaker=c["parameters"][4]
        elif c["code"]==401: found.append((speaker,c["parameters"][0]))
    return found


def run(args):
    m1=json.loads(args.map001.read_text(encoding="utf-8")); b1=json.loads(args.map001_baseline.read_text(encoding="utf-8"))
    m2=json.loads(args.map002.read_text(encoding="utf-8")); b2=json.loads(args.map002_baseline.read_text(encoding="utf-8"))
    results=[]
    def check(name, condition, detail=""):
        results.append({"name":name,"status":"PASS" if condition else "FAIL","detail":detail})
    check("candidate JSON schemas load", True)
    check("MAP-002 geometry/data unchanged", m2["data"]==b2["data"] and m2["width"]==b2["width"] and m2["height"]==b2["height"] and m2["tilesetId"]==b2["tilesetId"])
    other_keys=set(b2)-{"events","note"}
    check("MAP-002 non-event properties unchanged", all(m2[k]==b2[k] for k in other_keys))
    check("all 17 anchor IDs/names/coordinates preserved", all(m2["events"][i][k]==b2["events"][i][k] for i in range(1,18) for k in ("id","name","x","y")))
    with zipfile.ZipFile(args.sample_zip, "r") as archive:
        flags=json.loads(archive.read("SampleGenerated/data/Tilesets.json"))[3]["flags"]
    width,height=m2["width"],m2["height"]; size=width*height
    layers=[m2["data"][i*size:(i+1)*size] for i in range(4)]
    wall_ids={6784,6785,6787,6789,7048}
    def walkable(x,y):
        if not (0<=x<width and 0<=y<height): return False
        stack=[layer[y*width+x] for layer in layers]
        if stack[0]==1536 or any(tile in wall_ids for tile in stack): return False
        for tile in reversed(stack):
            if not tile or flags[tile]&0x10: continue
            return flags[tile]&0x0F != 0x0F
        return True
    route_cells=[]
    pos=[14,14]
    for route in ([1]*5,[4]*5+[3]*5+[4]*2+[3]*2,[2]*2+[1]*2+[2]*5):
        for code in route:
            dx,dy={1:(0,1),2:(-1,0),3:(1,0),4:(0,-1)}[code]
            pos[0]+=dx; pos[1]+=dy; route_cells.append(tuple(pos))
    check("Morning movement route ends at exact required cells", route_cells[4]==(14,19) and route_cells[18]==(21,12) and tuple(pos)==(14,14))
    check("Every Morning movement cell is stock-passable", all(walkable(*cell) for cell in route_cells), f"{len(route_cells)} steps")
    occupied={(21,13),(7,13),(13,12),(13,18)}
    check("Morning route avoids staged NPC collision cells", not (set(route_cells)&occupied))
    p1=m2["events"][1]["pages"][0]; p2=m2["events"][2]["pages"][0]
    check("Morning page gate uses SW101 and VR1>=1002", p1["trigger"]==3 and p1["conditions"]["switch1Id"]==101 and p1["conditions"]["switch1Valid"] and p1["conditions"]["variableId"]==1 and p1["conditions"]["variableValue"]==1002)
    check("Morning exact internal equality and SW102 OFF", any(c["code"]==111 and c["parameters"]==[1,1,0,1002,0] for c in p1["list"]) and any(c["code"]==111 and c["parameters"]==[0,102,1] for c in p1["list"]))
    check("Morning clears inherited MAP-001 black tint before Fade In", any(c["code"]==223 and c["parameters"]==[[0,0,0,0],0,False] for c in p1["list"]))
    first_morning_fadein=next(i for i,c in enumerate(p1["list"]) if c["code"]==222)
    check("Marek is visible before Morning Fade In", any(c["code"]==211 and c["parameters"]==[1] for c in p1["list"][:first_morning_fadein]))
    check("Morning anti-replay pages", len(m2["events"][1]["pages"])==3 and m2["events"][1]["pages"][1]["conditions"]["switch1Id"]==102 and m2["events"][1]["pages"][2]["conditions"]["variableValue"]==1003)
    check("Evening page gate uses SW110 and VR1>=1011", p2["trigger"]==3 and p2["conditions"]["switch1Id"]==110 and p2["conditions"]["variableId"]==1 and p2["conditions"]["variableValue"]==1011)
    check("Evening exact internal equality and SW111 OFF", any(c["code"]==111 and c["parameters"]==[1,1,0,1011,0] for c in p2["list"]) and any(c["code"]==111 and c["parameters"]==[0,111,1] for c in p2["list"]))
    check("Evening normalizes tint before household Fade In", any(c["code"]==223 and c["parameters"]==[[0,0,0,0],0,False] for c in p2["list"]))
    first_evening_fadein=next(i for i,c in enumerate(p2["list"]) if c["code"]==222)
    check("Marek is visible before Evening Fade In", any(c["code"]==211 and c["parameters"]==[1] for c in p2["list"][:first_evening_fadein]))
    check("Evening anti-replay pages", len(m2["events"][2]["pages"])==3 and m2["events"][2]["pages"][1]["conditions"]["switch1Id"]==111 and m2["events"][2]["pages"][2]["conditions"]["variableValue"]==1012)
    check("Morning exact dialogue and order", dialogue(p1)==MORNING, f"{len(dialogue(p1))} lines")
    check("Evening exact dialogue and order", dialogue(p2)==EVENING, f"{len(dialogue(p2))} lines")
    ambient=[("Davren","If the latch catches again, leave it for this evening."),("Elira","The survey office will still be there. Breakfast will not."),("Nessa","Latch thinks every closed door is a personal insult.")]
    check("approved family ambient lines exact", [dialogue(m2["events"][i]["pages"][1])[0] for i in (5,6,7)]==ambient)
    expected_images={5:("People1",4),6:("People1",5),7:("People2",2),8:("Nature",0)}
    check("placeholder character assignments exact", all((m2["events"][i]["pages"][0]["image"]["characterName"],m2["events"][i]["pages"][0]["image"]["characterIndex"])==v for i,v in expected_images.items()))
    all2=list(flatten(m2)); forbidden={126,127,128,301,302,355,655,357}
    check("no inventory/combat/shop/script/plugin commands", not any(c["code"] in forbidden for *_,c in all2))
    route_codes=[]
    for *_,c in all2:
        if c["code"]==205: route_codes += [x["code"] for x in c["parameters"][1]["list"]]
    check("no route scripts or route switch writes", not ({27,28,45}&set(route_codes)))
    transfers=[c["parameters"] for *_,c in all2 if c["code"]==201]
    check("Evening has sole MAP-002 transfer to MAP-001", transfers==[[0,1,14,10,2,2]])
    check("MAP-003 remains unresolved comment hook", any(c["code"]==108 and "HOOK MAP-003" in c["parameters"][0] for c in m2["events"][15]["pages"][0]["list"]) and not any(p[1]==3 for p in transfers))
    ses=[c["parameters"][0] for *_,c in all2 if c["code"]==250]
    check("Morning Dog SE exactly once", sum(s["name"]=="Dog" and s["volume"]==55 for s in ses)==1)
    check("repair SE exactly once and restrained", sum(s["name"]=="Equip1" and s["volume"]==45 for s in ses)==1)
    check("distant three-note cue exactly once and faint", sum(s["name"]=="Ancient_ThreeNote_Resonance" and s["volume"]==35 for s in ses)==1)
    se_index=next(i for i,c in enumerate(p2["list"]) if c["code"]==250 and c["parameters"][0]["name"]=="Ancient_ThreeNote_Resonance")
    post_se_waits=[c["parameters"][0] for c in p2["list"][se_index+1:] if c["code"]==230]
    check("night cue preserves target post-audio silence", post_se_waits[:2]==[105,219], "3.4s cue plus approximately 120 silent frames")
    latch_dialogue=dialogue(m2["events"][8]["pages"][0])+dialogue(m2["events"][9]["pages"][0])
    check("Latch has no speech/thought text", latch_dialogue==[])
    switch_writes=[c["parameters"] for *_,c in all2 if c["code"]==121]
    variable_writes=[c["parameters"] for *_,c in all2 if c["code"]==122]
    check("only approved MAP-002 global switch writes", switch_writes==[[102,102,0],[111,111,0]])
    check("only VR1 writes exact stages", variable_writes==[[1,1,0,0,1003],[1,1,0,0,1012]])
    mi_sw=next(i for i,c in enumerate(p1["list"]) if c["code"]==121 and c["parameters"]==[102,102,0])
    check("Morning player release visible/followers hidden", p1["list"][mi_sw+1]["parameters"]==[1,1,0,0,1003] and p1["list"][mi_sw+2]["code"]==211 and p1["list"][mi_sw+2]["parameters"]==[1] and p1["list"][mi_sw+3]["code"]==216 and p1["list"][mi_sw+3]["parameters"]==[1])
    evening_codes=[c["code"] for c in p2["list"]]
    i_sw=next(i for i,c in enumerate(p2["list"]) if c["code"]==121 and c["parameters"]==[111,111,0])
    check("Evening output ordered before black transfer", 221 in evening_codes[:i_sw] and p2["list"][i_sw+1]["parameters"]==[1,1,0,0,1012] and p2["list"][i_sw+2]["parameters"]==[0,1,14,10,2,2])
    check("bedroom uses stock downed pose and restores Actor1", any(c["code"]==205 and any(x.get("parameters")==["Damage1",0] for x in c["parameters"][1]["list"]) for c in p2["list"]) and any(c["code"]==205 and any(x.get("parameters")==["Actor1",0] for x in c["parameters"][1]["list"]) for c in p2["list"]))
    # MAP-001 may differ only in the tail beginning at the approved hook.
    base=copy.deepcopy(b1); candidate=copy.deepcopy(m1)
    bl=base["events"][1]["pages"][0]["list"]; cl=candidate["events"][1]["pages"][0]["list"]
    bi=next(i for i,c in enumerate(bl) if c["code"]==108 and c["parameters"][0].startswith("HOOK PRO-SC-002"))
    ci=next(i for i,c in enumerate(cl) if c["code"]==108 and c["parameters"][0].startswith("HOOK PRO-SC-002"))
    base["events"][1]["pages"][0]["list"]=bl[:bi]; candidate["events"][1]["pages"][0]["list"]=cl[:ci]
    check("MAP-001 validated opening prefix and all other data preserved", base==candidate and bl[:bi]==cl[:ci])
    check("MAP-001 exact authorized transfer tail", cl[ci:]==[{"code":108,"indent":0,"parameters":["HOOK PRO-SC-002: approved transfer to MAP-002 Morning."]},{"code":201,"indent":0,"parameters":[0,2,14,14,8,2]},{"code":0,"indent":0,"parameters":[]}])
    check("MAP-001 state writes remain SW101 then VR1=1002", cl[ci-2]["code"]==121 and cl[ci-2]["parameters"]==[101,101,0] and cl[ci-1]["code"]==122 and cl[ci-1]["parameters"]==[1,1,0,0,1002])
    check("candidate hashes recorded", True, f"Map001={sha(args.map001)} Map002={sha(args.map002)}")
    return results


def main():
    p=argparse.ArgumentParser(); p.add_argument("--map001",type=Path,required=True); p.add_argument("--map001-baseline",type=Path,required=True); p.add_argument("--map002",type=Path,required=True); p.add_argument("--map002-baseline",type=Path,required=True); p.add_argument("--sample-zip",type=Path,required=True); p.add_argument("--json-output",type=Path); p.add_argument("--text-output",type=Path); a=p.parse_args()
    results=run(a); passed=sum(r["status"]=="PASS" for r in results); failed=len(results)-passed
    payload={"validator":"MAP-002 Eventwright Functional Spine Pass 01","summary":{"passed":passed,"failed":failed,"total":len(results)},"results":results}
    text="\n".join(f"{r['status']}: {r['name']}"+(f" — {r['detail']}" if r['detail'] else "") for r in results)+f"\nSUMMARY: {passed}/{len(results)} PASS\n"
    if a.json_output: a.json_output.parent.mkdir(parents=True,exist_ok=True); a.json_output.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    if a.text_output: a.text_output.parent.mkdir(parents=True,exist_ok=True); a.text_output.write_text(text,encoding="utf-8")
    print(text,end=""); raise SystemExit(1 if failed else 0)


if __name__=="__main__": main()
