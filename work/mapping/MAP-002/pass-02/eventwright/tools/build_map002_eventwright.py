#!/usr/bin/env python3
"""Build MAP-002 Eventwright Functional Spine Pass 01.

Reads accepted MAP-001 and MAP-002 baselines and writes only the Eventwright
candidate files named by the caller. Source/reference archives are never opened.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


def cmd(code, parameters=None, indent=0):
    return {"code": code, "indent": indent, "parameters": parameters or []}


def conditions(*, switch=None, variable=None, value=0, self_switch=None):
    return {
        "actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False,
        "selfSwitchCh": self_switch or "A", "selfSwitchValid": bool(self_switch),
        "switch1Id": switch or 1, "switch1Valid": switch is not None,
        "switch2Id": 1, "switch2Valid": False,
        "variableId": variable or 1, "variableValid": variable is not None,
        "variableValue": value,
    }


def page(*, cond=None, image=None, commands=None, trigger=0, priority=1,
         through=False, direction_fix=False):
    return {
        "conditions": cond or conditions(),
        "directionFix": direction_fix,
        "image": image or {"characterIndex": 0, "characterName": "", "direction": 2,
                            "pattern": 1, "tileId": 0},
        "list": (commands or []) + [cmd(0)],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True,
                      "skippable": False, "wait": False},
        "moveSpeed": 3, "moveType": 0, "priorityType": priority,
        "stepAnime": False, "through": through, "trigger": trigger, "walkAnime": True,
    }


def image(name, index, direction=2, pattern=1):
    return {"characterIndex": index, "characterName": name, "direction": direction,
            "pattern": pattern, "tileId": 0}


FACES = {"Marek": ("Actor1", 0), "Davren": ("People1", 4),
         "Elira": ("People1", 5), "Nessa": ("People2", 2)}


def say(speaker, line, indent=2):
    face, index = FACES[speaker]
    return [cmd(101, [face, index, 0, 2, speaker], indent), cmd(401, [line], indent)]


def wait(frames, indent=2):
    return cmd(230, [frames], indent)


def set_location(character_id, x, y, direction=0, indent=2):
    return cmd(203, [character_id, 0, x, y, direction], indent)


def move_route(character_id, route_commands, *, wait_for=True, indent=2):
    route = {"list": route_commands + [{"code": 0, "parameters": []}],
             "repeat": False, "skippable": False, "wait": wait_for}
    return cmd(205, [character_id, route], indent)


def step(code, *parameters):
    return {"code": code, "parameters": list(parameters)}


def exact_gate(commands, stage, required_switch, indent=0):
    """Nested exact stage equality + required switch OFF."""
    out = [cmd(111, [1, 1, 0, stage, 0], indent),
           cmd(111, [0, required_switch, 1], indent + 1)]
    for command in commands:
        c = copy.deepcopy(command)
        c["indent"] += indent + 2
        out.append(c)
    out += [cmd(412, [], indent + 1), cmd(412, [], indent)]
    return out


def morning_commands():
    c = [cmd(108, ["PRO-SC-002 / Morning at the Venn House"], 0)]
    body = [
        cmd(221), cmd(211, [1]), cmd(216, [1]),
        set_location(-1, 14, 14, 8, 0),
        set_location(5, 21, 13, 4, 0), set_location(6, 7, 13, 6, 0),
        set_location(7, 13, 12, 2, 0), set_location(8, 13, 18, 2, 0),
        cmd(216, [1]), cmd(223, [[0, 0, 0, 0], 0, False], 0), cmd(222), wait(36, 0),
    ]
    for who, line in [
        ("Elira", "If you check that strap again, it may start charging you for the inspection."),
        ("Marek", "The stitching was loose."),
        ("Nessa", "It was loose the first time you checked it."),
        ("Marek", "Then the second check confirmed an excellent memory."),
        ("Davren", "A sound professional result."),
    ]:
        body += say(who, line, 0) + [wait(12, 0)]
    body += [move_route(8, [step(16)], indent=0),
             cmd(250, [{"name": "Dog", "pan": 0, "pitch": 100, "volume": 55}], 0)]
    for who, line in [
        ("Nessa", "Latch has been arguing with the door since sunrise."),
        ("Marek", "He dislikes closed questions."),
        ("Nessa", "Doors."), ("Marek", "Those too."),
    ]:
        body += say(who, line, 0) + [wait(12, 0)]
    body += [
        move_route(-1, [step(1), step(1), step(1), step(1), step(1), step(16)], indent=0),
        wait(20, 0),
        cmd(250, [{"name": "Equip1", "pan": 0, "pitch": 95, "volume": 45}], 0), wait(24, 0),
    ]
    for who, line in [("Davren", "It would have held another day."),
                      ("Marek", "That's what it said yesterday.")]:
        body += say(who, line, 0) + [wait(12, 0)]
    # Path avoids the supper table, Davren, and the repair-table collision cell.
    body += [move_route(-1, [step(4)] * 5 + [step(3)] * 5 + [step(4)] * 2 +
                        [step(3)] * 2 + [step(19)], indent=0),
             wait(20, 0), move_route(-1, [step(17), step(18)], indent=0), wait(22, 0),
             move_route(-1, [step(17), step(18)], indent=0), wait(22, 0)]
    for who, line in [("Elira", "You checked it last night."),
                      ("Marek", "I checked the measure. This is the buckle."),
                      ("Nessa", "A separate crisis."), ("Marek", "Potentially.")]:
        body += say(who, line, 0) + [wait(12, 0)]
    body += [move_route(-1, [step(18)], indent=0)]
    for who, line in [("Marek", "Joren's calibration weight."),
                      ("Davren", "He would have remembered."),
                      ("Marek", "Tomorrow, perhaps."),
                      ("Elira", "Back before supper?"),
                      ("Marek", "That was the assignment."),
                      ("Davren", "Assignments and roads both change."),
                      ("Marek", "Then I will write down which one.")]:
        body += say(who, line, 0) + [wait(12, 0)]
    body += [move_route(-1, [step(2)] * 2 + [step(1)] * 2 + [step(2)] * 5 + [step(19)], indent=0),
             cmd(121, [102, 102, 0], 0), cmd(122, [1, 1, 0, 0, 1003], 0),
             cmd(211, [1], 0), cmd(216, [1], 0)]
    c += exact_gate(body, 1002, 102)
    return c


def evening_commands():
    c = [cmd(108, ["PRO-SC-011 / Home, But Changed"], 0)]
    body = [
        cmd(221), cmd(211, [1]), cmd(216, [1]),
        set_location(-1, 14, 19, 8, 0),
        set_location(5, 21, 13, 4, 0), set_location(6, 7, 13, 6, 0),
        set_location(7, 13, 12, 2, 0), set_location(8, 13, 19, 6, 0),
        move_route(8, [step(40), step(41, "Nature", 0), step(40)], indent=0),
        cmd(223, [[0, 0, 0, 0], 0, False], 0), cmd(222), wait(36, 0),
    ]
    for who, line in [
        ("Nessa", "What happened to Latch?"), ("Marek", "Mud."),
        ("Nessa", "I can see the mud. Why is he wearing half the north road?"),
        ("Marek", "He found a ditch he disagreed with."),
        ("Elira", "Then both of you can leave the disagreement by the door."),
        ("Davren", "The west shutter caught again."),
        ("Elira", "Because the frame is warped."),
        ("Davren", "The hinge remains more cooperative."),
    ]:
        body += say(who, line, 0) + [wait(12, 0)]
    body += [cmd(221), set_location(-1, 15, 13, 8, 0),
             set_location(5, 16, 12, 4, 0), set_location(6, 14, 11, 2, 0),
             set_location(7, 13, 12, 6, 0), cmd(222), wait(36, 0)]
    for who, line in [
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
    ]:
        body += say(who, line, 0) + [wait(12, 0)]
    body += [
        cmd(221),
        move_route(5, [step(39)], indent=0), move_route(6, [step(39)], indent=0),
        move_route(7, [step(39)], indent=0), move_route(8, [step(39)], indent=0),
        set_location(9, 19, 9, 8, 0),
        move_route(9, [step(41, "Nature", 0), step(40), step(19)], indent=0),
        set_location(-1, 21, 5, 2, 0),
        move_route(-1, [step(41, "Damage1", 0), step(16)], indent=0),
        # Force a deterministic top-right bedroom frame using stock scrolling only.
        cmd(204, [8, 20, 6, True], 0), cmd(204, [6, 20, 6, True], 0),
        cmd(223, [[-68, -68, -32, 24], 60, True], 0), cmd(222), wait(75, 0),
        cmd(250, [{"name": "Ancient_ThreeNote_Resonance", "pan": 0,
                  "pitch": 100, "volume": 35}], 0), wait(105, 0),
        # The 3.4-second source cue occupies about 204 frames. These waits place
        # the wake during the cue and preserve roughly 120 silent frames after it.
        move_route(-1, [step(19)], indent=0), wait(219, 0),
        cmd(221), move_route(-1, [step(41, "Actor1", 0), step(16)], indent=0),
        cmd(121, [111, 111, 0], 0), cmd(122, [1, 1, 0, 0, 1012], 0),
        cmd(201, [0, 1, 14, 10, 2, 2], 0),
    ]
    c += exact_gate(body, 1011, 111)
    return c


def replace_event(map_data, event_id, pages):
    event = map_data["events"][event_id]
    event["pages"] = pages


def build_map002(baseline):
    data = copy.deepcopy(baseline)
    data["note"] = "MAP-002 Eventwright Functional Spine Pass 01; geometry from accepted Mapping Pass 01"
    replace_event(data, 1, [page(cond=conditions(switch=101, variable=1, value=1002),
                                 commands=morning_commands(), trigger=3, priority=0, through=True),
                            page(cond=conditions(switch=102), trigger=0, priority=0, through=True),
                            page(cond=conditions(variable=1, value=1003), trigger=0,
                                 priority=0, through=True)])
    replace_event(data, 2, [page(cond=conditions(switch=110, variable=1, value=1011),
                                 commands=evening_commands(), trigger=3, priority=0, through=True),
                            page(cond=conditions(switch=111), trigger=0, priority=0, through=True),
                            page(cond=conditions(variable=1, value=1012), trigger=0,
                                 priority=0, through=True)])

    # Family is visible before the intro. A higher SW102 page adds the approved ambient line.
    family = {
        5: (image("People1", 4, 4), "Davren", "If the latch catches again, leave it for this evening."),
        6: (image("People1", 5, 6), "Elira", "The survey office will still be there. Breakfast will not."),
        7: (image("People2", 2, 2), "Nessa", "Latch thinks every closed door is a personal insult."),
    }
    for eid, (img, who, line) in family.items():
        replace_event(data, eid, [page(image=img, commands=[], trigger=0, priority=1),
                                  page(cond=conditions(switch=102), image=img,
                                       commands=say(who, line, 0), trigger=0, priority=1)])
    replace_event(data, 8, [page(image=image("Nature", 0, 2), commands=[], priority=1)])
    replace_event(data, 9, [page(commands=[], priority=1, through=True)])
    replace_event(data, 15, [page(commands=[cmd(108, ["HOOK MAP-003: destination intentionally unresolved."])],
                                  priority=0, through=True)])
    return data


def patch_map001(baseline):
    data = copy.deepcopy(baseline)
    opening = data["events"][1]["pages"][0]["list"]
    hook = next(i for i, c in enumerate(opening)
                if c["code"] == 108 and c["parameters"] and
                c["parameters"][0].startswith("HOOK PRO-SC-002"))
    if opening[hook + 1]["code"] != 108 or opening[-1]["code"] != 0:
        raise ValueError("MAP-001 opening hook no longer matches accepted baseline")
    opening[hook:] = [cmd(108, ["HOOK PRO-SC-002: approved transfer to MAP-002 Morning."]),
                      cmd(201, [0, 2, 14, 14, 8, 2]), cmd(0)]
    return data


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--map001-baseline", type=Path, required=True)
    p.add_argument("--map002-baseline", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args()
    out = a.output_dir.resolve(); out.mkdir(parents=True, exist_ok=True)
    m1 = json.loads(a.map001_baseline.read_text(encoding="utf-8"))
    m2 = json.loads(a.map002_baseline.read_text(encoding="utf-8"))
    (out / "Map001_TRANSFER_PATCH_CANDIDATE.json").write_text(
        json.dumps(patch_map001(m1), separators=(",", ":")), encoding="utf-8")
    (out / "Map002.json").write_text(
        json.dumps(build_map002(m2), separators=(",", ":")), encoding="utf-8")
    print("Built MAP-002 Eventwright candidate and isolated MAP-001 transfer patch candidate")


if __name__ == "__main__":
    main()
