# MAP-001 Mapping Pass 01 — independent validation

**Outcome: MAP-001 Mapping skeleton PASS.** The 31 static checks pass and supplied RPG Maker MZ editor evidence confirms that the candidate opens and displays at 29x21 with the expected tiles and six event anchors. This is acceptance of Mapping Pass 01 geometry only. The candidate is not a finished cinematic, Tested/Locked map, or production promotion; it must remain outside `game/data/` until the production tileset is registered.

## Baseline and independence

Reviewed requirements at repository baseline `c5dda89c8eff08cdfc74c1fa9780b14322f50ff7`: main Bible, normative Production Roles and Handoff Contract, Prologue ID assignments, and MAP-001 blueprint including section 21. Independently read locked `PrologueStoryv0.3.pdf`, PDF pages 2 and 5, including P-01 and P-08, from the supplied story archive.

Validator inspected the finished Mapper package without editing its map, generator, manifest, images or dependency note. This report and `validate_candidate.py` / `validation_checks.json` are Validator-owned artifacts. No upstream requirement was waived.

- Candidate `Map001.json` SHA-256: `469b92fb6218e84eea0f957ccc810b738e6114b61d926aba4a3908f5877243be`.
- Sample archive SHA-256: `b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768`.
- Source fixture: sample `Tilesets.json` entry 4; not an Eryndra tileset allocation.

## Checks and evidence

All 31 independent automated checks pass; full results are in `validation_checks.json`.

| Area | Result | Evidence and limit |
|---|---|---|
| Map structure | PASS, static | 29×21; 3,654 nonnegative integer values across six layers; region layer zero; valid shadow values |
| Event contract | PASS, static | Exactly six IDs 1–6, prescribed names and coordinates; one unconditional invisible action-button page each; through; below characters; no autonomous movement; only terminating event and route commands |
| State and presentation boundaries | PASS, static | No event state writes, dialogue, transfers or audio; empty display name, no encounters, autoplay, parallax or looping |
| Collision | PASS, static | Read flags directly from supplied sample. Reproduced MZ `checkPassage` layer order 3→0 and star-skip semantics from supplied engine; all 343 outer-buffer cells block all four directions. All 104 passable floor cells form one connected area, with no escape into buffer. No ladder, counter or damage-floor flags |
| Tile provenance | PASS | Manifest covers every used nonzero tile and exact source flags/counts; empty tile 0 is star/skip, not treated as an impassable foundation; archive checksum matches |
| Ring reserve | PASS, spatial only | x12..16/y4..7 has wall backing and no upper-layer graphics; ring anchor exactly (14,6); no actual runtime ring asset |
| Camera | PASS, static | Default bounds x6..22/y4..16; alternate x6..22/y2..14. Both inside the canvas and contain the entire ring reservation |
| Offline review images | PASS, skeleton scope | Inspected both 816×624 camera crops and four-state ring-footprint diagram. One sealed, uncluttered chamber; wall/floor contrast; no visible doorway, route, entity, loot, shrine or symbols. These are offline composites, not engine screenshots |
| Canon | PASS at allowed skeleton fidelity | Same geometry reserved for opening and closing. Ring mock-up is wall-backed, divided and lacks a doorway opening or symbols. Dead roots, dust, metal, age and finished ring dominance remain explicit assets, as section 21 permits; they are not falsely represented as complete |
| MZ editor-open | PASS, visual evidence | `MZ_Editor_Open_Evidence.png` shows the candidate open in RPG Maker MZ as map 001 at 29x21. The stock placeholder wall/floor tiles display without a visible missing-asset marker, and the left event list shows all six prescribed names. Exact MZ/editor version and an explicit error-free launch statement were not supplied; this is a documentation gap, not a Mapping geometry defect |

### Editor evidence interpretation

- The visible character graphic at the upper-left of the wall is the blank review project's player-start marker. It is not one of `Map001.json`'s six events and does not contradict the Mapper requirement that no actor or NPC be placed. Eventwright remains responsible for the final hidden-player/input-lock behavior before any runtime cinematic is accepted.
- The white outlined squares on the vertical centerline are invisible event-selection boxes. Three prescribed anchors share `(14,10)`, with the other anchors at `(14,6)`, `(14,8)` and `(14,12)`, so overlapping selections are expected in the editor.
- The plain stone rectangle and empty ring reservation are expected at skeleton fidelity. Final stone/metal character, dust, dead roots, darkness and fractured-ring artwork remain registered dependencies.
- Evidence PNG SHA-256: `cc26a77913e1dcb4fe8be797612e1d6a87af5d5412f7566e7e4feb5f89e85e97`.

The compositor's selected A4 quarter-tile calculation and wall table use agree with the supplied engine implementation for the selected wall kind; this supports the offline visual review but does not replace the editor check.

## Mapping acceptance and remaining dependencies

| ID | Owner | Severity / stage | Required outcome and regression |
|---|---|---|---|
| VAL-MAP001-001 | Validation / Foreman coordination | Nonblocking evidence metadata | Editor-open and visual display are confirmed by `MZ_Editor_Open_Evidence.png`. Record the exact RPG Maker MZ/editor version and whether any errors appeared if available. No map change or second Mapping pass is required from the supplied evidence |
| DEP-MAP001-001 | Foreman | Blocks production promotion | Register production tileset dependency before copying candidate to `game/data/`; if flags/ID change, rerun collision and tile-reference checks |
| DEP-MAP001-002 | Asset / Eventwright | Required before presentation acceptance | Supply ring, dust, dead roots/fine seams, unfamiliar metal and appropriate final stone/darkness. Preserve reserved footprint, deliberate black fracture, lack of recent traffic and no explanatory symbolism; recheck both frames after assets are integrated |
| DEP-MAP001-003 | Foreman / Eventwright / Asset | Required for later executable flow | Specify MAP-002 destination and three-note presentation, then implement hidden player/input control, pulse/residual/closing states and title/transfer behavior under an Eventwright work order |

No Mapping-owned geometry defect was found in this pass. The absent assets are permitted documented skeleton placeholders. Mapping Pass 01 may advance to the Eventwright planning/handoff stage, while the candidate remains outside production `game/data/` pending tileset registration and later presentation integration.

Save/load, cinematic timing, input lock, hidden-player behavior, scene-state progression and transfers are not implemented in the candidate and were not playtested. Their absence is consistent with Mapping scope and cannot be interpreted as validated gameplay.

## Reproduce static checks

Run from this folder:

```sh
python validate_candidate.py Map001.json /absolute/path/to/02-SampleGenerated.zip > validation_checks.json
```

The checker requires Python's standard library. Static success alone does not reproduce the editor evidence recorded above. Keep both supplied reference packages unchanged.
