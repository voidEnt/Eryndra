# MAP-002 Eventwright Functional Spine Pass 01

**Result:** Ready for independent Validation and user-side RPG Maker MZ playtesting. Static Eventwright checks pass `39/39`; installer checks pass `8/8`.

This package turns the accepted MAP-002 Mapping Pass 01 skeleton into the executable morning (`PRO-SC-002`) and evening (`PRO-SC-011`) scene candidates. It also supplies a separately named MAP-001 candidate whose only authorized change is the post-title transfer into MAP-002.

## Runtime candidates

- `Map002.json` — integrated MAP-002 event candidate
- `Map001_TRANSFER_PATCH_CANDIDATE.json` — accepted MAP-001 plus the approved transfer hook; this is intentionally not named `Map001.json` inside the repository package

## Supporting artifacts

- `EVENT_COMMAND_MANIFEST.md`
- `PLAYTEST_INSTRUCTIONS.md`
- `DEPENDENCY_AND_DEVIATION_REPORT.md`
- `install_into_eryndra_review.py`
- `tools/build_map002_eventwright.py`
- `tools/validate_eventwright.py`
- `tests/test_installer.py`
- `validation/eventwright_results.json`
- `validation/eventwright_results.txt`
- `validation/installer_test_results.txt`
- `validation/VALIDATION_REPORT.md`

## Status boundary

This is an Eventwright handoff, not final acceptance. MAP-001 opening regression, both MAP-002 scenes, real runtime movement, camera framing, placeholder rendering, audio level and state persistence still require independent Validation and user-side MZ evidence.
