#!/usr/bin/env python3
"""Guarded cumulative-project installer for MAP-004 Eventwright Pass 01."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


MAP003_BASELINE_SHA256 = "f96b341538c0bf33b19844a6b276b879ebbed6ebdf296c58b7424ccad568f128"
MAP003_CANDIDATE_SHA256 = "c6abe71c8de84622156c2da2ed70056e07fd589f7f16a90db1ce7763efe4326f"
MAP004_BASELINE_SHA256 = "56e6080854d7c77498db66256eb28cb44d8ad808d7b6119a29a785f8c1e5d4b4"
MAP004_CANDIDATE_SHA256 = "97141a482b0fa703e78d525843bc81d4ba742aa260970ac60502d894d46190ea"

EXPECTED_NAMES = {
    "switches": {103: "PRO_Survey_Assignment_Received", 110: "PRO_Report_Complete"},
    "variables": {1: "SYS_StoryStage"},
}
EXPECTED_MAP004_REGISTRATION_NAMES = {
    "",
    "MAP004",
    "Brackenford - Survey Office",
}


class Refusal(RuntimeError):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refuse_reference_target(target: Path) -> None:
    resolved = str(target.resolve()).lower().replace("\\", "/")
    forbidden = ("samplegenerated", "eryndrastory.zip", "samplegenerated.zip",
                 "/project_sources/", "/archive/")
    if target.suffix.lower() == ".zip" or any(term in resolved for term in forbidden):
        raise Refusal("target is an immutable source/reference package or archive")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Refusal(f"invalid or unreadable JSON: {path}") from exc


def preflight(target: Path, candidate_dir: Path) -> dict:
    refuse_reference_target(target)
    if not target.is_dir() or not any(target.glob("*.rmmzproject")):
        raise Refusal("target is not an RPG Maker MZ project directory")

    paths = {
        "map003": target / "data" / "Map003.json",
        "map004": target / "data" / "Map004.json",
        "mapinfos": target / "data" / "MapInfos.json",
        "system": target / "data" / "System.json",
        "runtime": target / "js" / "rmmz_core.js",
        "candidate003": candidate_dir / "Map003_EVENT2_PATCH_CANDIDATE.json",
        "candidate004": candidate_dir / "Map004.json",
    }
    required = ["map003", "mapinfos", "system", "runtime", "candidate003", "candidate004"]
    missing = [str(paths[key]) for key in required if not paths[key].is_file()]
    if missing:
        raise Refusal("missing required files: " + ", ".join(missing))

    if digest(paths["map003"]) not in {MAP003_BASELINE_SHA256, MAP003_CANDIDATE_SHA256}:
        raise Refusal("Map003.json is neither accepted Pass 02 nor this installed patch")
    if paths["map004"].exists() and digest(paths["map004"]) not in {
            MAP004_BASELINE_SHA256, MAP004_CANDIDATE_SHA256}:
        raise Refusal("Map004.json is neither accepted Mapping Pass 03 nor this candidate")
    if digest(paths["candidate003"]) != MAP003_CANDIDATE_SHA256:
        raise Refusal("MAP-003 integration candidate checksum mismatch")
    if digest(paths["candidate004"]) != MAP004_CANDIDATE_SHA256:
        raise Refusal("MAP-004 candidate checksum mismatch")

    map003 = load_json(paths["map003"])
    candidate003 = load_json(paths["candidate003"])
    candidate004 = load_json(paths["candidate004"])
    infos = load_json(paths["mapinfos"])
    system = load_json(paths["system"])
    if len(map003.get("events", [])) <= 2 or len(candidate003.get("events", [])) <= 2:
        raise Refusal("MAP-003 event table is incompatible")
    if candidate004.get("width") != 25 or candidate004.get("height") != 19:
        raise Refusal("MAP-004 candidate dimensions are incompatible")
    if not isinstance(infos, list):
        raise Refusal("MapInfos.json is incompatible")

    # Map ID 4 is reserved for Eryndra's survey office.  An absent/null entry,
    # a blank registration, the Mapping-stage name, or the final display name
    # are the only states this installer may claim.  Refuse before constructing
    # outputs if another project map already owns the slot.
    if len(infos) > 4 and infos[4] is not None:
        registration = infos[4]
        if not isinstance(registration, dict):
            raise Refusal("MapInfos.json ID 4 registration is incompatible")
        if registration and registration.get("id") != 4:
            raise Refusal("MapInfos.json ID 4 registration has a conflicting id")
        name = registration.get("name", "")
        if name not in EXPECTED_MAP004_REGISTRATION_NAMES:
            raise Refusal(
                f"MapInfos.json ID 4 is already registered as {name!r}; "
                "expected an Eryndra MAP-004 registration or blank"
            )

    for table, assignments in EXPECTED_NAMES.items():
        values = system.get(table)
        if not isinstance(values, list):
            raise Refusal(f"System.json has no {table} table")
        for idx, expected in assignments.items():
            if len(values) <= idx:
                raise Refusal(f"System.json {table} table is too short for ID {idx}")
            if values[idx] not in ("", expected):
                raise Refusal(
                    f"System.json {table} ID {idx} is already named {values[idx]!r}; "
                    f"expected {expected!r} or blank"
                )

    for rel in ("img/characters/People1.png",):
        if not (target / rel).is_file():
            raise Refusal(f"missing stock placeholder asset: {rel}")

    return {"paths": paths, "map003": map003, "candidate003": candidate003,
            "candidate004": candidate004, "infos": infos, "system": system}


def prepared_outputs(check: dict) -> dict[str, bytes]:
    map003 = copy.deepcopy(check["map003"])
    map003["events"][2] = copy.deepcopy(check["candidate003"]["events"][2])

    infos = copy.deepcopy(check["infos"])
    while len(infos) <= 4:
        infos.append(None)
    prior = infos[4] if isinstance(infos[4], dict) else {}
    infos[4] = {
        "id": 4,
        "expanded": prior.get("expanded", False),
        "name": "Brackenford - Survey Office",
        "order": prior.get("order", 4),
        "parentId": 3,
        "scrollX": prior.get("scrollX", 0),
        "scrollY": prior.get("scrollY", 0),
    }

    system = copy.deepcopy(check["system"])
    for table, assignments in EXPECTED_NAMES.items():
        for idx, expected in assignments.items():
            if system[table][idx] == "":
                system[table][idx] = expected

    encode = lambda obj: json.dumps(obj, ensure_ascii=False,
                                    separators=(",", ":")).encode("utf-8")
    return {
        "Map003.json": encode(map003),
        "Map004.json": encode(check["candidate004"]),
        "MapInfos.json": encode(infos),
        "System.json": encode(system),
    }


def install(target: Path, candidate_dir: Path, dry_run: bool = False) -> Path | None:
    check = preflight(target, candidate_dir)
    outputs = prepared_outputs(check)
    paths = check["paths"]

    # A dry run performs the same construction and JSON parse checks without writes.
    for payload in outputs.values():
        json.loads(payload.decode("utf-8"))
    if dry_run:
        return None

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    backup = target / ".eryndra_backups" / f"MAP-004-eventwright-{stamp}"
    backup.mkdir(parents=True, exist_ok=False)
    destinations = {
        "Map003.json": paths["map003"], "Map004.json": paths["map004"],
        "MapInfos.json": paths["mapinfos"], "System.json": paths["system"],
    }
    existed = {name: path.exists() for name, path in destinations.items()}
    originals = {name: path.read_bytes() for name, path in destinations.items() if path.exists()}
    for name, payload in originals.items():
        (backup / name).write_bytes(payload)

    staged: list[Path] = []
    try:
        for name, destination in destinations.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(prefix=name + ".", suffix=".tmp",
                                             dir=destination.parent)
            os.close(fd)
            temp = Path(temp_name)
            temp.write_bytes(outputs[name])
            staged.append(temp)
        for temp, destination in zip(staged, destinations.values()):
            os.replace(temp, destination)
    except Exception:
        for name, destination in destinations.items():
            if existed[name]:
                destination.write_bytes(originals[name])
            elif destination.exists():
                destination.unlink()
        raise
    finally:
        for temp in staged:
            temp.unlink(missing_ok=True)
    return backup


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    candidate_dir = Path(__file__).resolve().parent
    try:
        backup = install(args.project.resolve(), candidate_dir, args.dry_run)
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    if args.dry_run:
        print("PASS: preflight and staged-output checks succeeded; no files written")
    else:
        print(f"INSTALLED: MAP-003 event 2 and MAP-004; backup: {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
