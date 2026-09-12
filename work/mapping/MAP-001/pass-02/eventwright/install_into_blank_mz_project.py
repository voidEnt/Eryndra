#!/usr/bin/env python3
"""Install the MAP-001 proof build into a user-owned blank RPG Maker MZ project.

The installer refuses reference-project paths, verifies a blank one-map project,
backs up every replaced file, then installs the map, assets, tileset registration,
map registration, story-state names, and start position.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ASSET_ROOT = HERE.parent / "assets"
MAP_SOURCE = HERE / "Map001.json"

ASSETS = {
    "MAP001_WatcherStation_Base.png": ("img/parallaxes/!MAP001_WatcherStation_Base.png",),
    "MAP001_Ring_Pulse.png": ("img/pictures/MAP001_Ring_Pulse.png",),
    "MAP001_Ring_Residual.png": ("img/pictures/MAP001_Ring_Residual.png",),
    "MAP001_Ring_Propagated.png": ("img/pictures/MAP001_Ring_Propagated.png",),
    "MAP001_Dust_Tremor.png": ("img/pictures/MAP001_Dust_Tremor.png",),
    "SYS_Eryndra_Title.png": ("img/pictures/SYS_Eryndra_Title.png",),
    "Ancient_ThreeNote_Resonance.ogg": ("audio/se/Ancient_ThreeNote_Resonance.ogg",),
    "Eryndra_CinematicCollision_A5.png": ("img/tilesets/Eryndra_CinematicCollision_A5.png",),
}

SWITCH_NAMES = {
    100: "PRO_Started",
    101: "PRO_WatcherStation_Awakened",
    111: "PRO_HomeEvening_Complete",
    112: "PRO_Complete",
}


def fail(message: str) -> None:
    raise SystemExit(f"INSTALL REFUSED: {message}")


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid JSON at {path}: {exc}")


def find_asset(name: str) -> Path:
    matches = [path for path in ASSET_ROOT.rglob(name) if path.is_file()]
    if len(matches) != 1:
        fail(f"expected exactly one asset named {name} under {ASSET_ROOT}; found {len(matches)}")
    return matches[0]


def validate_target(target: Path) -> tuple[Path, dict, list, list]:
    target = target.expanduser().resolve()
    lowered = [part.lower() for part in target.parts]
    if "samplegenerated" in lowered or "project_sources" in lowered:
        fail("target is inside a reference/source tree")
    if any(part.lower().endswith(".zip") for part in target.parts):
        fail("target resolves through an archive path")
    if not target.is_dir():
        fail(f"target directory does not exist: {target}")
    project_files = list(target.glob("*.rmmzproject"))
    if len(project_files) != 1:
        fail("target must contain exactly one .rmmzproject file")

    data = target / "data"
    required = [data / "System.json", data / "Tilesets.json",
                data / "MapInfos.json", data / "Map001.json"]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        fail("target is not a complete blank MZ project; missing: " + ", ".join(missing))

    system = read_json(required[0])
    tilesets = read_json(required[1])
    mapinfos = read_json(required[2])
    current_map = read_json(required[3])

    populated_maps = [entry for entry in mapinfos if entry is not None]
    if len(populated_maps) != 1 or populated_maps[0].get("id") != 1:
        fail("target must be a blank one-map project with only Map 001 registered")
    if any(event is not None for event in current_map.get("events", [])):
        fail("target Map001 already contains events and is not blank")
    if len(current_map.get("data", [])) != current_map.get("width", 0) * current_map.get("height", 0) * 6:
        fail("target Map001 has malformed tile data")
    return target, system, tilesets, mapinfos


def backup_file(target: Path, backup_root: Path) -> None:
    if not target.exists():
        return
    relative = target.relative_to(backup_root.parent.parent)
    backup = backup_root / relative
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup)


def ensure_index(entries: list, index: int, fill="") -> None:
    while len(entries) <= index:
        entries.append(fill)


def tileset_7() -> dict:
    fragment = find_asset("Tileset007.fragment.json")
    value = read_json(fragment)
    if value.get("id") != 7 or len(value.get("flags", [])) != 8192:
        fail("Tileset007.fragment.json is malformed")
    if value["flags"][1536] != 15 or value["flags"][1537] != 0:
        fail("Tileset007.fragment.json does not implement the approved collision flags")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Path to a newly created, user-owned blank RPG Maker MZ project")
    args = parser.parse_args()

    target, system, tilesets, mapinfos = validate_target(Path(args.target))
    if not MAP_SOURCE.is_file():
        fail(f"proof map is missing: {MAP_SOURCE}")
    asset_sources = {name: find_asset(name) for name in ASSETS}

    # Complete every refusal-producing preflight before creating a backup
    # directory or changing any target path.
    approved_tileset = tileset_7()
    ensure_index(tilesets, 7, None)
    if tilesets[7] not in (None, approved_tileset):
        fail("Tileset ID 7 is already occupied")
    tilesets[7] = approved_tileset

    ensure_index(system["switches"], 112)
    for index, name in SWITCH_NAMES.items():
        current = system["switches"][index]
        if current not in ("", name):
            fail(f"switch {index} is already named {current!r}")
        system["switches"][index] = name
    ensure_index(system["variables"], 1)
    if system["variables"][1] not in ("", "SYS_StoryStage"):
        fail(f"variable 1 is already named {system['variables'][1]!r}")
    system["variables"][1] = "SYS_StoryStage"
    system["startMapId"] = 1
    system["startX"] = 14
    system["startY"] = 10

    mapinfos[1].update({"id": 1, "name": "Forgotten Watcher Station",
                        "parentId": 0, "expanded": True, "order": 1})

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = target / ".eryndra-backups" / f"MAP001-pass02-{timestamp}"
    destinations = [
        target / "data/Map001.json", target / "data/System.json",
        target / "data/Tilesets.json", target / "data/MapInfos.json",
        target / "MAP001_PASS02_INSTALL_RECEIPT.json",
    ]
    for name, relative_paths in ASSETS.items():
        for relative in relative_paths:
            destinations.append(target / relative)
    backup_root.mkdir(parents=True, exist_ok=False)
    for destination in destinations:
        backup_file(destination, backup_root)

    (target / "data/Map001.json").write_bytes(MAP_SOURCE.read_bytes())
    (target / "data/System.json").write_text(json.dumps(system, separators=(",", ":")), encoding="utf-8")
    (target / "data/Tilesets.json").write_text(json.dumps(tilesets, separators=(",", ":")), encoding="utf-8")
    (target / "data/MapInfos.json").write_text(json.dumps(mapinfos, separators=(",", ":")), encoding="utf-8")
    for name, relative_paths in ASSETS.items():
        for relative in relative_paths:
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset_sources[name], destination)

    receipt = {
        "package": "MAP-001 Pass 02 proof build",
        "backup": str(backup_root),
        "installed_map": "data/Map001.json",
        "tileset": 7,
        "start": {"mapId": 1, "x": 14, "y": 10},
        "assets": [path for paths in ASSETS.values() for path in paths],
    }
    (target / "MAP001_PASS02_INSTALL_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"Installed MAP-001 proof build into: {target}")
    print(f"Backup created at: {backup_root}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
