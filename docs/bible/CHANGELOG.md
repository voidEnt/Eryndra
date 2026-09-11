# Eryndra Implementation Bible Changelog

This changelog records meaningful structural and implementation-reference changes to the living Bible.

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
