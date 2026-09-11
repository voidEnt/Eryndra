# Eryndra Implementation Bible Changelog

This changelog records meaningful structural and implementation-reference changes to the living Bible.

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
