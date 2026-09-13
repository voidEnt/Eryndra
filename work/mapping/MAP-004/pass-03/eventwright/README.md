# MAP-004 Eventwright Functional Spine Pass 01

This directory contains the Eventwright candidate for `PRO-SC-004` (The Survey Assignment) and `PRO-SC-010` (The Report), plus the isolated MAP-003 office-door integration patch.

## Candidate files

- `Map004.json` — accepted Mapping Pass 03 geometry with authorized event pages added.
- `Map003_EVENT2_PATCH_CANDIDATE.json` — accepted MAP-003 Pass 02 with only event ID 2 changed.
- `install_into_eryndra_review.py` — guarded installer for the existing cumulative Eryndra review project.
- `tools/build_map004_eventwright.py` — deterministic candidate builder.
- `tools/validate_eventwright.py` — Eventwright self-validation; it is not independent Validation.
- `tests/test_installer.py` — installer safety/idempotence tests.
- `EVENT_COMMAND_MANIFEST.md` — exact event architecture and state/transfer effects.
- `DEPENDENCY_AND_DEVIATION_REPORT.md` — dependencies, authority notes and deviations.
- `PLAYTEST_INSTRUCTIONS.md` — downstream MZ runtime checklist.
- `validation/` — repeatable static self-check evidence.

## Current gate

Eventwright self-checks pass **31/31** and installer tests pass **11/11**. The installer refuses a conflicting MapInfos ID 4 registration before creating backups or writing project data; absent, null, blank, `MAP004`, and the exact final Eryndra registration remain compatible. Independent Eventwright Validation and user RPG Maker MZ runtime testing are **NOT RUN**. The candidate must not be described as runtime-tested or accepted until those gates occur.

The attached `EryndraStory.zip` and `SampleGenerated.zip` remain immutable references and are not installation targets or runtime dependencies.
