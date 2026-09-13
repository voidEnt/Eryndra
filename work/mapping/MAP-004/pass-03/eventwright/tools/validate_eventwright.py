#!/usr/bin/env python3
"""Static self-validation for MAP-004 Eventwright Functional Spine Pass 01."""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def commands(event: dict) -> list[dict]:
    return [item for page in event["pages"] for item in page["list"]]


def text_sequence(event: dict) -> list[tuple[str, list[str]]]:
    out = []
    for page in event["pages"]:
        current = None
        for item in page["list"]:
            if item["code"] == 101:
                current = (item["parameters"][4], [])
                out.append(current)
            elif item["code"] == 401 and current is not None:
                current[1].append(item["parameters"][0])
            elif item["code"] not in (401,):
                current = None
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", type=Path, required=True)
    parser.add_argument("--map004-baseline", type=Path, required=True)
    parser.add_argument("--map003-baseline", type=Path, required=True)
    parser.add_argument("--results-json", type=Path, required=True)
    parser.add_argument("--results-text", type=Path, required=True)
    args = parser.parse_args()

    candidate004 = load(args.candidate_dir / "Map004.json")
    candidate003 = load(args.candidate_dir / "Map003_EVENT2_PATCH_CANDIDATE.json")
    baseline004 = load(args.map004_baseline)
    baseline003 = load(args.map003_baseline)

    spec = importlib.util.spec_from_file_location(
        "builder", args.candidate_dir / "tools" / "build_map004_eventwright.py")
    builder = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(builder)

    checks: list[dict] = []

    def check(name: str, passed: bool, detail: str = ""):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    check("MAP-004 dimensions and tileset preserved",
          (candidate004["width"], candidate004["height"], candidate004["tilesetId"]) ==
          (baseline004["width"], baseline004["height"], baseline004["tilesetId"]))
    check("MAP-004 tile/collision array byte-equivalent",
          candidate004["data"] == baseline004["data"])
    top_keys = set(baseline004) - {"events", "note"}
    check("MAP-004 non-event map properties preserved",
          all(candidate004[k] == baseline004[k] for k in top_keys))
    check("MAP-004 anchor identities and coordinates preserved",
          all(candidate004["events"][i][k] == baseline004["events"][i][k]
              for i in range(1, 9) for k in ("id", "name", "x", "y")))
    check("MAP-004 prop/camera anchors 6-8 remain inert and byte-equivalent",
          all(candidate004["events"][i] == baseline004["events"][i]
              for i in (6, 7, 8)))

    top003 = set(baseline003) - {"events"}
    check("MAP-003 map geometry and properties byte-equivalent",
          all(candidate003[k] == baseline003[k] for k in top003))
    check("Only MAP-003 event ID 2 differs",
          all(candidate003["events"][i] == baseline003["events"][i]
              for i in range(len(baseline003["events"])) if i != 2) and
          candidate003["events"][2] != baseline003["events"][2])

    e1, e2 = candidate004["events"][1], candidate004["events"][2]
    check("Morning controller begins at >=1004 autorun",
          e1["pages"][0]["conditions"]["variableId"] == 1 and
          e1["pages"][0]["conditions"]["variableValue"] == 1004 and
          e1["pages"][0]["trigger"] == 3)
    check("Report controller begins at >=1010 autorun",
          e2["pages"][0]["conditions"]["variableId"] == 1 and
          e2["pages"][0]["conditions"]["variableValue"] == 1010 and
          e2["pages"][0]["trigger"] == 3)
    check("Morning exact equality and SW103-OFF guards present",
          [111, 111] == [c["code"] for c in e1["pages"][0]["list"][:2]] and
          e1["pages"][0]["list"][0]["parameters"] == [1, 1, 0, 1004, 0] and
          e1["pages"][0]["list"][1]["parameters"] == [0, 103, 1])
    check("Report exact equality and SW110-OFF guards present",
          [111, 111] == [c["code"] for c in e2["pages"][0]["list"][:2]] and
          e2["pages"][0]["list"][0]["parameters"] == [1, 1, 0, 1010, 0] and
          e2["pages"][0]["list"][1]["parameters"] == [0, 110, 1])
    check("Completion and stage-ceiling blank pages prevent controller replay",
          len(e1["pages"]) == 3 and len(e2["pages"]) == 3 and
          e1["pages"][2]["conditions"]["switch1Id"] == 103 and
          e2["pages"][2]["conditions"]["switch1Id"] == 110 and
          e1["pages"][1]["conditions"]["variableValue"] == 1005 and
          e2["pages"][1]["conditions"]["variableValue"] == 1011 and
          all(p["trigger"] == 0 for p in e1["pages"][1:] + e2["pages"][1:]))

    check("Morning dialogue speakers, order, wording and line breaks exact",
          text_sequence(e1) == builder.MORNING_DIALOGUE)
    check("Report dialogue speakers, order, wording and line breaks exact",
          text_sequence(e2) == builder.REPORT_DIALOGUE)
    all_text = text_sequence(e1) + text_sequence(e2)
    check("All Show Text content lines are <=40 characters",
          all(len(line) <= 40 for _, lines in all_text for line in lines),
          f"maximum={max(len(line) for _, lines in all_text for line in lines)}")
    check("Every Show Text box uses speaker name and at most four lines",
          all(speaker and 1 <= len(lines) <= 4 for speaker, lines in all_text))

    def state_positions(event, switch, stage):
        cmds = commands(event)
        sw = [i for i, c in enumerate(cmds)
              if c["code"] == 121 and c["parameters"] == [switch, switch, 0]]
        vr = [i for i, c in enumerate(cmds)
              if c["code"] == 122 and c["parameters"] == [1, 1, 0, 0, stage]]
        return sw, vr
    m_sw, m_vr = state_positions(e1, 103, 1005)
    r_sw, r_vr = state_positions(e2, 110, 1011)
    check("Morning writes only SW103 then stage1005 exactly once",
          len(m_sw) == len(m_vr) == 1 and m_sw[0] < m_vr[0])
    check("Report writes only SW110 then stage1011 exactly once",
          len(r_sw) == len(r_vr) == 1 and r_sw[0] < r_vr[0])
    all_writes = [(c["code"], c["parameters"]) for event in (e1, e2)
                  for c in commands(event) if c["code"] in (121, 122)]
    check("No unauthorized MAP-004 global state writes",
          all_writes == [(121, [103, 103, 0]), (122, [1, 1, 0, 0, 1005]),
                         (121, [110, 110, 0]), (122, [1, 1, 0, 0, 1011])])

    for label, event in (("Morning", e1), ("Report", e2)):
        routes = [c for c in commands(event) if c["code"] == 205]
        ok = len(routes) == 1 and routes[0]["parameters"][0] == -1
        if ok:
            rcodes = [r["code"] for r in routes[0]["parameters"][1]["list"]]
            ok = rcodes == [4, 4, 4, 19, 0]
        check(f"{label} stages player from (12,15) to (12,12) facing north", ok)

    office_door = candidate004["events"][5]["pages"][0]
    transfer_out = [c for c in office_door["list"] if c["code"] == 201]
    check("MAP-004 door transfers to MAP-003 (31,16) south with black fade",
          len(transfer_out) == 1 and transfer_out[0]["parameters"] == [0, 3, 31, 16, 2, 0] and
          office_door["trigger"] == 0 and office_door["priorityType"] == 1)

    town_door = candidate003["events"][2]["pages"][0]
    town_cmds = town_door["list"]
    transfer_in = [c for c in town_cmds if c["code"] == 201]
    stage_entry = [c for c in town_cmds if c["code"] == 122]
    check("MAP-003 office door active only from stage1003 onward",
          town_door["conditions"]["variableId"] == 1 and
          town_door["conditions"]["variableValue"] == 1003)
    check("MAP-003 stage1003 equality guard advances to1004 only",
          any(c["code"] == 111 and c["parameters"] == [1, 1, 0, 1003, 0]
              for c in town_cmds) and stage_entry == [
                  {"code": 122, "indent": 1, "parameters": [1, 1, 0, 0, 1004]}])
    check("MAP-003 door transfers to MAP-004 (12,15) north with black fade",
          len(transfer_in) == 1 and transfer_in[0]["parameters"] == [0, 4, 12, 15, 8, 0] and
          town_door["trigger"] == 0 and town_door["priorityType"] == 1)

    edrin_pages = candidate004["events"][4]["pages"]
    check("Edrin visibility bands are hidden/base, visible1004, hidden1005, visible1010",
          len(edrin_pages) == 4 and
          edrin_pages[0]["image"]["characterName"] == "" and
          edrin_pages[1]["conditions"]["variableValue"] == 1004 and
          edrin_pages[1]["image"]["characterName"] == "People1" and
          edrin_pages[2]["conditions"]["variableValue"] == 1005 and
          edrin_pages[2]["image"]["characterName"] == "" and
          edrin_pages[3]["conditions"]["variableValue"] == 1010 and
          edrin_pages[3]["image"]["characterName"] == "People1")
    check("Joren and Edrin stock placeholders are distinct",
          candidate004["events"][3]["pages"][0]["image"] !=
          edrin_pages[1]["image"])

    allowed = {0, 101, 108, 111, 121, 122, 201, 205, 216, 401, 412}
    used = {c["code"] for event in candidate004["events"][1:6] for c in commands(event)}
    used |= {c["code"] for c in town_cmds}
    check("No unauthorized command types", used <= allowed,
          f"used={sorted(used)}")
    forbidden = {117, 125, 126, 127, 129, 132, 212, 223, 224, 225, 231, 232,
                 241, 245, 249, 250, 251, 261, 301, 302, 303, 355, 356, 357}
    check("No combat/audio/picture/tint/shake/plugin/script commands", not (used & forbidden))

    with tempfile.TemporaryDirectory() as temp:
        out = Path(temp)
        rebuilt004 = builder.build_map004(baseline004)
        rebuilt003 = builder.build_map003_patch(baseline003)
        check("Deterministic builder reproduces Map004.json", rebuilt004 == candidate004)
        check("Deterministic builder reproduces MAP-003 integration candidate",
              rebuilt003 == candidate003)

    passed = sum(c["passed"] for c in checks)
    result = {"suite": "MAP-004 Eventwright self-validation",
              "passed": passed, "total": len(checks), "checks": checks,
              "independent_validation": "NOT RUN",
              "runtime_validation": "NOT RUN"}
    args.results_json.parent.mkdir(parents=True, exist_ok=True)
    args.results_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [f"MAP-004 Eventwright self-validation: {passed}/{len(checks)} PASS"]
    lines += [f"{'PASS' if c['passed'] else 'FAIL'}: {c['name']}" +
              (f" — {c['detail']}" if c["detail"] else "") for c in checks]
    lines += ["Independent Validation: NOT RUN", "RPG Maker MZ runtime: NOT RUN"]
    args.results_text.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[0])
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
