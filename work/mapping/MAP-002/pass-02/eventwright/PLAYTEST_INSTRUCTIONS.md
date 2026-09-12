# MAP-002 Functional Spine Playtest Instructions

Use your existing cumulative Eryndra review project. Never install into `SampleGenerated`, either ZIP, or an extracted reference tree.

## Install

Close RPG Maker MZ. From PowerShell in this package directory:

```powershell
py install_into_eryndra_review.py "C:\full\path\to\Your_Existing_Eryndra_Review" --dry-run
py install_into_eryndra_review.py "C:\full\path\to\Your_Existing_Eryndra_Review"
```

The project must already contain registered maps 1 and 2, MAP-001's `Ancient_ThreeNote_Resonance` audio, and the listed stock placeholder sheets. The installer accepts either the exact initial baselines or the exact installed pre-wrap map pair, refuses all other/reformatted pairs and reference targets, and creates recoverable backups before replacement. If the dry run refuses, stop and report its output; do not force-install or manually overwrite anything.

## Test A — MAP-001 into Morning

1. Leave your working New Game start on MAP-001 unchanged (the player cannot start on top of an event).
2. Start a New Game.
3. Confirm the already validated MAP-001 opening remains visually and audibly unchanged through the `ERYNDRA` title.
4. Confirm the title clears under black and MAP-002 appears with the household staged correctly.
5. Confirm the exact Morning dialogue fits the message window, one restrained dog sound, crooked-latch action, collision-safe kit movement and double-check motions.
6. Confirm player control begins at `(14,14)`, Marek is visible, followers remain hidden, and family action-button lines work.
7. Walk all required Mapping-stage routes again. The south MAP-003 door must not transfer yet.
8. In F8 Console, run:

```javascript
[$gameMap.mapId(), $gameSwitches.value(101), $gameSwitches.value(102), $gameVariables.value(1), $gamePlayer.isTransparent(), $gamePlayer.followers().isVisible()]
```

Expected:

```text
[2, true, true, 1003, false, false]
```

Save, load and verify the Morning autorun does not replay.

## Test B — Evening direct setup

During any map playtest, open F8 Console and run this as one statement:

```javascript
$gameSwitches.setValue(110,true);$gameSwitches.setValue(111,false);$gameVariables.setValue(1,1011);$gamePlayer.reserveTransfer(2,14,19,8,2);SceneManager.goto(Scene_Map);
```

Then confirm:

1. Marek and muddy Latch appear by the entry; Latch does not bark.
2. The exact entry and shutter dialogue plays.
3. The four distinct supper positions read clearly and the exact supper exchange plays without cropped text.
4. The scene fades to Marek's bedroom with Marek presented asleep and Latch silent at `(19,9)`, facing north.
5. The three-note cue plays exactly once, faintly; Marek changes pose without leaving the bed; there is no explanatory dialogue.
6. The screen fades fully black before transfer to MAP-001.
7. MAP-001's existing Omen controller begins. Its full later montage remains a separate integration dependency.

During the MAP-001 arrival, run:

```javascript
[$gameMap.mapId(), $gameSwitches.value(110), $gameSwitches.value(111), $gameSwitches.value(112), $gameVariables.value(1)]
```

Expected at the handoff:

```text
[1, true, true, false, 1012]
```

Repeat Test B from a fresh setup and then test a save/load after `SW111=true`; the MAP-002 Evening controller must not replay.

## Record as defects

Record any blocked movement, wrong face/sprite, skipped/repeated dialogue, wrong camera crop, audible double cue, visible transfer flash, black-tint persistence, state mismatch or autorun replay. Static PASS does not supersede runtime evidence.
