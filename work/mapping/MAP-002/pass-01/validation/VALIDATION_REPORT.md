# MAP-002 Mapping Pass 01 - Independent Validation Report

**Production unit:** `MAP-002 Brackenford - Venn Home`  
**Validated stage:** Mapping skeleton Pass 01 only  
**Outcome:** **PASS**  
**Blocking defects:** None  
**Eventwright gate:** **OPEN.** Eventwright may begin the Functional Spine pass using this accepted spatial skeleton. This Mapping-stage PASS does not constitute acceptance of later event logic or final scene integration.

**Regression result:** `MAP002-OBS-01` is **CLOSED**. Mapping removed stock tile 332, regenerated the map and affected composites, and corrected the manifest/handoff language without changing the approved geometry.

**Runtime confirmation:** `MAP002-VAL-C01` is **CLOSED**. The user confirmed that `Map002.json` opens and renders correctly in RPG Maker MZ and that the required collision routes work.

## 1. Scope and authority

This review was performed under the Validator role defined by the normative Production Roles and Handoff Contract. No Mapper-owned deliverable was altered. Validation covered the approved work order, `Map002.json`, all three review composites, the dependency manifest, Mapper handoff, deterministic builder, Mapper validator, locked Prologue sections P-02/P-07, and the Player 1 Venn-household canon.

This outcome accepts only the Mapping Pass 01 spatial substrate. It does not validate dialogue, character graphics, event commands, transfers, audio, lighting, global state, save/load behavior, or the finished `PRO-SC-002` / `PRO-SC-011` scenes.

## 2. Evidence reviewed

- Approved blueprint: `docs/design/maps/MAP-002_Brackenford_Venn_Home_Blueprint.md`
- Map candidate: `work/mapping/MAP-002/pass-01/Map002.json`
- Composites:
  - `MAP-002_full-map.png`
  - `MAP-002_common-room_816x624.png`
  - `MAP-002_marek-bedroom_816x624.png`
- Mapper documentation: `README.md`, `MAPPING_HANDOFF.md`, and `TILE_DEPENDENCY_MANIFEST.md`
- Reproduction and Mapper-stage validation scripts
- Locked `PrologueStoryv0.3`, P-02 and P-07
- Locked `Player1Backgroundv0.2`, especially "Life Before the Story" and "The Venn Household"
- Bible production workflow, role contract, Map Work Order Standard, and Prologue ID assignments

## 3. Technical findings

### Map structure - PASS

- The map is valid JSON with a `29 x 23` canvas and six MZ data planes.
- It uses stock MZ `Inside` tileset slot 3 and has no parallax, looping, encounters, autoplay, regions, shadow data, plugins, or executable Mapping-stage logic.
- All 17 required anchors exist at the exact IDs, names, and coordinates in the work order.
- Every anchor contains one unconditional Mapper-safe blank page: no graphic, no autonomous movement, Through ON, Below Characters, Action Button, and only command code 0.
- The active footprint remains inside the specified bounds and contains the three sleeping spaces, hall, open kitchen, common/supper room, repair nook, and south mud entry.
- The three bedroom thresholds are the only openings in the bedroom wall. The south aperture at `(14,20)` is the only exterior route.
- An independent directional-passage traversal using the stock tileset flags reached all required route and staging cells from `(14,14)`. The corrected connected walkable component contains 268 cells.
- The four table staging cells are walkable and connected without trapping the common-room route.

### Camera and composites - PASS at skeleton fidelity

- All composites have the required dimensions: full map `1392 x 1104`; camera reviews `816 x 624`.
- The common-room frame contains the kitchen, table, repair nook, entry approach, and required staging space.
- The Marek-room frame contains Marek's bed, the south doorway, and Latch's threshold coordinate together.
- The visible black areas are authored impassable buffer outside the house walls, not missing pixels or a crop beyond the canvas. User-side MZ confirmation closed Condition `MAP002-VAL-C01` with correct rendering and required route behavior.

### Reproducibility - PASS

Rebuilding into an isolated temporary directory reproduced byte-identical outputs:

| Deliverable | SHA-256 |
|---|---|
| `Map002.json` | `429310b40f87053f669aca5377cd0544604d929b0e828a754d6ef966f78cdcd7` |
| `MAP-002_full-map.png` | `a719cb9d2a4a643605d19dab43d37d4650636260d0065485a6cd7f0b09c1849c` |
| `MAP-002_common-room_816x624.png` | `fea0eaf00672e47176da650474ac3d4403f117ab7a9327e6200ab36fc379be33` |
| `MAP-002_marek-bedroom_816x624.png` | `f635f2bb539d92844835da2877884a745706af5f6ba780802d42f2d26aa02bdc` |

