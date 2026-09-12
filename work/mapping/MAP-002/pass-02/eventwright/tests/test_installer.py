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
    print("PASS: 8 installer refusal/atomicity scenarios")


if __name__=="__main__": main()
