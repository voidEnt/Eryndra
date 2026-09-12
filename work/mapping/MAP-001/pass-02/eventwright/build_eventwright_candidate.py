#!/usr/bin/env python3
"""Build MAP-001 Pass 02 from the accepted Pass 01 geometry.

This script only reads the accepted map and writes into this Eventwright folder.
It never reads from or writes to either immutable ZIP package.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PASS02 = HERE.parent
REPO = HERE.parents[4]
SOURCE_MAP = REPO / "work/mapping/MAP-001/pass-01/Map001.json"
OUTPUT_MAP = HERE / "Map001.json"
RESULTS = HERE / "build_results.json"


def command(code: int, parameters: list, indent: int = 0) -> dict:
    return {"code": code, "indent": indent, "parameters": parameters}


def comment(text: str) -> dict:
    return command(108, [text])


def empty_page(*, trigger: int = 0, switch: int | None = None,
               variable: tuple[int, int] | None = None,
               self_switch: str | None = None, commands: list[dict] | None = None) -> dict:
    conditions = {
        "actorId": 1, "actorValid": False,
        "itemId": 1, "itemValid": False,
        "selfSwitchCh": self_switch or "A", "selfSwitchValid": self_switch is not None,
        "switch1Id": switch or 1, "switch1Valid": switch is not None,
        "switch2Id": 1, "switch2Valid": False,
        "variableId": variable[0] if variable else 1,
        "variableValid": variable is not None,
        "variableValue": variable[1] if variable else 0,
    }
    return {
        "conditions": conditions,
        "directionFix": False,
        "image": {"characterIndex": 0, "characterName": "", "direction": 2,
                  "pattern": 1, "tileId": 0},
        "list": (commands or []) + [command(0, [])],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True,
                      "skippable": False, "wait": False},
        "moveSpeed": 3, "moveType": 0, "priorityType": 0,
        "stepAnime": False, "through": True, "trigger": trigger, "walkAnime": True,
    }


def show_picture(number: int, name: str, opacity: int = 255) -> dict:
    # id, name, upper-left origin, direct coordinates, x, y, scale x/y,
    # opacity, normal blend
    return command(231, [number, name, 0, 0, 0, 0, 100, 100, opacity, 0])


def move_picture(number: int, opacity: int, duration: int, wait: bool) -> dict:
    # id, upper-left origin, direct coordinates, x, y, scale x/y, opacity,
    # normal blend, duration, wait, constant-speed easing
    return command(232, [number, 0, 0, 0, 0, 100, 100, opacity, 0,
                         duration, wait, 0])


def opening_commands() -> list[dict]:
    return [
        comment("PRO-SC-001 / P-01 — The Forgotten Place"),
        command(211, [0]),                         # player transparency ON
        command(216, [1]),                         # followers hidden
        command(121, [100, 100, 0]),               # SW-0100 ON
        command(122, [1, 1, 0, 0, 1001]),          # VR-0001 = 1001
        command(223, [[-255, -255, -255, 0], 0, False]),
        command(230, [30]),
        comment("Slow reveal of the dormant chamber"),
        command(223, [[-24, -24, -28, 8], 180, True]),
        command(230, [150]),
        comment("Reframe from chamber camera to ring camera"),
        command(204, [8, 2, 4, True]),             # scroll up 2 tiles
        show_picture(5, "MAP001_Dust_Tremor", 0),
        move_picture(5, 80, 18, False),
        command(225, [2, 4, 36, True]),
        move_picture(5, 0, 24, True),
        command(235, [5]),
        show_picture(2, "MAP001_Ring_Pulse", 0),
        move_picture(2, 190, 15, True),
        command(250, [{"name": "Ancient_ThreeNote_Resonance", "pan": 0,
                       "pitch": 100, "volume": 80}]),
        command(230, [210]),                       # 3.4 s cue + small tail
        move_picture(2, 0, 18, True),
        command(235, [2]),
        command(230, [24]),                        # full dark beat before residual returns
        show_picture(3, "MAP001_Ring_Residual", 115),
        command(230, [120]),
        command(221, []),                          # fade out
        command(235, [3]),
        command(223, [[-255, -255, -255, 0], 0, False]),
        comment("Narrative title reveal; this is a picture, not Go To Title"),
        show_picture(6, "SYS_Eryndra_Title", 0),
        command(222, []),                          # fade in over black-tinted map
        move_picture(6, 255, 45, True),
        command(230, [90]),
        move_picture(6, 0, 45, True),
        command(235, [6]),
        command(121, [101, 101, 0]),               # SW-0101 ON
        command(122, [1, 1, 0, 0, 1002]),          # VR-0001 = 1002
        comment("HOOK PRO-SC-002: insert approved transfer to MAP-002 here."),
        comment("Proof build ends cleanly on black; destination is intentionally unresolved."),
    ]


def omen_commands() -> list[dict]:
    return [
        comment("PRO-SC-012 / P-08 — MAP-001 portion of The Omen"),
        command(211, [0]),
        command(216, [1]),
        command(223, [[-255, -255, -255, 0], 0, False]),
        command(230, [30]),
        command(223, [[-24, -24, -28, 8], 120, True]),
        command(204, [8, 2, 4, True]),
        show_picture(4, "MAP001_Ring_Propagated", 170),
        command(250, [{"name": "Ancient_ThreeNote_Resonance", "pan": 0,
                       "pitch": 100, "volume": 80}]),
        command(230, [210]),                       # 3.4 s cue + small tail
        comment("HOOK DISTANT_ANSWER: MAP-008 owns the answering three-note montage."),
        command(230, [90]),
        command(221, []),
        command(235, [4]),
        comment("HOOK PRO-SC-012 CONTINUE: MAP-007/MAP-008 montage integration."),
        comment("SW-0112 and story stage 2001 are deliberately deferred."),
        command(123, ["A", 0]),                    # local proof replay guard
    ]


def convert_collision(data: list[int], width: int, height: int) -> list[int]:
    area = width * height
    if len(data) != area * 6:
        raise ValueError(f"Unexpected map data length {len(data)}; expected {area * 6}")
    output = [0] * (area * 6)
    for index, tile in enumerate(data[:area]):
        # The accepted floor placeholder is the only passable foundation.
        output[index] = 1537 if tile == 1559 else 1536
    return output


def main() -> None:
    source_bytes = SOURCE_MAP.read_bytes()
    source = json.loads(source_bytes)
    candidate = copy.deepcopy(source)
    candidate["tilesetId"] = 7
    candidate["parallaxName"] = "!MAP001_WatcherStation_Base"  # MZ map-aligned zero parallax
    candidate["parallaxShow"] = True
    candidate["data"] = convert_collision(source["data"], source["width"], source["height"])

    events = candidate["events"]
    events[1]["pages"] = [
        empty_page(trigger=3, commands=opening_commands()),
        empty_page(switch=101),
    ]
    events[2]["pages"] = [
        empty_page(trigger=3, variable=(1, 1012), commands=omen_commands()),
        empty_page(self_switch="A"),
        empty_page(switch=112),
    ]
    # Registration/presentation/camera anchors remain inert and retain IDs/coordinates.
    for event_id in (3, 4, 5, 6):
        events[event_id]["pages"] = [empty_page()]

    output_bytes = (json.dumps(candidate, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    OUTPUT_MAP.write_bytes(output_bytes)
    results = {
        "status": "PASS",
        "source_map": str(SOURCE_MAP.relative_to(REPO)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "output_map": str(OUTPUT_MAP.relative_to(REPO)),
        "output_sha256": hashlib.sha256(output_bytes).hexdigest(),
        "width": candidate["width"], "height": candidate["height"],
        "tileset_id": candidate["tilesetId"],
        "parallax": candidate["parallaxName"],
        "preserved_anchor_ids": [1, 2, 3, 4, 5, 6],
    }
    RESULTS.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
