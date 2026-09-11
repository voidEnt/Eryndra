# MAP-001 Mapping Pass 01

**MAP-001 Mapping skeleton: PASS.**

This package is the first geometry skeleton for Forgotten Watcher Station, following the approved MAP-001 blueprint. Separate Mapper and Validator roles performed construction and review. It is not a playable opening scene or a production map promotion.

## Review

- [Candidate map](Map001.json)
- [Full map tile composite](Map001_Tile_Composite.png)
- [Default camera](Camera_Default_816x624.png)
- [Alternate camera](Camera_Alternate_816x624.png)
- [Ring-state footprint diagram](Ring_State_Footprint_REVIEW_ONLY.png)
- [Dependencies, deviations and MZ editor instructions](Mapping_Dependency_Note.md)
- [Tile manifest](Tile_Dependency_Manifest.json)
- [Independent validation report](validation_report.md)
- [Machine-readable checks](validation_checks.json)

Images reconstruct the selected stock tiles offline; they are not MZ screenshots. The ring diagram is review-only and does not add ring graphics to the candidate map.

## Editor evidence

The candidate was opened successfully in a newly created blank RPG Maker MZ project. `MZ_Editor_Open_Evidence.png` confirms the 29x21 map, stock placeholder tiles, and all six named anchors. The visible character is the blank project's player-start marker; it is not a MAP-001 event. See the independent validation report and Mapping handoff record for the acceptance scope.

## Next gate

Mapping Pass 01 may advance to Eventwright planning. Production tileset registration and the listed visual dependencies remain pending, so do not copy this candidate into the production game yet.

The production index remains Assigned because this accepted skeleton has not been promoted to `game/data`. No story event commands, new global state, sample database import or finished presentation are included.

## Reproduce

With Python and Pillow installed, run `python build_candidate.py /path/to/02-SampleGenerated.zip`. The independent checker documents its invocation in `validate_candidate.py`. Keep the supplied sample archive available; its checksum is recorded in the manifest. No source tileset sheets or sample runtime files are included in this package.
