#!/usr/bin/env python3
"""Refusal, preflight-before-write, success, and rollback tests for installer."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "install_into_eryndra_review.py")
installer = importlib.util.module_from_spec(spec); spec.loader.exec_module(installer)
BASE1 = Path(os.environ["ERYNDRA_MAP001_BASELINE"])
BASE2 = Path(os.environ["ERYNDRA_MAP002_BASELINE"])


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    if not root.exists(): return h.hexdigest()
    for p in sorted(q for q in root.rglob("*") if q.is_file()):
        h.update(str(p.relative_to(root)).encode()); h.update(p.read_bytes())
    return h.hexdigest()


def fixture(parent: Path, name="EryndraReview") -> Path:
    p = parent / name; (p / "data").mkdir(parents=True); (p / "js").mkdir()
    (p / "Game.rmmzproject").write_text("RPGMZ 1.0.0", encoding="utf-8")
    (p / "js/rmmz_core.js").write_text("// MZ", encoding="utf-8")
    shutil.copy2(BASE1, p / "data/Map001.json"); shutil.copy2(BASE2, p / "data/Map002.json")
    (p / "data/MapInfos.json").write_text(json.dumps([None,{"id":1},{"id":2}]), encoding="utf-8")
    for rel in ("img/characters/Actor1.png", "img/characters/People1.png",
                "img/characters/People2.png", "img/characters/Nature.png",
                "img/characters/Damage1.png", "img/faces/Actor1.png",
                "img/faces/People1.png", "img/faces/People2.png",
                "audio/se/Ancient_ThreeNote_Resonance.ogg"):
        path=p/rel; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(b"fixture")
    return p


def previous_candidate_map2() -> bytes:
    """Reconstitute the accepted pre-wrap build for an upgrade test."""
    data=json.loads((ROOT/"Map002.json").read_text(encoding="utf-8"))
    for event in data["events"]:
        if not event: continue
        for page in event["pages"]:
            commands=page["list"]; restored=[]; index=0
            while index<len(commands):
                command=commands[index]
                if command["code"]==101:
                    restored.append(command); index+=1; lines=[]
                    while index<len(commands) and commands[index]["code"]==401:
                        lines.append(commands[index]["parameters"][0]); index+=1
                    if lines: restored.append({"code":401,"indent":command["indent"],"parameters":[" ".join(lines)]})
                else: restored.append(command); index+=1
            page["list"]=restored
    result=json.dumps(data,separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(result).hexdigest()==installer.MAP002_PRE_WRAP_SHA256
    return result


def expect_refusal_unchanged(project: Path):
    before=tree_hash(project)
    try: installer.install(project, ROOT)
    except installer.Refusal: pass
    else: raise AssertionError("expected refusal")
    assert tree_hash(project)==before, "refused tree changed"


def main():
    with tempfile.TemporaryDirectory() as td:
        temp=Path(td)
        for archive_name in ("EryndraStory.zip", "SampleGenerated.zip"):
            archive=temp/archive_name; archive.write_bytes(b"immutable-fixture")
            before=archive.read_bytes()
            try: installer.install(archive,ROOT)
            except installer.Refusal: pass
            else: raise AssertionError("expected archive refusal")
            assert archive.read_bytes()==before
        sample=fixture(temp,"SampleGenerated_reference"); expect_refusal_unchanged(sample)
        bad=fixture(temp,"MissingAsset"); (bad/"img/characters/Nature.png").unlink(); expect_refusal_unchanged(bad)
        wrong=fixture(temp,"WrongBaseline"); (wrong/"data/Map002.json").write_text("{}",encoding="utf-8"); expect_refusal_unchanged(wrong)
        dry=fixture(temp,"DryRun"); before=tree_hash(dry); assert installer.install(dry,ROOT,True) is None; assert tree_hash(dry)==before
        good=fixture(temp,"Good"); backup=installer.install(good,ROOT); assert backup and backup.is_dir()
        assert (good/"data/Map001.json").read_bytes()==(ROOT/"Map001_TRANSFER_PATCH_CANDIDATE.json").read_bytes()
        assert (good/"data/Map002.json").read_bytes()==(ROOT/"Map002.json").read_bytes()
        previous=fixture(temp,"PreviouslyInstalled")
        shutil.copy2(ROOT/"Map001_TRANSFER_PATCH_CANDIDATE.json",previous/"data/Map001.json")
        (previous/"data/Map002.json").write_bytes(previous_candidate_map2())
        before=tree_hash(previous); assert installer.install(previous,ROOT,True) is None
        assert tree_hash(previous)==before
        prior_backup=installer.install(previous,ROOT); assert prior_backup and prior_backup.is_dir()
        assert (prior_backup/"Map002.json").read_bytes()==previous_candidate_map2()
        assert (previous/"data/Map002.json").read_bytes()==(ROOT/"Map002.json").read_bytes()
        mixed=fixture(temp,"MixedPair")
        shutil.copy2(ROOT/"Map001_TRANSFER_PATCH_CANDIDATE.json",mixed/"data/Map001.json")
        expect_refusal_unchanged(mixed)
        rollback=fixture(temp,"Rollback"); before1=(rollback/"data/Map001.json").read_bytes(); before2=(rollback/"data/Map002.json").read_bytes()
        real_replace=os.replace; calls=0
        def fail_second(src,dst):
            nonlocal calls; calls+=1
            if calls==2: raise OSError("injected second replacement failure")
            return real_replace(src,dst)
        try:
            with mock.patch.object(installer.os,"replace",side_effect=fail_second): installer.install(rollback,ROOT)
        except OSError: pass
        else: raise AssertionError("expected injected failure")
        assert (rollback/"data/Map001.json").read_bytes()==before1
        assert (rollback/"data/Map002.json").read_bytes()==before2
    print("PASS: 10 installer refusal/atomicity scenarios (including prior-build upgrade)")


if __name__=="__main__": main()
