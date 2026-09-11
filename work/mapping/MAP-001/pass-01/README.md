# MAP-001 Mapping Pass 01

**Candidate built; static checks passed; Mapping acceptance pending.**

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

## Next gate

Open the candidate in a newly created blank Eryndra review project using RPG Maker MZ, following the dependency note. Keep both supplied ZIPs and any extracted SampleGenerated reference tree unchanged. Record the editor version and any errors or visual discrepancies. Actual editor-open has not been performed here and is required by blueprint section 21 before handoff. Production tileset registration and the listed visual dependencies also remain pending; do not copy this candidate into the production game yet.

The production index remains Assigned. No story event commands, new global state, sample database import or finished presentation are included.

## Reproduce

With Python and Pillow installed, run `python build_candidate.py /path/to/02-SampleGenerated.zip`. The independent checker documents its invocation in `validate_candidate.py`. Keep the supplied sample archive available; its checksum is recorded in the manifest. No source tileset sheets or sample runtime files are included in this package.
