# MAP-003 — Mapping Pass 02 Correction Candidate

**Stage:** Mapper correction to independent defect `MAP003-M01` in [`pass-01/validation/VALIDATION_REPORT.md`](../pass-01/validation/VALIDATION_REPORT.md). Mapper self-check `15/15 PASS`; separate independent regression pending.

`Map003.json` is a corrected original 45×35 Outside-tileset spatial map. Its only designed change from Pass 01 is event ID 7 `EV_NPC_Latch_Departure` moved from `(12,26)` near the Venn home to the approved northern-road staging cell `(21,8)`. Builder source, generated map, four re-rendered PNG previews and the strengthened self-check are retained here; Pass 01 is unchanged for auditability.

The self-check now **parses the ten approved event IDs, names and coordinates directly from the blueprint** rather than comparing solely to the builder's own `ANCHORS` table. This catches the error class found by independent Validation. See `validation_self_results.txt` and `MAPPING_HANDOFF.md` for evidence/remaining gates.

No live transfer, dialogue, sprite/follower behavior, map registration or review-project modification is part of this pass. The sample ZIP remains read-only for stock asset previews; EryndraStory ZIP remains read-only canon. A separate Validator must approve this correction before Eventwright can integrate MAP-003; MAP-004 and MAP-005 destinations are still absent.
