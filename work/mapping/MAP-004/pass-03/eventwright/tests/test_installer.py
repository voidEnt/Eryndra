#!/usr/bin/env python3
"""Tests for the guarded MAP-004 cumulative-project installer."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent
ROOT = Path(__file__).resolve().parents[4]
MAP003_BASELINE = ROOT / "MAP-003" / "pass-02" / "Map003.json"
MAP004_BASELINE = ROOT / "MAP-004" / "pass-03" / "Map004.json"

spec = importlib.util.spec_from_file_location("installer", CANDIDATE / "install_into_eryndra_review.py")
installer = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(installer)


def compact(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name) / "Eryndra_Review"
        (self.project / "data").mkdir(parents=True)
        (self.project / "js").mkdir()
        (self.project / "img" / "characters").mkdir(parents=True)
        (self.project / "Game.rmmzproject").write_text("RPGMZ 1.0.0", encoding="utf-8")
        (self.project / "js" / "rmmz_core.js").write_text("runtime", encoding="utf-8")
        (self.project / "img" / "characters" / "People1.png").write_bytes(b"stock")
        shutil.copy2(MAP003_BASELINE, self.project / "data" / "Map003.json")
        shutil.copy2(MAP004_BASELINE, self.project / "data" / "Map004.json")
        infos = [None, {"id": 1, "expanded": False, "name": "MAP001", "order": 1,
                        "parentId": 0, "scrollX": 0, "scrollY": 0}]
        (self.project / "data" / "MapInfos.json").write_bytes(compact(infos))
        switches = [""] * 121
        variables = [""] * 21
        system = {"switches": switches, "variables": variables, "gameTitle": "Eryndra"}
        (self.project / "data" / "System.json").write_bytes(compact(system))

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self):
        return {p.name: p.read_bytes() for p in (self.project / "data").glob("*.json")}

    def test_dry_run_writes_nothing(self):
        before = self.snapshot()
        self.assertIsNone(installer.install(self.project, CANDIDATE, dry_run=True))
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.project / ".eryndra_backups").exists())

    def test_install_patches_and_backs_up(self):
        old003 = (self.project / "data" / "Map003.json").read_bytes()
        backup = installer.install(self.project, CANDIDATE)
        self.assertTrue(backup.is_dir())
        self.assertEqual((backup / "Map003.json").read_bytes(), old003)
        candidate003 = json.loads((CANDIDATE / "Map003_EVENT2_PATCH_CANDIDATE.json").read_text())
        installed003 = json.loads((self.project / "data" / "Map003.json").read_text())
        baseline003 = json.loads(MAP003_BASELINE.read_text())
        self.assertEqual(installed003["events"][2], candidate003["events"][2])
        self.assertEqual(installed003["data"], baseline003["data"])
        self.assertTrue(all(installed003["events"][i] == baseline003["events"][i]
                            for i in range(len(baseline003["events"])) if i != 2))

    def test_map004_and_registration_installed(self):
        installer.install(self.project, CANDIDATE)
        self.assertEqual((self.project / "data" / "Map004.json").read_bytes(),
                         (CANDIDATE / "Map004.json").read_bytes())
        infos = json.loads((self.project / "data" / "MapInfos.json").read_text())
        self.assertEqual(infos[4]["id"], 4)
        self.assertEqual(infos[4]["name"], "Brackenford - Survey Office")
        self.assertEqual(infos[4]["parentId"], 3)

    def test_blank_database_names_are_filled_only_at_assigned_ids(self):
        before = json.loads((self.project / "data" / "System.json").read_text())
        installer.install(self.project, CANDIDATE)
        after = json.loads((self.project / "data" / "System.json").read_text())
        self.assertEqual(after["switches"][103], "PRO_Survey_Assignment_Received")
        self.assertEqual(after["switches"][110], "PRO_Report_Complete")
        self.assertEqual(after["variables"][1], "SYS_StoryStage")
        for i in range(len(before["switches"])):
            if i not in (103, 110):
                self.assertEqual(after["switches"][i], before["switches"][i])

    def test_idempotent_second_install(self):
        installer.install(self.project, CANDIDATE)
        first = self.snapshot()
        installer.install(self.project, CANDIDATE)
        self.assertEqual(first, self.snapshot())

    def test_accepts_compatible_mapinfos_id4_states(self):
        infos_path = self.project / "data" / "MapInfos.json"
        base = json.loads(infos_path.read_text())
        while len(base) <= 4:
            base.append(None)
        compatible = (
            None,
            {"id": 4, "expanded": False, "name": "", "order": 4,
             "parentId": 0, "scrollX": 0, "scrollY": 0},
            {"id": 4, "expanded": False, "name": "MAP004", "order": 4,
             "parentId": 0, "scrollX": 0, "scrollY": 0},
            {"id": 4, "expanded": True, "name": "Brackenford - Survey Office",
             "order": 12, "parentId": 3, "scrollX": 8, "scrollY": 4},
        )
        for registration in compatible:
            with self.subTest(registration=registration):
                infos = list(base)
                infos[4] = registration
                infos_path.write_bytes(compact(infos))
                before = self.snapshot()
                self.assertIsNone(installer.install(self.project, CANDIDATE, dry_run=True))
                self.assertEqual(before, self.snapshot())

    def test_refuses_unrelated_mapinfos_id4_without_writes(self):
        infos_path = self.project / "data" / "MapInfos.json"
        infos = json.loads(infos_path.read_text())
        while len(infos) <= 4:
            infos.append(None)
        infos[4] = {"id": 4, "expanded": True, "name": "Unrelated Dungeon",
                    "order": 4, "parentId": 0, "scrollX": 3, "scrollY": 7}
        infos_path.write_bytes(compact(infos))
        before = self.snapshot()
        with self.assertRaises(installer.Refusal):
            installer.install(self.project, CANDIDATE)
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.project / ".eryndra_backups").exists())

    def test_refuses_conflicting_database_name_without_writes(self):
        system_path = self.project / "data" / "System.json"
        system = json.loads(system_path.read_text())
        system["switches"][103] = "OTHER_SYSTEM_FLAG"
        system_path.write_bytes(compact(system))
        before = self.snapshot()
        with self.assertRaises(installer.Refusal):
            installer.install(self.project, CANDIDATE)
        self.assertEqual(before, self.snapshot())

    def test_refuses_unaccepted_map003_without_writes(self):
        path = self.project / "data" / "Map003.json"
        data = json.loads(path.read_text())
        data["width"] = 44
        path.write_bytes(compact(data))
        before = self.snapshot()
        with self.assertRaises(installer.Refusal):
            installer.install(self.project, CANDIDATE)
        self.assertEqual(before, self.snapshot())

    def test_refuses_reference_named_target(self):
        renamed = Path(self.temp.name) / "SampleGenerated"
        self.project.rename(renamed)
        with self.assertRaises(installer.Refusal):
            installer.install(renamed, CANDIDATE, dry_run=True)

    def test_preserves_unrelated_mapinfos_and_system_fields(self):
        infos_path = self.project / "data" / "MapInfos.json"
        infos = json.loads(infos_path.read_text())
        infos.append({"id": 2, "expanded": True, "name": "Venn Home", "order": 77,
                      "parentId": 3, "scrollX": 42, "scrollY": 9})
        infos_path.write_bytes(compact(infos))
        installer.install(self.project, CANDIDATE)
        after_infos = json.loads(infos_path.read_text())
        self.assertEqual(after_infos[2], infos[2])
        system = json.loads((self.project / "data" / "System.json").read_text())
        self.assertEqual(system["gameTitle"], "Eryndra")


if __name__ == "__main__":
    unittest.main(verbosity=2)
