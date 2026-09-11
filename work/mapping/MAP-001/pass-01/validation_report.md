# MAP-001 Mapping Pass 01 — independent validation

**Outcome: static skeleton checks PASS; Mapping handoff PENDING.** The required actual MZ editor-open check is **NOT RUN**. This is not an overall Mapping PASS or permission to advance to Eventwright. The candidate is not marked Tested or Locked and must remain outside `game/data/` until acceptance and production dependency registration.

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
| MZ editor-open | NOT RUN | No actual editor session was performed. Static parsing and composites do not satisfy section 19/21 |

The compositor's selected A4 quarter-tile calculation and wall table use agree with the supplied engine implementation for the selected wall kind; this supports the offline visual review but does not replace the editor check.

## Pending gate and dependencies

| ID | Owner | Severity / stage | Required outcome and regression |
|---|---|---|---|
| VAL-MAP001-001 | Validation with MZ editor access / Foreman coordination | Blocking evidence gap for Mapping handoff | Open the candidate in a newly created blank Eryndra review project, record editor/project version and missing-asset errors, and confirm tiles/events display correctly. Keep SampleGenerated unchanged and reference-only. Compare with review composite. If map changes, rerun static checks and visual review against its new checksum |
| DEP-MAP001-001 | Foreman | Blocks production promotion | Register production tileset dependency before copying candidate to `game/data/`; if flags/ID change, rerun collision and tile-reference checks |
| DEP-MAP001-002 | Asset / Eventwright | Required before presentation acceptance | Supply ring, dust, dead roots/fine seams, unfamiliar metal and appropriate final stone/darkness. Preserve reserved footprint, deliberate black fracture, lack of recent traffic and no explanatory symbolism; recheck both frames after assets are integrated |
| DEP-MAP001-003 | Foreman / Eventwright / Asset | Required for later executable flow | Specify MAP-002 destination and three-note presentation, then implement hidden player/input control, pulse/residual/closing states and title/transfer behavior under an Eventwright work order |

No Mapping-owned geometry defect was found in this pass. The absent assets are permitted documented skeleton placeholders, not reasons to invent substitutes. The editor evidence gap is a required gate, not an asserted engine failure.

Save/load, cinematic timing, input lock, hidden-player behavior, scene-state progression and transfers are not implemented in the candidate and were not playtested. Their absence is consistent with Mapping scope and cannot be interpreted as validated gameplay.

## Reproduce static checks

Run from this folder:

```sh
python validate_candidate.py Map001.json /absolute/path/to/02-SampleGenerated.zip > validation_checks.json
```

The checker requires Python's standard library. Overall acceptance remains pending even if it exits successfully. The Mapper's dependency note gives blank-project editor inspection steps; keep both supplied reference packages unchanged.
