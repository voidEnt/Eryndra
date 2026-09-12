#!/usr/bin/env python3
"""Guarded installer for MAP-002 Eventwright Functional Spine Pass 01."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


MAP001_BASELINE_SHA256 = "f6b6a5f5e90d4f48b3b886ee5b23a09a86fba802e4d28c3cacfbf5468d4a39f6"
MAP002_BASELINE_SHA256 = "429310b40f87053f669aca5377cd0544604d929b0e828a754d6ef966f78cdcd7"
MAP001_PRE_WRAP_SHA256 = "98fec8f89e190531e5de74b525574769b59c79c2030a9fd2ac9a906c47d623cd"
MAP002_PRE_WRAP_SHA256 = "23b0c50b6323ca8eb1fd189b20caed7c6732cde54932ea2f1526f1cd4f6ac9ad"


class Refusal(RuntimeError):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refuse_reference_target(target: Path) -> None:
    lowered = str(target.resolve()).lower().replace("\\", "/")
    forbidden = ("samplegenerated", "eryndrastory.zip", "samplegenerated.zip",
                 "/project_sources/", "/archive/")
    if any(term in lowered for term in forbidden) or target.suffix.lower() == ".zip":
        raise Refusal("target represents an immutable source/reference package or archive")


def preflight(target: Path, candidate_dir: Path) -> dict[str, Path]:
    refuse_reference_target(target)
    if not target.is_dir():
        raise Refusal("target is not a directory")
    if not any(target.glob("*.rmmzproject")):
        raise Refusal("target does not contain an RPG Maker MZ .rmmzproject file")
    required = {
        "map001": target / "data" / "Map001.json",
        "map002": target / "data" / "Map002.json",
        "mapinfos": target / "data" / "MapInfos.json",
        "runtime": target / "js" / "rmmz_core.js",
        "candidate001": candidate_dir / "Map001_TRANSFER_PATCH_CANDIDATE.json",
        "candidate002": candidate_dir / "Map002.json",
    }
    missing = [str(p) for p in required.values() if not p.is_file()]
    if missing:
        raise Refusal("missing required project/candidate files: " + ", ".join(missing))
    installed_pair=(digest(required["map001"]),digest(required["map002"]))
    allowed_pairs={
        (MAP001_BASELINE_SHA256,MAP002_BASELINE_SHA256),
        (MAP001_PRE_WRAP_SHA256,MAP002_PRE_WRAP_SHA256),
    }
    if installed_pair not in allowed_pairs:
        raise Refusal("map pair does not match an accepted pre-install or installed pre-wrap build; no files changed")
    try:
        infos = json.loads(required["mapinfos"].read_text(encoding="utf-8"))
        if len(infos) <= 2 or not infos[1] or not infos[2] or infos[1]["id"] != 1 or infos[2]["id"] != 2:
            raise ValueError
        json.loads(required["candidate001"].read_text(encoding="utf-8"))
        json.loads(required["candidate002"].read_text(encoding="utf-8"))
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        raise Refusal("map registration or candidate JSON is incompatible") from exc
    asset_options = [
        (target / "audio" / "se" / "Ancient_ThreeNote_Resonance.ogg",
         target / "audio" / "se" / "Ancient_ThreeNote_Resonance.m4a"),
    ]
    for options in asset_options:
        if not any(p.is_file() for p in options):
            raise Refusal("missing SE-001 Ancient_ThreeNote_Resonance runtime asset")
    for rel in ("img/characters/Actor1.png", "img/characters/People1.png",
                "img/characters/People2.png", "img/characters/Nature.png",
                "img/characters/Damage1.png", "img/faces/Actor1.png",
                "img/faces/People1.png", "img/faces/People2.png"):
        if not (target / rel).is_file():
            raise Refusal(f"missing required stock placeholder asset: {rel}")
    return required


def install(target: Path, candidate_dir: Path, dry_run: bool = False) -> Path | None:
    files = preflight(target, candidate_dir)
    if dry_run:
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target / ".eryndra_backups" / f"MAP-002-eventwright-{stamp}"
    backup.mkdir(parents=True, exist_ok=False)
    originals = {"Map001.json": files["map001"].read_bytes(),
                 "Map002.json": files["map002"].read_bytes()}
    for name, source in (("Map001.json", files["map001"]), ("Map002.json", files["map002"])):
        shutil.copy2(source, backup / name)
    staged = []
    try:
        for key, destination in (("candidate001", files["map001"]),
                                 ("candidate002", files["map002"])):
            fd, temp_name = tempfile.mkstemp(prefix=destination.name + ".", suffix=".tmp",
                                             dir=destination.parent)
            os.close(fd)
            temp = Path(temp_name); temp.write_bytes(files[key].read_bytes()); staged.append(temp)
        os.replace(staged[0], files["map001"])
        os.replace(staged[1], files["map002"])
    except Exception:
        files["map001"].write_bytes(originals["Map001.json"])
        files["map002"].write_bytes(originals["Map002.json"])
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
        print(f"REFUSED: {exc}", file=sys.stderr); return 2
    if args.dry_run:
        print("PASS: all preflight checks succeeded; no files written")
    else:
        print(f"INSTALLED: Map001.json and Map002.json; backup: {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