The Mapper validator was independently rerun and returned `53/53 PASS`.

## 4. Canon and Narrative Style Gate - PASS

The spatial implications match the locked sources:

- The home reads as modest, practical, inhabited, and repair-minded rather than grand, destitute, ceremonial, or scholarly.
- Shared work dominates the common level: kitchen, supper table, repair surface, ordinary storage, and entry routine all coexist visibly.
- Davren's compact repair area and Elira's open kitchen placement support family interaction rather than isolating either activity.
- Nessa receives a distinct, modest sleeping space without childish-toy characterization.
- Marek's room is simple and has a work surface plus clear floor and threshold staging.
- Latch can occupy both the entry and Marek-room threshold without implying supernatural knowledge.
- Nothing visually introduces ancient technology, fractured-ring imagery, magic, shrines, weapons, treasure, hidden rooms, a second exit, or foreknowledge of the day's importance.
- The same geometry supports both ordinary morning routine and the false return to normal at supper before the night unease.

## 5. Source/reference integrity - PASS

The supplied archives retained their approved hashes before and after the isolated rebuild:

| Immutable input | SHA-256 |
|---|---|
| `EryndraStory.zip` | `56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611` |
| `SampleGenerated.zip` | `b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768` |

Static review confirms the builder opens `SampleGenerated.zip` only in read mode for stock tileset PNGs, and the Mapper validator opens it only in read mode for `Tilesets.json`. Neither script extracts into, writes to, or treats the sample project as an editable fixture. All produced work is confined to Eryndra-owned output paths or an isolated temporary validation directory.

## 6. Conditions and observations

### `MAP002-VAL-C01` - MZ editor/runtime confirmation - CLOSED

- **Status:** CLOSED by user-side RPG Maker MZ confirmation
- **Severity:** Resolved gate condition
- **Owner:** Validation with user-side RPG Maker MZ evidence
- **Closure evidence:** On 2026-09-12, the user confirmed that the supplied `Map002.json` opens and renders correctly in RPG Maker MZ and that the required collision routes work. This satisfies the work order's MZ editor/runtime confirmation requirement for Mapping Pass 01.
- **Regression result:** PASS for map load, stock tileset rendering, visible framing, and required collision-route behavior. Anchor structure remains covered by the independent static validation above.

### `MAP002-OBS-01` - Tile 332 description mismatch - CLOSED

- **Status:** CLOSED by Mapping regression correction
- **Owner:** Mapping documentation / later visual refinement
- **Original observation:** The manifest called tile `332` an "ordinary survey map," but the stock composite read as an animal portrait or decorative wall picture.
- **Correction verified:** Tile 332 is absent from the final map and builder. The full-map and bedroom composites were regenerated. The manifest and handoff now accurately describe the neutral preparation table at `(18,6)` as the element satisfying Marek's bedroom work-surface requirement.
- **Regression result:** PASS. No required anchor, route, room, camera frame, or canon implication was lost.

## 7. Downstream conditions

Eventwright may use the accepted geometry and exact anchors, subject to these restrictions:

1. Do not alter map geometry to implement the scenes; return any spatial defect to Mapping.
2. Supply the visible/operable front-door representation and crooked-latch beat without creating a second route.
3. Preserve the ordinary, non-supernatural treatment of Latch.
4. Use the approved entry/output states exactly: morning `1002 -> 1003` with `SW-0102`; evening `1011 -> 1012` with `SW-0111`.
5. Keep the field kit and calibration weight as scene props, not inventory/database rewards.
6. Preserve the user-confirmed MZ rendering and route behavior; presentation changes introduced during Eventwright require regression validation.
7. Do not mark the completed MAP-002 scenes Implemented, Tested, or integration-ready until the later Eventwright/runtime validation passes.

## 8. Decision

**MAP-002 Mapping Pass 01 receives final PASS.** The spatial skeleton is accepted for Eventwright Functional Spine work. `MAP002-VAL-C01` and `MAP002-OBS-01` are closed, no blocking defects remain, and no further Mapping correction is required for this pass. Later Eventwright behavior and complete scene integration remain separate validation gates.
