#!/usr/bin/env python3
"""Static validator for MAP-001 Eventwright Pass 02."""

from __future__ import annotations

import hashlib
import json
import struct
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
MAP = HERE / "Map001.json"
SOURCE = HERE.parents[4] / "work/mapping/MAP-001/pass-01/Map001.json"
OUTPUT = HERE / "validation_results.json"

EXPECTED_EVENTS = {
    1: ("EV_Story_PrologueOpening", 14, 10),
    2: ("EV_Story_PrologueOmen", 14, 10),
    3: ("EV_Visual_FracturedRing", 14, 6),
    4: ("EV_FX_DustTremor", 14, 12),
    5: ("EV_Camera_Chamber", 14, 10),
    6: ("EV_Camera_Ring", 14, 8),
}

EXPECTED_ASSETS = {
    "MAP001_WatcherStation_Base.png": (1392, 1008, False),
    "MAP001_Ring_Pulse.png": (816, 624, True),
    "MAP001_Ring_Residual.png": (816, 624, True),
    "MAP001_Ring_Propagated.png": (816, 624, True),
    "MAP001_Dust_Tremor.png": (816, 624, True),
    "SYS_Eryndra_Title.png": (816, 624, True),
    "Eryndra_CinematicCollision_A5.png": (768, 768, True),
}


checks: list[dict] = []


def check(name: str, condition: bool, evidence: str) -> None:
    checks.append({"name": name, "status": "PASS" if condition else "FAIL", "evidence": evidence})


def commands(page: dict) -> list[dict]:
    return page["list"]


def has(commands_: list[dict], code: int, parameters=None) -> bool:
    for entry in commands_:
        if entry["code"] == code and (parameters is None or entry["parameters"] == parameters):
            return True
    return False


def comments(commands_: list[dict]) -> str:
    return "\n".join(entry["parameters"][0] for entry in commands_ if entry["code"] in (108, 408))


def locate(name: str) -> list[Path]:
    return [path for path in ASSETS.rglob(name) if path.is_file()]


def png_info(path: Path) -> tuple[int, int, bool]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("not a PNG")
    width, height, depth, color_type = struct.unpack(">IIBB", data[16:26])
    return width, height, color_type in (4, 6)


