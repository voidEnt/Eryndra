# MAP-004 Eventwright Functional Spine Pass 01 — independent Validation

**Final outcome: PASS — static Eventwright gate only.** RPG Maker MZ runtime/playtest remains **NOT RUN**.

The first independent review returned **FAIL** on one installer-safety defect: with `Map004.json` absent, a non-Eryndra `MapInfos[4]` registration could be overwritten. Event JSON itself passed 120/120 independent structural checks. Eventwright corrected only installer safeguards/tests/documentation; candidate map/event JSON did not change. The focused independent regression then passed.

## Event implementation evidence

- Exact assignment/report speaker order, wording and line breaks match the approved work order; maximum content line length is 40 characters.
- `SW-0103` precedes stage 1005; `SW-0110` precedes stage 1011; no unauthorized global writes.
- Page ordering, exact equality guards, completion pages and stage ceilings terminate autoruns and prevent replays.
- Edrin is visible at stage 1004, absent 1005–1009 and visible from 1010; Joren remains distinct; Latch is absent.
- MAP-004 geometry/tile data and eight anchor identities/coordinates are preserved. MAP-003 differs only at event ID 2.
- Transfers are exact: MAP-003 → MAP-004 `(12,15)` facing north, and MAP-004 → MAP-003 `(31,16)` facing south, both black fade.
- Deterministic rebuild matches `Map004.json` SHA-256 `97141a482b0fa703e78d525843bc81d4ba742aa260970ac60502d894d46190ea` and MAP-003 integration candidate `c6abe71c8de84622156c2da2ed70056e07fd589f7f16a90db1ce7763efe4326f`.

## Installer regression

Independent MapInfos conflict matrix: **14/14 PASS**. Unrelated strings, lists, numbers, wrong/missing IDs and unrelated/null/numeric names refuse before backup with byte-identical zero writes. Absent/null/empty/blank/`MAP004`/exact Eryndra registrations install successfully and are data-idempotent on a second install. Shipped installer suite: **11/11 PASS**; package checksum manifest: PASS.

This PASS authorizes installation into the existing cumulative Eryndra review project for user runtime validation. It does not validate in-engine character rendering, message-window fit, forced movement, event activation, actual save/load replay behavior or transfer feel. Those checks must use `PLAYTEST_INSTRUCTIONS.md`. Record any failure before proceeding to MAP-005 Eventwright work.
