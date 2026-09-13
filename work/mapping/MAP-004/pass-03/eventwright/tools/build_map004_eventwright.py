#!/usr/bin/env python3
"""Build MAP-004 Eventwright Functional Spine Pass 01.

The builder copies the accepted MAP-004 Mapping Pass 03 and MAP-003 Mapping
Pass 02 baselines, changes event commands only, and writes deterministic JSON.
The immutable story/reference ZIP files are never opened or modified here.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


def command(code: int, parameters=None, indent: int = 0) -> dict:
    return {"code": code, "indent": indent, "parameters": parameters or []}


def conditions(*, switch: int | None = None, variable: int | None = None,
               value: int = 0) -> dict:
    return {
        "actorId": 1, "actorValid": False,
        "itemId": 1, "itemValid": False,
        "selfSwitchCh": "A", "selfSwitchValid": False,
        "switch1Id": switch or 1, "switch1Valid": switch is not None,
        "switch2Id": 1, "switch2Valid": False,
        "variableId": variable or 1, "variableValid": variable is not None,
        "variableValue": value,
    }


def character_image(name: str, index: int, direction: int) -> dict:
    return {
        "characterIndex": index, "characterName": name,
        "direction": direction, "pattern": 1, "tileId": 0,
    }


def page(*, cond=None, image=None, commands=None, trigger: int = 0,
         priority: int = 0, through: bool = True,
         direction_fix: bool = False) -> dict:
    return {
        "conditions": cond or conditions(),
        "directionFix": direction_fix,
        "image": image or character_image("", 0, 2),
        "list": (commands or []) + [command(0)],
        "moveFrequency": 3,
        "moveRoute": {
            "list": [{"code": 0, "parameters": []}],
            "repeat": True, "skippable": False, "wait": False,
        },
        "moveSpeed": 3, "moveType": 0, "priorityType": priority,
        "stepAnime": False, "through": through, "trigger": trigger,
        "walkAnime": True,
    }


def move_step(code: int, *parameters) -> dict:
    return {"code": code, "parameters": list(parameters)}


def forced_route(character_id: int, steps: list[dict], indent: int = 2) -> dict:
    route = {
        "list": steps + [move_step(0)],
        "repeat": False, "skippable": False, "wait": True,
    }
    return command(205, [character_id, route], indent)


def show_text(speaker: str, lines: list[str], indent: int = 2) -> list[dict]:
    if not 1 <= len(lines) <= 4:
        raise ValueError(f"{speaker}: Show Text requires one to four lines")
    if any(len(line) > 40 for line in lines):
        raise ValueError(f"{speaker}: dialogue line exceeds 40 visible characters")
    return [
        command(101, ["", 0, 0, 2, speaker], indent),
        *(command(401, [line], indent) for line in lines),
    ]


def exact_scene(body: list[dict], *, stage: int, switch: int) -> list[dict]:
    """Run body only when StoryStage equals stage and completion is OFF."""
    result = [
        command(111, [1, 1, 0, stage, 0], 0),
        command(111, [0, switch, 1], 1),
    ]
    for item in body:
        shifted = copy.deepcopy(item)
        shifted["indent"] += 2
        result.append(shifted)
    result.extend([command(412, [], 1), command(412, [], 0)])
    return result


MORNING_DIALOGUE = [
    ("Joren", ["Morning, Marek. The north road needs", "a second pair of eyes."]),
    ("Joren", ["A road crew says one old marker no", "longer agrees with the recorded line."]),
    ("Joren", ["Likely a minor ground shift. Verify", "the road and boundary marks."]),
    ("Joren", ["Correct the measurement, note it in", "the ledger, and be back before supper."]),
    ("Edrin", ["Before he turns a misplaced stone", "into a diplomatic crisis, you mean."]),
    ("Marek", ["Roads only stay boring because", "someone notices the stones."]),
    ("Edrin", ["There he is. I worried the morning", "had made you agreeable."]),
    ("Joren", ["Edrin has his own inspection along", "the first stretch. Take the north road."]),
    ("Marek", ["Understood. I'll report when we're back."]),
]


REPORT_DIALOGUE = [
    ("Joren", ["You're back. What did you find?"]),
    ("Marek", ["The marker shifted uphill. The soil", "around it wasn't freshly disturbed."]),
    ("Marek", ["Above it, the slope opened onto worked", "masonry absent from our records."]),
    ("Marek", ["It may be an old substructure. Road", "risk uncertain. Inspect it properly."]),
    ("Joren", ["I'll mark the site for examination.", "Anything else?"]),
    ("Marek", ["I heard three tones inside. Evenly", "spaced. I couldn't identify the source."]),
    ("Marek", ["For a moment, I thought the stone—"]),
    ("Marek", ["No. Record that the sound came from", "within the structure."]),
    ("Joren", ["I will. You don't decorate reports,", "so uncertainty belongs in this one."]),
    ("Edrin", ["My route offered a washed shoulder", "and a wagoner arguing with the rain."]),
    ("Edrin", ["You win the stranger report."]),
    ("Marek", ["I would rather not."]),
    ("Joren", ["We'll examine it properly. For now,", "go home. Supper has seniority."]),
]


def scene_commands(scene: str) -> list[dict]:
    if scene == "morning":
        stage, switch, next_stage = 1004, 103, 1005
        dialogue = MORNING_DIALOGUE
        label = "PRO-SC-004 / The Survey Assignment"
    elif scene == "report":
        stage, switch, next_stage = 1010, 110, 1011
        dialogue = REPORT_DIALOGUE
        label = "PRO-SC-010 / The Report"
    else:
        raise ValueError(scene)

    body = [
        command(108, [label], 0),
        command(216, [1], 0),  # Followers OFF; Prologue exploration is solo.
        forced_route(-1, [move_step(4), move_step(4), move_step(4), move_step(19)], 0),
    ]
    for speaker, lines in dialogue:
        body.extend(show_text(speaker, lines, 0))
    body.extend([
        command(121, [switch, switch, 0], 0),
        command(122, [1, 1, 0, 0, next_stage], 0),
        command(216, [1], 0),  # Restore the intended followers-OFF solo state.
    ])
    return exact_scene(body, stage=stage, switch=switch)


def replace_pages(map_data: dict, event_id: int, pages: list[dict]) -> None:
    map_data["events"][event_id]["pages"] = pages


def build_map004(baseline: dict) -> dict:
    data = copy.deepcopy(baseline)
    data["note"] = (
        "MAP-004 Eventwright Functional Spine Pass 01; geometry preserved "
        "from accepted Mapping Pass 03"
    )

    # A stage-ceiling blank page prevents an autorun page whose MZ condition is
    # necessarily >= from monopolizing input if a debug/save state is inconsistent.
    replace_pages(data, 1, [
        page(cond=conditions(variable=1, value=1004),
             commands=scene_commands("morning"), trigger=3),
        page(cond=conditions(variable=1, value=1005)),
        page(cond=conditions(switch=103)),
    ])
    replace_pages(data, 2, [
        page(cond=conditions(variable=1, value=1010),
             commands=scene_commands("report"), trigger=3),
        page(cond=conditions(variable=1, value=1011)),
        page(cond=conditions(switch=110)),
    ])

    # Placeholder graphics establish no final appearance canon.
    joren = character_image("People1", 4, 2)
    edrin = character_image("People1", 0, 6)
    replace_pages(data, 3, [page(image=joren, priority=1, through=False)])
    replace_pages(data, 4, [
        page(),
        page(cond=conditions(variable=1, value=1004), image=edrin,
             priority=1, through=False),
        page(cond=conditions(variable=1, value=1005)),
        page(cond=conditions(variable=1, value=1010), image=edrin,
             priority=1, through=False),
    ])
    replace_pages(data, 5, [
        page(commands=[command(201, [0, 3, 31, 16, 2, 0])],
             trigger=0, priority=1, through=False),
    ])
    # IDs 6-8 remain byte-equivalent to the Mapping baseline.
    return data


def build_map003_patch(baseline: dict) -> dict:
    data = copy.deepcopy(baseline)
    transfer_commands = [
        command(108, ["MAP-003 office door / MAP-004 integration"], 0),
        command(111, [1, 1, 0, 1003, 0], 0),
        command(122, [1, 1, 0, 0, 1004], 1),
        command(412, [], 0),
        command(201, [0, 4, 12, 15, 8, 0], 0),
    ]
    replace_pages(data, 2, [
        page(cond=conditions(variable=1, value=1003),
             commands=transfer_commands, trigger=0,
             priority=1, through=False),
    ])
    return data


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")),
                    encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map004-baseline", type=Path, required=True)
    parser.add_argument("--map003-baseline", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    map004 = json.loads(args.map004_baseline.read_text(encoding="utf-8"))
    map003 = json.loads(args.map003_baseline.read_text(encoding="utf-8"))
    write_json(args.output_dir / "Map004.json", build_map004(map004))
    write_json(args.output_dir / "Map003_EVENT2_PATCH_CANDIDATE.json",
               build_map003_patch(map003))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
