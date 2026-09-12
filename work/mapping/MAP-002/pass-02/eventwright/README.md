# MAP-002 Eventwright Functional Spine Pass 01

**Result:** Dialogue-wrap correction ready for user-side RPG Maker MZ retest. Static Eventwright checks pass `40/40`; installer checks pass `10/10`; independent static checks pass `63/63`. The new build is not yet runtime-accepted.

This package turns the accepted MAP-002 Mapping Pass 01 skeleton into the executable morning (`PRO-SC-002`) and evening (`PRO-SC-011`) scene candidates. It also supplies a separately named MAP-001 candidate whose only authorized change is the post-title transfer into MAP-002.

After a user playtest found clipped message text, the builder now wraps each dialogue/ambient message into at most four physical lines of at most 36 characters. The wording and beat order are unchanged. The guarded installer accepts the exact installed pre-wrap pair in the existing cumulative review project and retains atomic backups/refusal safeguards.

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
