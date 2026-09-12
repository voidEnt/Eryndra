#!/usr/bin/env python3
"""Independent Validator for MAP-002 Eventwright Functional Spine Pass 01.

This script is Validator-owned. It reads Eventwright candidates and accepted
baselines but never modifies them.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from unittest import mock


STORY_SHA = "56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611"
SAMPLE_SHA = "b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768"
BASE1_SHA = "f6b6a5f5e90d4f48b3b886ee5b23a09a86fba802e4d28c3cacfbf5468d4a39f6"
BASE2_SHA = "429310b40f87053f669aca5377cd0544604d929b0e828a754d6ef966f78cdcd7"
CAND1_SHA = "98fec8f89e190531e5de74b525574769b59c79c2030a9fd2ac9a906c47d623cd"
CAND2_SHA = "fcf70f9e356c2b35ec72332129715f9ff6e856cb6a90003e5e3352dbf757c933"

MORNING = [
    ("Elira", "If you check that strap again, it may start charging you for the inspection."),
    ("Marek", "The stitching was loose."),
    ("Nessa", "It was loose the first time you checked it."),
    ("Marek", "Then the second check confirmed an excellent memory."),
    ("Davren", "A sound professional result."),
    ("Nessa", "Latch has been arguing with the door since sunrise."),
    ("Marek", "He dislikes closed questions."), ("Nessa", "Doors."),
    ("Marek", "Those too."), ("Davren", "It would have held another day."),
    ("Marek", "That's what it said yesterday."),
    ("Elira", "You checked it last night."),
    ("Marek", "I checked the measure. This is the buckle."),
    ("Nessa", "A separate crisis."), ("Marek", "Potentially."),
    ("Marek", "Joren's calibration weight."),
    ("Davren", "He would have remembered."), ("Marek", "Tomorrow, perhaps."),
    ("Elira", "Back before supper?"), ("Marek", "That was the assignment."),
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

FACES = {"Marek": ("Actor1", 0), "Davren": ("People1", 4),
         "Elira": ("People1", 5), "Nessa": ("People2", 2)}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    if root.exists():
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            h.update(str(path.relative_to(root)).encode())
            h.update(path.read_bytes())
    return h.hexdigest()


def flatten(data):
    for event in data["events"]:
        if event:
            for pi, page in enumerate(event["pages"]):
                for ci, command in enumerate(page["list"]):
                    yield event, pi, ci, command


def dialogue(page):
    rows, speaker, lines = [], None, []
    for command in page["list"]:
        if command["code"] == 101:
            if speaker is not None:
                rows.append((speaker, " ".join(lines)))
            speaker = command["parameters"][4]
            lines = []
        elif command["code"] == 401:
            lines.append(command["parameters"][0])
    if speaker is not None:
        rows.append((speaker, " ".join(lines)))
    return rows


def message_layout_ok(commands):
    count, active = 0, False
    for command in commands:
        if command["code"] == 101:
            if active and count == 0:
                return False
            count, active = 0, True
        elif command["code"] == 401:
            if not active or len(command["parameters"][0]) > 36:
                return False
            count += 1
            if count > 4:
                return False
        elif active:
            if count == 0:
                return False
            active = False
    return not active or count > 0


def find_index(commands, code, params=None):
    return next(i for i, c in enumerate(commands)
                if c["code"] == code and (params is None or c["parameters"] == params))


def page_condition_exact(page, *, switch, variable, value):
    c = page["conditions"]
    return (page["trigger"] == 3 and c["switch1Valid"] and c["switch1Id"] == switch
            and c["variableValid"] and c["variableId"] == variable
            and c["variableValue"] == value)


def exact_gate(commands, stage, off_switch):
    outer = {"code": 111, "indent": 0, "parameters": [1, 1, 0, stage, 0]}
    inner = {"code": 111, "indent": 1, "parameters": [0, off_switch, 1]}
    return (outer in commands and inner in commands
            and {"code": 412, "indent": 1, "parameters": []} in commands
            and {"code": 412, "indent": 0, "parameters": []} in commands)


def command_schema_ok(command):
    code, p = command["code"], command["parameters"]
    lengths = {0: 0, 101: 5, 108: 1, 111: None, 121: 3, 122: None,
               201: 6, 203: 5, 204: 4, 205: 2, 211: 1, 216: 1,
               221: 0, 222: 0, 223: 3, 230: 1, 250: 1, 401: 1, 412: 0}
    if code not in lengths:
        return False
    if lengths[code] is not None and len(p) != lengths[code]:
        return False
    if code == 111 and len(p) not in (3, 5):
        return False
    if code == 122 and len(p) < 5:
        return False
    if code == 205:
        route = p[1]
        if not isinstance(route, dict) or not route["list"] or route["list"][-1] != {"code": 0, "parameters": []}:
            return False
        for move in route["list"]:
            mlens = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 16: 0, 17: 0,
                     18: 0, 19: 0, 39: 0, 40: 0, 41: 2}
            if move["code"] not in mlens or len(move["parameters"]) != mlens[move["code"]]:
                return False
    return True


def fixture(parent: Path, name: str, base1: Path, base2: Path) -> Path:
    project = parent / name
    (project / "data").mkdir(parents=True)
    (project / "js").mkdir()
    (project / "Game.rmmzproject").write_text("RPGMZ 1.0.0", encoding="utf-8")
    (project / "js/rmmz_core.js").write_text("// MZ", encoding="utf-8")
    shutil.copy2(base1, project / "data/Map001.json")
    shutil.copy2(base2, project / "data/Map002.json")
    (project / "data/MapInfos.json").write_text(
        json.dumps([None, {"id": 1}, {"id": 2}]), encoding="utf-8")
    for rel in ("img/characters/Actor1.png", "img/characters/People1.png",
                "img/characters/People2.png", "img/characters/Nature.png",
                "img/characters/Damage1.png", "img/faces/Actor1.png",
                "img/faces/People1.png", "img/faces/People2.png",
                "audio/se/Ancient_ThreeNote_Resonance.ogg"):
        p = project / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"validator-fixture")
    return project


def run(a):
    m1 = json.loads(a.map001.read_text(encoding="utf-8"))
    b1 = json.loads(a.map001_baseline.read_text(encoding="utf-8"))
    m2 = json.loads(a.map002.read_text(encoding="utf-8"))
    b2 = json.loads(a.map002_baseline.read_text(encoding="utf-8"))
    results = []

    def check(name, condition, detail="", owner=None, severity=None):
        row = {"name": name, "status": "PASS" if condition else "FAIL", "detail": detail}
        if not condition:
            row["owner"] = owner or "Eventwright"
            row["severity"] = severity or "blocking"
        results.append(row)

    check("candidate JSON parses", True)
    check("immutable EryndraStory hash preserved", sha(a.story_zip) == STORY_SHA, sha(a.story_zip), "Other")
    check("immutable SampleGenerated hash preserved", sha(a.sample_zip) == SAMPLE_SHA, sha(a.sample_zip), "Other")
    check("accepted MAP-001 baseline hash", sha(a.map001_baseline) == BASE1_SHA, sha(a.map001_baseline), "Foreman")
    check("accepted MAP-002 baseline hash", sha(a.map002_baseline) == BASE2_SHA, sha(a.map002_baseline), "Foreman")
    check("candidate hashes are expected", sha(a.map001) == CAND1_SHA and sha(a.map002) == CAND2_SHA,
          f"Map001={sha(a.map001)} Map002={sha(a.map002)}")

    # Deterministic rebuild into an isolated temporary directory.
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        cp = subprocess.run([
            "python3", str(a.builder), "--map001-baseline", str(a.map001_baseline),
            "--map002-baseline", str(a.map002_baseline), "--output-dir", str(out)],
            capture_output=True, text=True)
        check("builder completes", cp.returncode == 0, cp.stderr.strip())
        check("MAP-001 rebuild deterministic", (out / a.map001.name).read_bytes() == a.map001.read_bytes())
        check("MAP-002 rebuild deterministic", (out / a.map002.name).read_bytes() == a.map002.read_bytes())

    check("MAP-002 dimensions/tileset/data preserved",
          all(m2[k] == b2[k] for k in ("width", "height", "tilesetId", "data")))
    check("MAP-002 non-event properties preserved except authorized note",
          all(m2[k] == b2[k] for k in b2 if k not in ("events", "note")))
    check("all 17 anchor identities and coordinates preserved",
          len(m2["events"]) == len(b2["events"]) and
          all(m2["events"][i][k] == b2["events"][i][k]
              for i in range(1, 18) for k in ("id", "name", "x", "y")))
    check("no additional MAP-002 events introduced", len(m2["events"]) == 18)

    p_m = m2["events"][1]["pages"][0]
    p_e = m2["events"][2]["pages"][0]
    ml, el = p_m["list"], p_e["list"]
    check("Morning page-level gate", page_condition_exact(p_m, switch=101, variable=1, value=1002))
    check("Morning exact equality and SW102-OFF nested gate", exact_gate(ml, 1002, 102))
    check("Morning anti-replay completion pages",
          len(m2["events"][1]["pages"]) == 3
          and m2["events"][1]["pages"][1]["conditions"]["switch1Id"] == 102
          and m2["events"][1]["pages"][1]["conditions"]["switch1Valid"]
          and m2["events"][1]["pages"][2]["conditions"]["variableValue"] == 1003
          and m2["events"][1]["pages"][2]["conditions"]["variableValid"])
    check("Evening page-level gate", page_condition_exact(p_e, switch=110, variable=1, value=1011))
    check("Evening exact equality and SW111-OFF nested gate", exact_gate(el, 1011, 111))
    check("Evening anti-replay completion pages",
          len(m2["events"][2]["pages"]) == 3
          and m2["events"][2]["pages"][1]["conditions"]["switch1Id"] == 111
          and m2["events"][2]["pages"][1]["conditions"]["switch1Valid"]
          and m2["events"][2]["pages"][2]["conditions"]["variableValue"] == 1012
          and m2["events"][2]["pages"][2]["conditions"]["variableValid"])

    check("Morning exact dialogue and beat order", dialogue(p_m) == MORNING, f"{len(dialogue(p_m))}/22 lines")
    check("Evening exact dialogue and beat order", dialogue(p_e) == EVENING, f"{len(dialogue(p_e))}/22 lines")
    check("every message respects face-window width and four-line MZ limit",
          all(message_layout_ok(page["list"]) for event in m2["events"] if event for page in event["pages"]))
    for label, page in (("Morning", p_m), ("Evening", p_e)):
        face_rows = [(c["parameters"][4], c["parameters"][0], c["parameters"][1])
                     for c in page["list"] if c["code"] == 101]
        check(f"{label} face/speaker placeholders exact",
              all(FACES[speaker] == (face, index) for speaker, face, index in face_rows))
    ambient = [("Davren", "If the latch catches again, leave it for this evening."),
               ("Elira", "The survey office will still be there. Breakfast will not."),
               ("Nessa", "Latch thinks every closed door is a personal insult.")]
    check("approved family ambient lines exact",
          [dialogue(m2["events"][i]["pages"][1])[0] for i in (5, 6, 7)] == ambient)
    check("Latch has no speech or thought text",
          dialogue(m2["events"][8]["pages"][0]) == []
          and dialogue(m2["events"][9]["pages"][0]) == [])

    all_commands = [c for *_, c in flatten(m2)]
    forbidden = {126, 127, 128, 301, 302, 355, 357, 655}
    check("no inventory/combat/shop/script/plugin commands",
          not any(c["code"] in forbidden for c in all_commands))
    check("all Eventwright command arrays match stock MZ schema",
          all(command_schema_ok(c) for c in all_commands))
    check("every event page terminates with command 0",
          all(page["list"] and page["list"][-1] == {"code": 0, "indent": 0, "parameters": []}
              for event in m2["events"] if event for page in event["pages"]))
    route_codes = [move["code"] for c in all_commands if c["code"] == 205
                   for move in c["parameters"][1]["list"]]
    check("movement routes contain no scripts or switch writes",
          not ({27, 28, 45} & set(route_codes)))

    setloc_m = [c["parameters"] for c in ml if c["code"] == 203]
    check("Morning initial staging exact", setloc_m[:5] == [
        [-1, 0, 14, 14, 8], [5, 0, 21, 13, 4], [6, 0, 7, 13, 6],
        [7, 0, 13, 12, 2], [8, 0, 13, 18, 2]])
    routes = [c["parameters"] for c in ml if c["code"] == 205 and c["parameters"][0] == -1]
    route_lists = [[x["code"] for x in p[1]["list"][:-1]] for p in routes]
    expected = [[1] * 5 + [16], [4] * 5 + [3] * 5 + [4] * 2 + [3] * 2 + [19],
                [17, 18], [17, 18], [18], [2] * 2 + [1] * 2 + [2] * 5 + [19]]
    check("Morning movement and inspection routes exact", route_lists == expected)

    # Directional stock-MZ passage checking, including source and destination sides.
    with zipfile.ZipFile(a.sample_zip) as z:
        flags = json.loads(z.read("SampleGenerated/data/Tilesets.json"))[3]["flags"]
    width, height = m2["width"], m2["height"]
    size = width * height
    layers = [m2["data"][i * size:(i + 1) * size] for i in range(4)]

    def pass_dir(x, y, direction):
        bit = {2: 1, 4: 2, 6: 4, 8: 8}[direction]
        for tile in reversed([layer[y * width + x] for layer in layers]):
            flag = flags[tile]
            if flag & 0x10:
                continue
            if flag & bit == 0:
                return True
            if flag & bit == bit:
                return False
        return False

    pos, traversed, passage = (14, 14), [], True
    for codes in ([1] * 5, [4] * 5 + [3] * 5 + [4] * 2 + [3] * 2,
                  [2] * 2 + [1] * 2 + [2] * 5):
        for code in codes:
            direction = {1: 2, 2: 4, 3: 6, 4: 8}[code]
            dx, dy = {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}[direction]
            nxt = (pos[0] + dx, pos[1] + dy)
            reverse = {2: 8, 4: 6, 6: 4, 8: 2}[direction]
            passage = passage and pass_dir(*pos, direction) and pass_dir(*nxt, reverse)
            traversed.append(nxt)
            pos = nxt
    check("Morning routes satisfy directional passability", passage, f"{len(traversed)} steps")
    occupied = {(21, 13), (7, 13), (13, 12), (13, 18)}
    check("Morning routes avoid active NPC collision cells", not (set(traversed) & occupied))
    check("Morning ends at release coordinate", pos == (14, 14))

    mi = find_index(ml, 121, [102, 102, 0])
    check("Morning state output/order exact",
          ml[mi:mi + 4] == [
              {"code": 121, "indent": 2, "parameters": [102, 102, 0]},
              {"code": 122, "indent": 2, "parameters": [1, 1, 0, 0, 1003]},
              {"code": 211, "indent": 2, "parameters": [1]},
              {"code": 216, "indent": 2, "parameters": [1]}])
    first_m_fade = find_index(ml, 222)
    check("Morning clears black tint and reveals Marek before Fade In",
          any(c["code"] == 223 and c["parameters"] == [[0, 0, 0, 0], 0, False]
              for c in ml[:first_m_fade])
          and any(c["code"] == 211 and c["parameters"] == [1] for c in ml[:first_m_fade]))

    setloc_e = [c["parameters"] for c in el if c["code"] == 203]
    check("Evening entry staging exact", setloc_e[:5] == [
        [-1, 0, 14, 19, 8], [5, 0, 21, 13, 4], [6, 0, 7, 13, 6],
        [7, 0, 13, 12, 2], [8, 0, 13, 19, 6]])
    supper = setloc_e[5:9]
    check("Supper stages four distinct approved positions",
          supper == [[-1, 0, 15, 13, 8], [5, 0, 16, 12, 4],
                     [6, 0, 14, 11, 2], [7, 0, 13, 12, 6]]
          and len({(p[2], p[3]) for p in supper}) == 4)
    check("Bedroom stages Latch and Marek exactly",
          setloc_e[9:11] == [[9, 0, 19, 9, 8], [-1, 0, 21, 5, 2]])
    bedroom_moves = [c for c in el if c["code"] == 205 and c["parameters"][0] == -1]
    check("Marek sleeping placeholder, wake pose, and Actor1 restore",
          any(any(x["code"] == 41 and x["parameters"] == ["Damage1", 0]
                  for x in c["parameters"][1]["list"]) for c in bedroom_moves)
          and any(any(x["code"] == 19 for x in c["parameters"][1]["list"])
                  for c in bedroom_moves)
          and any(any(x["code"] == 41 and x["parameters"] == ["Actor1", 0]
                  for x in c["parameters"][1]["list"]) for c in bedroom_moves))
    check("threshold Latch faces north, is visible, and is silent",
          any(c["code"] == 205 and c["parameters"][0] == 9
              and any(x["code"] == 19 for x in c["parameters"][1]["list"]) for c in el))
    check("bedroom camera uses stock deterministic scroll",
          [c["parameters"] for c in el if c["code"] == 204] == [[8, 20, 6, True], [6, 20, 6, True]])
    check("restrained night tint precedes bedroom Fade In",
          any(c["code"] == 223 and c["parameters"] == [[-68, -68, -32, 24], 60, True]
              for c in el))

    ses = [c["parameters"][0] for c in all_commands if c["code"] == 250]
    check("Morning Dog SE occurs exactly once and evening has none",
          sum(s["name"] == "Dog" for s in ses) == 1
          and not any(c["code"] == 250 and c["parameters"][0]["name"] == "Dog" for c in el))
    check("repair SE occurs exactly once at restrained settings",
          sum(s == {"name": "Equip1", "pan": 0, "pitch": 95, "volume": 45} for s in ses) == 1)
    check("night three-note cue occurs exactly once at faint volume",
          sum(s == {"name": "Ancient_ThreeNote_Resonance", "pan": 0,
                    "pitch": 100, "volume": 35} for s in ses) == 1)
    sei = next(i for i, c in enumerate(el)
               if c["code"] == 250 and c["parameters"][0]["name"] == "Ancient_ThreeNote_Resonance")
    waits = [c["parameters"][0] for c in el[sei + 1:] if c["code"] == 230]
    check("night cue schedule preserves wake and post-cue silence", waits[:2] == [105, 219],
          "3.4-second cue; approximately 120 silent frames before fade")

    transfers = [c["parameters"] for c in all_commands if c["code"] == 201]
    check("MAP-002 has one exact evening transfer under black",
          transfers == [[0, 1, 14, 10, 2, 2]] and any(c["code"] == 221 for c in el[:find_index(el, 201)]))
    check("MAP-003 remains an inactive unresolved hook",
          transfers == [[0, 1, 14, 10, 2, 2]]
          and any(c["code"] == 108 and "HOOK MAP-003" in c["parameters"][0]
                  for c in m2["events"][15]["pages"][0]["list"]))
    ei = find_index(el, 121, [111, 111, 0])
    check("Evening state output and transfer order exact",
          el[ei:ei + 3] == [
              {"code": 121, "indent": 2, "parameters": [111, 111, 0]},
              {"code": 122, "indent": 2, "parameters": [1, 1, 0, 0, 1012]},
              {"code": 201, "indent": 2, "parameters": [0, 1, 14, 10, 2, 2]}])
    switch_writes = [c["parameters"] for c in all_commands if c["code"] == 121]
    variable_writes = [c["parameters"] for c in all_commands if c["code"] == 122]
    check("no unapproved MAP-002 global state writes",
          switch_writes == [[102, 102, 0], [111, 111, 0]]
          and variable_writes == [[1, 1, 0, 0, 1003], [1, 1, 0, 0, 1012]])

    # MAP-001 may differ only from the approved hook to end of opening page.
    bcopy, ccopy = copy.deepcopy(b1), copy.deepcopy(m1)
    bl = bcopy["events"][1]["pages"][0]["list"]
    cl = ccopy["events"][1]["pages"][0]["list"]
    bi = next(i for i, c in enumerate(bl) if c["code"] == 108 and c["parameters"][0].startswith("HOOK PRO-SC-002"))
    ci = next(i for i, c in enumerate(cl) if c["code"] == 108 and c["parameters"][0].startswith("HOOK PRO-SC-002"))
    bcopy["events"][1]["pages"][0]["list"] = bl[:bi]
    ccopy["events"][1]["pages"][0]["list"] = cl[:ci]
    check("MAP-001 differs only at authorized opening tail", bcopy == ccopy and bl[:bi] == cl[:ci])
    check("MAP-001 authorized transfer tail exact", cl[ci:] == [
        {"code": 108, "indent": 0, "parameters": ["HOOK PRO-SC-002: approved transfer to MAP-002 Morning."]},
        {"code": 201, "indent": 0, "parameters": [0, 2, 14, 14, 8, 2]},
        {"code": 0, "indent": 0, "parameters": []}])
    check("MAP-001 retained validated final state writes", cl[ci - 2:ci] == [
        {"code": 121, "indent": 0, "parameters": [101, 101, 0]},
        {"code": 122, "indent": 0, "parameters": [1, 1, 0, 0, 1002]}])

    # Installer tests performed independently against isolated disposable fixtures.
    spec = importlib.util.spec_from_file_location("map002_installer", a.installer)
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for name in ("EryndraStory.zip", "SampleGenerated.zip"):
            archive = tmp / name
            archive.write_bytes(b"immutable-test")
            before = archive.read_bytes()
            refused = False
            try:
                installer.install(archive, a.package_dir)
            except installer.Refusal:
                refused = True
            check(f"installer refuses {name} without mutation", refused and archive.read_bytes() == before)

        sample = fixture(tmp, "SampleGenerated_reference", a.map001_baseline, a.map002_baseline)
        before = tree_hash(sample)
        refused = False
        try:
            installer.install(sample, a.package_dir)
        except installer.Refusal:
            refused = True
        check("installer refuses named extracted reference tree byte-identically",
              refused and tree_hash(sample) == before)

        bad = fixture(tmp, "MissingAsset", a.map001_baseline, a.map002_baseline)
        (bad / "img/characters/Nature.png").unlink()
        before = tree_hash(bad)
        refused = False
        try:
            installer.install(bad, a.package_dir)
        except installer.Refusal:
            refused = True
        check("installer missing-asset refusal is byte-identical", refused and tree_hash(bad) == before)

        wrong = fixture(tmp, "WrongBaseline", a.map001_baseline, a.map002_baseline)
        (wrong / "data/Map002.json").write_text("{}", encoding="utf-8")
        before = tree_hash(wrong)
        refused = False
        try:
            installer.install(wrong, a.package_dir)
        except installer.Refusal:
            refused = True
        check("installer wrong-baseline refusal is byte-identical", refused and tree_hash(wrong) == before)

        dry = fixture(tmp, "DryRun", a.map001_baseline, a.map002_baseline)
        before = tree_hash(dry)
        result = installer.install(dry, a.package_dir, True)
        check("installer dry-run performs no writes", result is None and tree_hash(dry) == before)

        good = fixture(tmp, "Good", a.map001_baseline, a.map002_baseline)
        backup = installer.install(good, a.package_dir)
        check("installer success writes exact candidates and recoverable backup",
              backup is not None and backup.is_dir()
              and (good / "data/Map001.json").read_bytes() == a.map001.read_bytes()
              and (good / "data/Map002.json").read_bytes() == a.map002.read_bytes()
              and (backup / "Map001.json").read_bytes() == a.map001_baseline.read_bytes()
              and (backup / "Map002.json").read_bytes() == a.map002_baseline.read_bytes())

        rollback = fixture(tmp, "Rollback", a.map001_baseline, a.map002_baseline)
        before1 = (rollback / "data/Map001.json").read_bytes()
        before2 = (rollback / "data/Map002.json").read_bytes()
        real_replace, calls = os.replace, 0

        def fail_second(src, dst):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected second replacement failure")
            return real_replace(src, dst)

        failed = False
        try:
            with mock.patch.object(installer.os, "replace", side_effect=fail_second):
                installer.install(rollback, a.package_dir)
        except OSError:
            failed = True
        check("installer rolls back both maps after partial replacement failure",
              failed and (rollback / "data/Map001.json").read_bytes() == before1
              and (rollback / "data/Map002.json").read_bytes() == before2)

    failed_rows = [r for r in results if r["status"] == "FAIL"]
    return results, failed_rows


def main():
    p = argparse.ArgumentParser()
    for name in ("map001", "map001_baseline", "map002", "map002_baseline",
                 "story_zip", "sample_zip", "builder", "installer", "package_dir"):
        p.add_argument("--" + name.replace("_", "-"), dest=name, type=Path, required=True)
    p.add_argument("--json-output", type=Path, required=True)
    p.add_argument("--text-output", type=Path, required=True)
    a = p.parse_args()
    results, failures = run(a)
    passed = len(results) - len(failures)
    static_outcome = "PASS" if not failures else "FAIL"
    overall = "CONDITIONAL PASS" if not failures else "FAIL"
    payload = {
        "validator": "Independent MAP-002 Eventwright Validator",
        "scope": "Functional Spine Pass 01 static and installer validation",
        "static_outcome": static_outcome,
        "overall_outcome": overall,
        "summary": {"passed": passed, "failed": len(failures), "total": len(results)},
        "runtime_conditions": [
            "MAP-001 opening regression and transfer into MAP-002 Morning",
            "Morning presentation, movement, player release, state, interaction, and no replay after save/load",
            "Evening direct setup, staging, single faint cue, silence, black transfer, and MAP-001 Omen handoff",
            "Evening no replay after completion/save-load",
        ],
        "results": results,
    }
    text = "\n".join(
        f"{r['status']}: {r['name']}" + (f" — {r['detail']}" if r["detail"] else "")
        for r in results)
    text += (f"\nSUMMARY: {passed}/{len(results)} PASS\n"
             f"STATIC EVENTWRIGHT SCOPE: {static_outcome}\n"
             f"OVERALL HANDOFF: {overall} (pending user-side MZ runtime tests)\n")
    a.json_output.parent.mkdir(parents=True, exist_ok=True)
    a.json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    a.text_output.write_text(text, encoding="utf-8")
    print(text, end="")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
