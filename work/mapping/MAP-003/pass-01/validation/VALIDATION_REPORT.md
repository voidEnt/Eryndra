# MAP-003 Mapping Pass 01 — Independent Validation

**Outcome: FAIL — return to Mapping.** Tested the `Map003.json` with SHA-256 `b6a8babbcd8790b8c1a29f64540e116c2aad48dede54092b6b9418f33964d64c`. The independent checks pass **16/17**; the single failure violates a required exact event anchor and blocks Eventwright handoff. This is not a rejection of the overall spatial concept.

## Blocking defect MAP003-M01

- **Requirement:** The approved `MAP-003_Brackenford_Blueprint.md`, section 6, assigns local event ID 7 `EV_NPC_Latch_Departure` to `(21,8)`, at the northern-road departure. This location also protects the story timing: Latch appears near the road only when Marek departs after the assignment.
- **Observed:** `Map003.json` has event ID 7 at `(12,26)`, beside the Venn-home arrival. `tools/build_map003.py` contains the same erroneous source coordinate in its `ANCHORS` table. The Mapper's `14/14` self-check compares the map against that incorrect builder table, not against the blueprint, so it cannot catch this discrepancy.
- **Owner/severity:** Mapping / blocking exact-anchor and staging defect. No Eventwright workaround or relocation outside Mapping authority is acceptable.
- **Required correction outcome:** Correct ID 7 to `(21,8)` in the Mapper source and output, preserving ID/name/inert-page behavior. Re-run Mapper checks, render previews, and submit a second Mapping pass for independent regression. Verify both ordinary walking corridors and the northern-road approach remain clear. Do not introduce Latch dialogue or follower behavior in Mapping.

## Scope and supporting evidence

I independently read the locked `PrologueStoryv0.3` P-02, P-03, P-07 and `Player1Backgroundv0.2` directly from the immutable story archive. The ordinary, intact town treatment, understated workforce imagery and omission of supernatural lore match the required skeleton style; the two-story-era presentations can reuse the same map grid. The four supplied review images were inspected: they present the overall layout and home, office and northern-road camera frames. Visual dressing is sparse and doors are placeholders; that is documented, allowed for Pass 01, and not the reason for FAIL.

The validator reads stock MZ Outside tileset ID 2 flags directly from the immutable sample archive, not from the Mapper's passability helper. Using directional exit **and** target-entry checks, all three empty arrivals, exact door hotspots, north approach and two-cell walking bands are connected. Every outer edge is impassable; the future northern transfer sits on an interior road hotspot at `(22,4)`, not an off-map step. Event pages are inert and nonblocking, with no transfers, state writes, encounters, music, or parallax. Schema keys and all tile IDs match the stock reference. An isolated rebuild reproduced the JSON and four PNGs byte for byte.

This is static and image-based Validation only. **RPG Maker MZ runtime loading, in-game appearance, transfer integration and actual player playtest have not been performed**; the cumulative review project remains untouched. `MAP-002`, `MAP-001`, and both ZIP archives were untouched; their recorded SHA-256 checks remain unchanged. The sample contributes stock tiles and flags only, not an Eryndra layout or canon.

## Next gate

Return defect MAP003-M01 to Mapping. After a corrected Mapping Pass 02, run the independent checks again against the new candidate and visually inspect renewed previews. Only then can the Foreman consider an Eventwright handoff. No new review game should be created; any eventual integration targets the existing cumulative review project after authorization and proper map registration.

See `validate_independent.py` and `independent_results.txt` for reproducible evidence. Command from repository root:

```text
python3 work/mapping/MAP-003/pass-01/validation/validate_independent.py
```
