# MAP-003 Mapping Pass 02 — Independent Regression Validation

**Outcome: PASS for the Mapping skeleton at the fidelity specified in the approved work order.** Candidate `Map003.json` SHA-256 `f96b341538c0bf33b19844a6b276b879ebbed6ebdf296c58b7424ccad568f128`. Full independent audit **17/17** and targeted regression checks **8/8** pass. This retires the Mapping-owned blocker `MAP003-M01` from Pass 01.

## Defect closure and exact diff

The approved blueprint fixes event ID 7 `EV_NPC_Latch_Departure` at `(21,8)` near the northern-road departure. Pass 01 was wrong at `(12,26)`. The Pass 02 builder and emitted event are now at `(21,8)`, with identical ID, name, blank page, invisible appearance, below-character priority and `through` status. Comparing the decoded maps confirms **only** the event 7 `x/y` coordinates and the map's Pass 01-to-Pass 02 note changed. Every other event, every tile layer, all map metadata and all four camera/overall preview PNGs are unchanged. The corrected Mapper self-check now independently compares event coordinates against the approved work-order table and reports **15/15**.

## Mapping acceptance scope

- Checked the locked `PrologueStoryv0.3` P-02/P-03/P-07 and `Player1Backgroundv0.2` directly from the immutable canon ZIP against the approved Brackenford blueprint; ordinary inhabited town, morning/departure/unchanged return and non-mystical Latch staging remain consistent at skeleton fidelity. No ancient symbol, extra story beat, combat, quest, shop or reward has been added.
- Verified 45×35 nonlooping MZ data, six tile layers, exact 10 event IDs/names/coordinates, stock Outside tileset ID 2, inert pages, no unauthorized transfer or state change, no parallax or soundtrack, and stock tileset flags as read from the immutable sample archive.
- Independently tested MZ directional source-exit **and** target-entry passage from `(11,26)`, `(31,16)`, `(22,6)` through both entrance cells and `(22,4)`, all required two-tile bands, no accidental facade entrances, and sealed outer edges. Latch's moved blank anchor does not obstruct the north approach.
- Inspected the overall, home, office and northern-road review PNGs in Pass 01; Pass 02 previews are byte-identical. An isolated rebuild of Pass 02 produced byte-identical JSON and four images. Both ZIPs remained unchanged (story SHA-256 `56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611`; sample SHA-256 `b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768`).

The blank doorway art, sparse ordinary set dressing and lack of live dialogue are documented Pass 01/02 skeleton limitations, not blockers to Eventwright. The preview tile rendering is a representation, not an RPG Maker runtime screenshot. **MZ runtime loading, actual playtest, integration into the existing cumulative review project, cross-map transfers, time-of-day event logic, save/load and final art acceptance are not covered by this Mapping PASS.** They require later Eventwright/integration and runtime Validation; no new review project is requested or created here.

## Handoff

Foreman may authorize the MAP-003 Eventwright pass using this validated Mapping Pass 02 candidate. Eventwright should work from the fixed `(21,8)` Latch anchor and coordinate with authorized MAP-002/MAP-004/MAP-005 transfer dependencies; Eventwright must not alter Mapping geometry to add logic. Preserve MAP-001, MAP-002 and the immutable ZIPs. Any later map change triggers targeted regression.

Evidence: `full_independent_results.txt`, `independent_results.txt`, and `validate_independent.py` in this Validator-owned folder. Run from repository root:

```text
python3 work/mapping/MAP-003/pass-02/validation/validate_independent.py
```
