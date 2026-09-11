# Eryndra Implementation Bible Changelog

This changelog records meaningful structural and implementation-reference changes to the living Bible.

---

## 2026-09-11 — MAP-001 Foreman preflight

- Compared the existing blueprint with supplied PrologueStoryv0.3 PDF pages 2 and 5 and sample MZ configuration.
- Approved Mapping skeleton pass 01 only; no map or executable-scene validation claimed.
- Added a controlling preflight addendum to the MAP-001 blueprint: zero-based coordinates, exact six stub IDs/positions, ring footprint, two camera frames, no-op stub behavior, and hidden-player responsibility.
- Authorized sample tileset 4 only in an isolated review fixture, with tile/flag manifest required; no production TIL-004 assignment or sample database import.
- Recorded pending production asset/tileset registration, MAP-002 transfer coordinates and actual MZ-open evidence as later gate dependencies.
- Affected IDs: MAP-001, MAP-001-EV-001 through MAP-001-EV-006; no global state allocations or story changes.

---

## v0.4 — 2026-09-11

### Added
- Canonical stage-gated production workflow: **Blueprint / Work Order → Mapping → Eventwright → Validation**.
- Short-form implementation chain: **Mapping → Eventwright → Validation**.
- Multiple-pass policy for every implementation stage rather than one-shot handoffs.
- Mapping pass model:
  1. Blocking/Skeleton
  2. Spatial Refinement
  3. Mapper Compliance
- Eventwright pass model:
  1. Functional Spine
  2. Narrative/Presentation
  3. State/Edge-Case
- Validation pass model:
  1. Technical Validation
  2. Narrative Validation
  3. Integration Validation
- Rework loop allowing Validation to return defects to Eventwright or Mapping and allowing Eventwright to return spatial constraints to Mapping.
- Stage ownership rules:
  - Mapping owns space.
  - Eventwright owns executable scene logic.
  - Validation owns acceptance.
  - Bible/work orders own implementation requirements.
  - Locked story owns narrative canon.
- Regression rule requiring affected validation checks to be rerun when previously validated Mapping or Eventwright work changes.
- Work-order change rule requiring downstream work to be revalidated when controlling blueprints change.

### Changed
- Main Implementation Bible advanced to v0.3.
- Production strategy now explicitly prioritizes skeleton passes before decorative polish.
- `MAP-001` is treated first as a Mapping-stage skeleton produced from its mapper blueprint; event logic follows only after Mapping handoff.

### Current Next Step
- Execute the first Mapping pass for `MAP-001 / Map001.json` using the approved Forgotten Watcher Station blueprint, then hand the accepted spatial skeleton to Eventwright.

---

## v0.3 — 2026-09-10

### Added
- `docs/bible/ID_Allocation_Plan.md` defining stable RPG Maker MZ numeric ranges for Maps, Switches, Variables, Common Events, Items, Enemies, and Troops.
- `docs/bible/Prologue_MZ_ID_Assignments.md` containing the first concrete bridge from Bible entries to MZ data IDs.
- Direct-ID alignment rule: where practical, Bible numeric suffixes match RPG Maker MZ IDs.
- Explicit Deferred-content policy: Deferred is a flexible holding pool and may be reorganized until individual entries enter an implemented build.
- Priority-change rule: implemented content may be promoted or demoted between DEFERRED/SUPPORT/CORE without changing its numeric ID.
- `VR-0001 / SYS_StoryStage` value families and Prologue values 1001-1012, with Act I handoff at 2001.

### Assigned
- `ACT-001` Marek Venn -> MZ Actor 1.
- `MAP-001` through `MAP-008` -> `Map001.json` through `Map008.json`.
- `SW-0100` through `SW-0112` -> MZ Switches 100-112 for the Prologue story-state facts.
- `VR-0001` -> MZ Variable 1 (`SYS_StoryStage`).

### Changed
- Master Implementation Index advanced to v0.3 and synchronized with the concrete Prologue MZ assignments and reserved ranges.
- Main Bible advanced to v0.2 with active allocation policy, Deferred-content policy, direct-ID alignment, and current implementation references.

### Current Next Step
- Design and implement `MAP-001 / Map001.json` for `PRO-SC-001 The Forgotten Place`, including New Game initialization, cinematic event control, placeholder presentation assets, state changes, title reveal, and handoff to `MAP-002`.

---

## v0.2 — 2026-09-10

### Added
- Full first-pass decomposition of the locked Prologue into twelve implementation scenes (`PRO-SC-001` through `PRO-SC-012`).
- Dedicated Prologue implementation plan: `docs/design/Prologue_Implementation_Decomposition.md`.
- Initial Prologue CORE character assignments:
  - `ACT-001` Marek Venn
  - `NPC-001` Davren Venn
  - `NPC-002` Elira Venn
  - `NPC-003` Nessa Venn
  - `NPC-004` Latch
  - `NPC-005` Joren Pell
  - `NPC-006` Edrin Holt
  - `NPC-007` Cael Veyran
- Initial Prologue CORE map assignments `MAP-001` through `MAP-008`.
- Initial named Prologue story-state switches and proposed system-wide `SYS_StoryStage` variable concept.
- Explicit rule that the locked Prologue requires no CORE combat and no enemies/troops should be invented merely to add RPG combat.
- Vertical-slice success criteria covering sequence, map gating, transfers, character presence, dialogue/cinematics, motif continuity, canon secrecy, save/load integrity, and Act I handoff.

### Changed
- Master Implementation Index advanced to v0.2 and seeded with the Prologue scene, actor, NPC, map, state, common-event, and initial asset registries.

### Current Next Step
- Define reserved RPG Maker numeric ID ranges and then assign MZ IDs to the Prologue CORE registries before constructing the first maps/events.

---

## v0.1 — 2026-09-10

### Added
- Initial repository documentation structure.
- Source-of-truth hierarchy:
  1. locked story canon
  2. implementation Bible
  3. RPG Maker MZ executable state
- Nine top-level Bible sections.
- Naming and ID conventions for scenes, actors, NPCs, factions, maps, events, switches, variables, common events, classes, skills, states, items, weapons, armor, enemies, troops, tilesets, animations, quests, pictures, music, ambient audio, and sound effects.
- RPG Maker naming policy.
- Asset filename convention.
- Map and event naming policy.
- Global-switch versus self-switch policy.
- ID stability and retirement rule.
- Production priority classes: CORE, SUPPORT, DEFERRED.
- Implementation status lifecycle: Concept → Defined → Assigned → Implemented → Tested → Locked.
- Initial Master Implementation Index with scene, actor, NPC, map, switch, variable, common-event, item/equipment, enemy/troop, asset, and reserved-range registries.
- Prologue-first vertical-slice production strategy.

### Current Next Step
- Decompose the locked Prologue into implementation scenes and assign initial CORE entries before allocating detailed RPG Maker IDs.