def main() -> int:
    candidate = json.loads(MAP.read_text(encoding="utf-8"))
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    check("map dimensions", (candidate["width"], candidate["height"]) == (29, 21), "29x21")
    check("registered tileset", candidate["tilesetId"] == 7, f"tilesetId={candidate['tilesetId']}")
    check("camera-tracked map parallax", candidate["parallaxName"] == "MAP001_WatcherStation_Base",
          candidate["parallaxName"])
    area = 29 * 21
    expected_collision = [1537 if tile == 1559 else 1536 for tile in source["data"][:area]]
    check("accepted collision geometry", candidate["data"][:area] == expected_collision,
          "accepted floor -> 1537; all walls/buffer -> 1536")
    check("upper tile layers clear", set(candidate["data"][area:]) <= {0}, "layers 1-5 use tile 0 only")

    events = candidate["events"]
    check("six anchors only", len(events) == 7 and events[0] is None,
          f"events array length={len(events)}")
    for event_id, expected in EXPECTED_EVENTS.items():
        event = events[event_id]
        actual = (event["name"], event["x"], event["y"])
        check(f"anchor {event_id} identity/coordinate", actual == expected, repr(actual))

    opening = events[1]["pages"]
    check("opening has autorun + switch-101 stop page", len(opening) == 2 and
          opening[0]["trigger"] == 3 and opening[1]["conditions"]["switch1Valid"] and
          opening[1]["conditions"]["switch1Id"] == 101 and opening[1]["trigger"] == 0,
          "page 1 autorun; page 2 blank on SW-0101")
    oc = commands(opening[0])
    check("opening hides player/followers", has(oc, 211, [0]) and has(oc, 216, [1]),
          "Change Transparency ON; Followers HIDE")
    check("opening state writes", has(oc, 121, [100, 100, 0]) and
          has(oc, 122, [1, 1, 0, 0, 1001]) and has(oc, 121, [101, 101, 0]) and
          has(oc, 122, [1, 1, 0, 0, 1002]),
          "SW100 ON; V1=1001; SW101 ON; V1=1002")
    picture_names = [entry["parameters"][1] for entry in oc if entry["code"] == 231]
    check("opening picture sequence", picture_names == ["MAP001_Dust_Tremor", "MAP001_Ring_Pulse",
          "MAP001_Ring_Residual", "SYS_Eryndra_Title"], repr(picture_names))
    pulse_erase_index = next((index for index, entry in enumerate(oc)
                              if entry["code"] == 235 and entry["parameters"] == [2]), -1)
    residual_show_index = next((index for index, entry in enumerate(oc)
                                if entry["code"] == 231 and
                                entry["parameters"][1] == "MAP001_Ring_Residual"), -1)
    check("dark beat before residual returns", pulse_erase_index >= 0 and
          residual_show_index > pulse_erase_index and
          any(entry["code"] == 230 and entry["parameters"] == [24]
              for entry in oc[pulse_erase_index + 1:residual_show_index]),
          "24-frame fully dark pause after pulse erase")
    title_show_index = next((index for index, entry in enumerate(oc)
                             if entry["code"] == 231 and entry["parameters"][1] == "SYS_Eryndra_Title"), -1)
    fade_out_index = max((index for index, entry in enumerate(oc[:title_show_index])
                          if entry["code"] == 221), default=-1)
    black_tint_between = any(entry["code"] == 223 and
                             entry["parameters"] == [[-255, -255, -255, 0], 0, False]
                             for entry in oc[fade_out_index + 1:title_show_index])
    check("title visible alone over black", title_show_index >= 0 and fade_out_index >= 0 and
          black_tint_between and any(entry["code"] == 222 for entry in oc[title_show_index + 1:]),
          "after Fade Out, map tint resets to full black before title placement and Fade In")
    se_names = [entry["parameters"][0]["name"] for entry in oc if entry["code"] == 250]
    check("opening three-note cue once", se_names == ["Ancient_ThreeNote_Resonance"], repr(se_names))
    check("opening transfer hook and no guessed transfer", "HOOK PRO-SC-002" in comments(oc) and
          not has(oc, 201), "explicit hook; no Transfer Player command")

    omen = events[2]["pages"]
    check("omen page gates", len(omen) == 3 and omen[0]["trigger"] == 3 and
          omen[0]["conditions"]["variableValid"] and omen[0]["conditions"]["variableId"] == 1 and
          omen[0]["conditions"]["variableValue"] == 1012 and
          omen[1]["conditions"]["selfSwitchValid"] and omen[1]["conditions"]["selfSwitchCh"] == "A" and
          omen[2]["conditions"]["switch1Valid"] and omen[2]["conditions"]["switch1Id"] == 112,
          "V1>=1012 autorun; local A stop; SW112 final stop")
    cc = commands(omen[0])
    closing_pictures = [entry["parameters"][1] for entry in cc if entry["code"] == 231]
    check("propagated ring shown", closing_pictures == ["MAP001_Ring_Propagated"], repr(closing_pictures))
    closing_se = [entry["parameters"][0]["name"] for entry in cc if entry["code"] == 250]
    check("omen three-note cue once", closing_se == ["Ancient_ThreeNote_Resonance"], repr(closing_se))
    check("omen continuation hooks", "HOOK DISTANT_ANSWER" in comments(cc) and
          "HOOK PRO-SC-012 CONTINUE" in comments(cc), "both off-map hooks present")
    forbidden_state = any(entry["code"] == 121 and entry["parameters"][0] <= 112 <= entry["parameters"][1]
                          for entry in cc)
    forbidden_2001 = any(entry["code"] == 122 and 2001 in entry["parameters"] for entry in cc)
    check("omen defers global completion", not forbidden_state and not forbidden_2001,
          "does not set SW112 or story stage 2001")
    check("omen local replay guard", has(cc, 123, ["A", 0]), "Self Switch A ON")

    all_commands = oc + cc
    forbidden_codes = {101, 401, 201, 301, 302, 126, 127, 128, 355, 356, 357}
    found_forbidden = sorted({entry["code"] for entry in all_commands if entry["code"] in forbidden_codes})
    check("no dialogue/transfer/battle/inventory/script/plugin commands", not found_forbidden,
          f"found={found_forbidden}")
    for event_id in (3, 4, 5, 6):
        check(f"anchor {event_id} remains inert", events[event_id]["pages"][0]["list"] ==
              [{"code": 0, "indent": 0, "parameters": []}], "single terminator command")

    for name, expected in EXPECTED_ASSETS.items():
        matches = locate(name)
        if len(matches) != 1:
            check(f"asset {name}", False, f"found {len(matches)} copies")
            continue
        try:
            actual = png_info(matches[0])
            dimensions_ok = actual[:2] == expected[:2]
            alpha_ok = (not expected[2]) or actual[2]
            check(f"asset {name}", dimensions_ok and alpha_ok,
                  f"dimensions={actual[:2]}, alpha_channel={actual[2]}, sha256={hashlib.sha256(matches[0].read_bytes()).hexdigest()}")
        except ValueError as exc:
            check(f"asset {name}", False, str(exc))

    audio = locate("Ancient_ThreeNote_Resonance.ogg")
    audio_evidence = "missing"
    audio_ok = len(audio) == 1
    if audio_ok:
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "default=nw=1:nk=1", str(audio[0])],
                               capture_output=True, text=True)
        audio_ok = probe.returncode == 0
        audio_evidence = f"duration={probe.stdout.strip()}s, sha256={hashlib.sha256(audio[0].read_bytes()).hexdigest()}"
    check("three-note OGG readable", audio_ok, audio_evidence)

    required_scripts = [HERE / "install_into_blank_mz_project.py", HERE / "build_eventwright_candidate.py"]
    check("required scripts present", all(path.is_file() for path in required_scripts),
          ", ".join(path.name for path in required_scripts))

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    result = {"status": status, "checks": checks, "check_count": len(checks),
              "passed": sum(item["status"] == "PASS" for item in checks),
              "failed": sum(item["status"] == "FAIL" for item in checks)}
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{status}: {result['passed']}/{result['check_count']} checks passed")
    for item in checks:
        if item["status"] == "FAIL":
            print(f"FAIL: {item['name']}: {item['evidence']}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
