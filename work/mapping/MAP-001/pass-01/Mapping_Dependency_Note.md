# MAP-001 Mapping Pass 01 — dependency and deviation note

Baseline: `c5dda89c8eff08cdfc74c1fa9780b14322f50ff7`. Assigned fidelity: geometry skeleton only. **Candidate produced; Mapping acceptance and Eventwright handoff pending. Actual MZ editor-open: NOT RUN.**

## Inputs confirmed

Read main Bible, Production Roles and Handoff Contract, Master Implementation Index, Prologue scene decomposition and approved MAP-001 blueprint including controlling section 21. Rechecked supplied `EryndraStory/Acts/PrologueStoryv0.3.pdf`, PDF pages 2 and 5, P-01 and P-08. Fitted stone, undisturbed dust, dead roots, dull metal and wall-mounted divided ring are required; no living occupant, explanatory terminology or visible route belongs here. Opening and closing share this map.

## Produced

- `Map001.json`: 29×21, six layers, one sealed chamber. North wall x5..23/y4..7; open central floor x8..20/y8..15; thick side structure x5..7 and x21..23; sealed south foreground y16..17. Outer buffer uses a real blocked black tile, not empty cells.
- Six inert, invisible, unconditional action-button event stubs, IDs 1–6 and coordinates exactly matching the controlling work order. No actor, state change, movement, transfer or cinematic logic.
- `Map001_Tile_Composite.png`: complete 1392×1008 tile composite.
- `Camera_Default_816x624.png` and `Camera_Alternate_816x624.png`: exact specified camera crops of the tile composite. They are **offline tile reconstructions, not MZ screenshots**. No lighting/tint or ring artwork is added. They show the raw geometry, not a finished dormant cinematic.
- `Ring_State_Footprint_REVIEW_ONLY.png`: four illustrative states in the reserved wall footprint. **Review-only diagram; no runtime asset, pulse timing or lighting is implemented.** Black division retained, no letters/symbols in the ring. Labels appear only outside the review patches.
- `Tile_Dependency_Manifest.json`: every used tile ID, sample flag, sheet, count and archive checksum. Zero in empty layers is separately identified as star/skip, not a collision foundation.
- `build_candidate.py`: reproducible generator/compositor using the supplied ZIP and Pillow. Stock sheet pixels and engine wall-quarter lookup are read directly from the ZIP. No sample runtime or source sheets are added to this repository.

## Tile selection

Inspected Dungeon_A4 and Dungeon_A5 visually. Selected dark brick wall autotile kind 121 (`7856 + adjacency shape`) and A5 tile 1559 for a neutral fitted-stone floor. A5 tile 1536 supplies opaque black buffer. These are **stock stone placeholders**, not the final ancient technical-stone material. Their flags include no ladder, counter or damage floor. All wall/buffer passage bits are 15; floor passage bits are 0. Upper layers are empty/star and region layer is zero. The floor is one unobstructed rectangle. No floor tile has footprints, vegetation, loot or symbols.

Sample tileset 4 is authorized **only for the isolated review fixture**. It does not allocate Eryndra TIL-004. Production tileset assignment remains unresolved. Do not copy the sample database into production.

## Explicit outstanding dependencies / limits

| Requirement | Pass-01 disposition | Owner |
|---|---|---|
| Final stone, impossible age and unusual precision | Neutral stock stone placeholder; final fidelity unresolved | Asset / Foreman |
| Dull unfamiliar metal | No substitute prop; unresolved visual asset | Asset |
| Dead roots through fine seams | No live-vine substitute; unresolved visual asset | Asset |
| Undisturbed dust / tremor | Uncluttered floor reserved; dust texture and effect unresolved | Asset / Eventwright |
| Fractured ring / dominance | Wall reserve and four-state review diagram only; missing runtime ring explicitly tracked | Asset |
| Dark foreground / dormant reveal | Sealed south geometry; cinematic darkness and shading not implemented | Asset / Eventwright |
| Actual MZ editor-open | **NOT RUN; blocks Mapping handoff per section 21** | Validation with editor access |
| Production tileset registration | Pending; candidate must stay outside `game/data/` | Foreman |
| Hidden player/followers and input lock | Not implemented by Mapper | Eventwright |
| MAP-002 destination, three-note sound, title and transitions | Unassigned/unimplemented here; no guessed values | Foreman / Eventwright / Asset |

All four ring states fit the same five-by-four-tile wall reserve and both camera frames. This establishes accommodation only. The default camera is center (14,10), alternate (14,8), each 816×624. No map boundary is exposed in either frame. Tiny internal event markers are invisible at runtime; a hidden camera/player reference is not a placed character.

## Reproduction

Run `python build_candidate.py /absolute/path/to/02-SampleGenerated.zip` with Python and Pillow. Output files are written beside the script. This recomposes stock tile graphics directly, including A4 quarter-tile selection. It does not launch or simulate the MZ editor.

## Local MZ editor check

1. Extract the supplied sample into a **new disposable review folder**; preserve the original sample and Eryndra project.
2. In that disposable copy only, replace `data/Map001.json` with this candidate. Keep that copy's original Tilesets.json and stock sheets so fixture tileset 4 resolves. This is not a production import.
3. Open the disposable copy's `game.rmmzproject` in your licensed MZ editor. Select the map with ID 001 in the map tree; its author-facing sample name may differ, while this candidate deliberately has an empty runtime display name.
4. Verify one sealed room, correct tile appearance and six invisible stubs in the event editor. Verify map size 29×21 and tileset Dungeon, then compare north wall and floor with the supplied raw tile composite.
5. Record MZ version, result and any missing-sheet/editor errors for Validation. Editor-open alone does not validate cinematics. Do not press New Game and infer scene behavior: the sample System.json start location and party are not Eryndra's, and this pass deliberately does not alter them.

No geometry or anchor deviation from section 21 is intended. Known fidelity omissions above are explicitly allowed skeleton placeholders and must not be described as completed presentation. No Mapping PASS, Tested, Locked, editor-open or complete playable scene is claimed.
