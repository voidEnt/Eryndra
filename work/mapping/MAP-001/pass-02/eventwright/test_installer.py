#!/usr/bin/env python3
"""Isolated tests for the blank-project installer; creates no reference fixture."""

from __future__ import annotations

import json
import hashlib
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
INSTALLER = HERE / "install_into_blank_mz_project.py"
RESULTS = HERE / "installer_test_results.json"


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":")), encoding="utf-8")


def make_blank(root: Path, *, event=False) -> None:
    root.mkdir(parents=True)
    (root / "EryndraReview.rmmzproject").write_text("RPGMZ 1.0.0", encoding="utf-8")
    system = {"switches": ["", ""], "variables": ["", ""],
              "startMapId": 1, "startX": 0, "startY": 0}
    tilesets = [None]
    mapinfos = [None, {"id": 1, "expanded": False, "name": "MAP001",
                       "order": 1, "parentId": 0, "scrollX": 0, "scrollY": 0}]
    events = [None]
    if event:
        events.append({"id": 1, "name": "ExistingEvent", "x": 0, "y": 0, "pages": []})
    blank_map = {"width": 17, "height": 13, "data": [0] * (17 * 13 * 6), "events": events}
    write_json(root / "data/System.json", system)
    write_json(root / "data/Tilesets.json", tilesets)
    write_json(root / "data/MapInfos.json", mapinfos)
    write_json(root / "data/Map001.json", blank_map)


def tree_snapshot(root: Path) -> dict[str, str]:
    snapshot = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        snapshot[relative] = ("directory" if path.is_dir() else
                              hashlib.sha256(path.read_bytes()).hexdigest())
    return snapshot


def main() -> int:
    outcomes = []
    with tempfile.TemporaryDirectory(prefix="eryndra-installer-test-") as temporary:
        temp = Path(temporary)
        target = temp / "UserOwnedBlank"
        make_blank(target)
        result = subprocess.run(["python3", str(INSTALLER), str(target)],
                                capture_output=True, text=True)
        installed_map = json.loads((target / "data/Map001.json").read_text())
        system = json.loads((target / "data/System.json").read_text())
        tilesets = json.loads((target / "data/Tilesets.json").read_text())
        assets = [
            target / "img/parallaxes/!MAP001_WatcherStation_Base.png",
            target / "img/pictures/MAP001_Ring_Pulse.png",
            target / "img/pictures/MAP001_Ring_Residual.png",
            target / "img/pictures/MAP001_Ring_Propagated.png",
            target / "img/pictures/MAP001_Dust_Tremor.png",
            target / "img/pictures/SYS_Eryndra_Title.png",
            target / "img/tilesets/Eryndra_CinematicCollision_A5.png",
            target / "audio/se/Ancient_ThreeNote_Resonance.ogg",
        ]
        backups = list((target / ".eryndra-backups").glob("MAP001-pass02-*/data/Map001.json"))
        success = (result.returncode == 0 and installed_map["tilesetId"] == 7 and
                   system["startMapId"] == 1 and system["startX"] == 14 and system["startY"] == 10 and
                   system["switches"][100] == "PRO_Started" and
                   system["switches"][101] == "PRO_WatcherStation_Awakened" and
                   system["variables"][1] == "SYS_StoryStage" and tilesets[7]["id"] == 7 and
                   all(path.is_file() for path in assets) and len(backups) == 1)
        outcomes.append({"name": "install into generated blank project", "passed": success,
                         "returncode": result.returncode, "stderr": result.stderr})

        forbidden = temp / "SampleGenerated"
        make_blank(forbidden)
        before = tree_snapshot(forbidden)
        result = subprocess.run(["python3", str(INSTALLER), str(forbidden)],
                                capture_output=True, text=True)
        outcomes.append({"name": "refuse SampleGenerated path without mutation",
                         "passed": result.returncode != 0 and
                         tree_snapshot(forbidden) == before,
                         "returncode": result.returncode, "stderr": result.stderr})

        nonblank = temp / "NonblankProject"
        make_blank(nonblank, event=True)
        before = tree_snapshot(nonblank)
        result = subprocess.run(["python3", str(INSTALLER), str(nonblank)],
                                capture_output=True, text=True)
        outcomes.append({"name": "refuse nonblank project without mutation",
                         "passed": result.returncode != 0 and
                         tree_snapshot(nonblank) == before,
                         "returncode": result.returncode, "stderr": result.stderr})

        occupied = temp / "OccupiedTilesetProject"
        make_blank(occupied)
        occupied_tilesets = [None] * 8
        occupied_tilesets[7] = {"id": 7, "name": "Already Used", "flags": [],
                                "mode": 0, "note": "", "tilesetNames": [""] * 9}
        write_json(occupied / "data/Tilesets.json", occupied_tilesets)
        before = tree_snapshot(occupied)
        result = subprocess.run(["python3", str(INSTALLER), str(occupied)],
                                capture_output=True, text=True)
        outcomes.append({"name": "refuse occupied Tileset 7 with entire tree unchanged",
                         "passed": result.returncode != 0 and tree_snapshot(occupied) == before,
                         "returncode": result.returncode, "stderr": result.stderr})

    status = "PASS" if all(item["passed"] for item in outcomes) else "FAIL"
    RESULTS.write_text(json.dumps({"status": status, "tests": outcomes}, indent=2) + "\n",
                       encoding="utf-8")
    print(f"{status}: {sum(item['passed'] for item in outcomes)}/{len(outcomes)} tests passed")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
