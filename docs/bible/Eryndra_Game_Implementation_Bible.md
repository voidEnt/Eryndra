# Eryndra Game Implementation Bible

**Version:** 0.3  
**Status:** Living document  
**Role:** Authoritative implementation reference for translating locked story canon into RPG Maker MZ data and project structure.

---

# Section 0 — Master Implementation Index

The compact cross-project registry lives in `Master_Implementation_Index.md` and links story scenes, actors, maps, switches, variables, events, assets, battles, and implementation status.

Supporting implementation references currently include:

- `ID_Allocation_Plan.md`
- `Prologue_MZ_ID_Assignments.md`
- `../design/Prologue_Implementation_Decomposition.md`
- `../design/Map_Work_Order_Standard.md`

---

# Section 1 — Project Governance & Technical Standards

## 1.1 Source-of-Truth Hierarchy

1. **Story canon** — locked narrative source material.
2. **Implementation Bible** — implementation canon.
3. **RPG Maker MZ project** — current executable state.

Conflicts between layers must be reviewed and resolved explicitly.

## 1.2 Production Priority

- **CORE** — required for the main story spine.
- **SUPPORT** — required for CORE content to function correctly.
- **DEFERRED** — optional material postponed until the story spine works.

`DEFERRED` is deliberately flexible. Deferred content may be added, removed, renamed, reorganized, or promoted later. Once an individual entry has entered an implemented build, its numeric ID follows the normal stability/retirement rules even if its priority later changes.

## 1.3 Implementation Status

`Concept → Defined → Assigned → Implemented → Tested → Locked`

These statuses describe the implementation object, not a single worker's completion claim. An object may move backward when Validation identifies a problem requiring upstream revision.

## 1.4 Story Scope Codes

- `PRO` — Prologue
- `A1` — Act I
- `A2` — Act II
- `A3` — Act III
- `A4` — Act IV
- `A5` — Act V
- `EPI` — Epilogue
- `SYS` — system-wide content
- `DBG` — debug/development content
- `DEF` — deferred/optional content where useful

## 1.5 Bible ID Conventions

| Category | Format | Example |
|---|---|---|
| Story Scene | `PRO-SC-###`, `A1-SC-###` | `PRO-SC-001` |
| Actor | `ACT-###` | `ACT-001` |
| NPC | `NPC-###` | `NPC-014` |
| Faction | `FAC-###` | `FAC-003` |
| Map | `MAP-###` | `MAP-012` |
| Map Event | `MAP-###-EV-###` | `MAP-012-EV-006` |
| Switch | `SW-####` | `SW-0100` |
| Variable | `VR-####` | `VR-0001` |
| Common Event | `CE-###` | `CE-008` |
| Class | `CLS-###` | `CLS-001` |
| Skill | `SKL-###` | `SKL-012` |
| State | `STA-###` | `STA-006` |
| Item | `ITM-###` | `ITM-027` |
| Weapon | `WPN-###` | `WPN-014` |
| Armor | `ARM-###` | `ARM-022` |
| Enemy | `EN-###` | `EN-018` |
| Troop | `TRP-###` | `TRP-009` |
| Tileset | `TIL-###` | `TIL-004` |
| Animation | `ANI-###` | `ANI-021` |
| Quest | `QST-###` | `QST-001` |
| Picture/CG | `PIC-###` | `PIC-006` |
| Music | `BGM-###` | `BGM-004` |
| Ambient Audio | `BGS-###` | `BGS-002` |
| Sound Effect | `SE-###` | `SE-014` |

### Direct-ID alignment

When a Bible object has a direct one-to-one RPG Maker MZ numeric ID, the Bible numeric suffix should match the MZ ID whenever practical.

Examples:

- `ACT-001` = Actor 1
- `MAP-001` = `Map001.json`
- `SW-0100` = Switch 100
- `VR-0001` = Variable 1

Story scenes and named NPC identities remain independent logical IDs where no global MZ data ID exists.

## 1.6 RPG Maker Database Naming

RPG Maker database names should remain human-readable. Bible codes are tracked in the Bible rather than embedded everywhere in player-facing database names.

Examples:

- Actor database name: `Marek`
- Enemy database name: `Ash Wolf`
- Map database name: `Brackenford`

Switches and variables include readable scope prefixes because they appear in large lists:

- `PRO_Contact_Complete`
- `A1_Council_Meeting_Complete`
- `SYS_StoryStage`

## 1.7 Asset Filename Convention

Use:

`Category_CharacterOrLocation_Description_Variant.ext`

Examples:

- `Face_Marek_Default.png`
- `Face_Marek_Wounded.png`
- `Char_Marek_Travel.png`
- `SV_Marek_Default.png`
- `Enemy_AshWolf.png`
- `CG_Prologue_Vision01.png`
- `Tile_Brackenford_Exterior_A.png`
- `BGM_MarekTheme.ogg`

Rules:

- No spaces.
- Use underscores between concepts.
- Avoid runtime asset version numbers unless technically required.
- Do not rename referenced runtime assets casually after implementation.

## 1.8 Map Naming

Maps should describe the physical location directly.

Examples:

- `Brackenford`
- `Brackenford - Venn Home`
- `Brackenford - Survey Office`
- `Old Place - Exterior`
- `Old Place - Interior`

## 1.9 Event Naming

Name events by purpose rather than visual appearance.

Preferred:

- `EV_Story_MarekArrival`
- `EV_Transfer_SurveyOffice`
- `EV_NPC_Joren`
- `EV_Controller_Contact`
- `DEC_Fireplace`

Avoid generic names such as `Event001`, `Guy`, or `Thing` except for temporary experiments.

## 1.10 Switch and Self-Switch Policy

Use global switches only when state must be known outside the local event/map.

Prefer Self Switches A-D for local persistent states such as:

- chest opened
- one-time local dialogue complete
- local lever activated
- local door permanently opened

## 1.11 ID Stability Rule

**Once an ID has entered an implemented build, never reuse it for a different object.**

Before implementation, an Assigned entry may still be corrected if architecture requires it. After implementation, deleted IDs become retired rather than recycled. Renaming or reprioritizing an object does not change its implemented ID.

## 1.12 Reserved ID Ranges

The active allocation policy is defined in `ID_Allocation_Plan.md`.

Current major reservations include:

- Prologue Maps: 001-049
- Prologue Switches: 0100-0299
- Prologue Variables: 0050-0099
- Prologue Common Events: 020-039
- Prologue Items: 100-149
- Prologue Enemies/Troops: 001-024

System, Acts I-V, Epilogue, Debug, Deferred, and unallocated reserve ranges are explicitly defined in that file.

The first concrete Prologue assignments are recorded in `Prologue_MZ_ID_Assignments.md`.

## 1.13 Versioning and Change Control

Meaningful structural changes must be recorded in `CHANGELOG.md`.

Changes that affect dependencies should record affected IDs, especially actor, map, switch, variable, item/equipment, common-event, and scene IDs.

Blueprints and work orders are living implementation documents until their associated object is Locked. If a work order changes after downstream work has begun, affected downstream work must be revalidated.

## 1.13A Immutable Source and Reference Packages

Supplied story archives and reference-project archives are immutable inputs. Workers may inspect them read-only, including extraction to temporary scratch storage, but must never rewrite an archive or use an extracted reference project as an editable Eryndra test fixture.

`EryndraStory.zip` remains narrative-source material. `SampleGenerated.zip` remains technical and visual reference only. Eryndra maps, databases, assets and tests must live in Eryndra-owned repository paths or in newly created Eryndra review projects. Copying or replacing files inside a SampleGenerated project tree for testing is prohibited.

## 1.14 Plugin and Custom-Code Policy

Default to stock RPG Maker MZ behavior unless a plugin or custom JavaScript solves a demonstrated need.

Every plugin must record purpose, version, source, license, dependencies, configuration notes, and affected systems.

Custom JavaScript should remain narrow, documented, and avoid replacing stock systems unnecessarily.

## 1.15 Canonical Production Workflow

The standard implementation chain is:

**Blueprint / Work Order → Mapping → Eventwright → Validation**

The first three worker stages are commonly referred to as:

**Mapping → Eventwright → Validation**

The Blueprint/Work Order is the controlling recipe supplied to the Mapping stage. Each stage may require multiple passes. Advancement is based on acceptance criteria, not simply on the fact that a pass was attempted.

### A. Blueprint / Work Order

Before implementation, the relevant Bible categories, story scenes, locked story source, IDs, assets, state dependencies, and acceptance criteria are assembled into a task-specific work order.

The work order exists to reduce interpretation by downstream workers. It must state what is required, what is forbidden, what is still flexible, and what must be checked against story canon.

For maps, the active standard is `../design/Map_Work_Order_Standard.md`.

### B. Mapping

The Mapper builds the physical stage required by the work order.

Mapper responsibility includes:

- map dimensions and usable footprint
- terrain, walls, floors, architecture, and environmental geometry
- passability and collision
- required sightlines and staging space
- transfers/spawn positions when specified
- region placement when specified
- named event anchors/stubs required by downstream work
- spatial support for required alternate states
- compliance with the Narrative Style Gate

The Mapper does **not** independently invent story beats, dialogue, quests, enemies, rewards, global state logic, or canon changes.

Typical Mapping passes may include:

1. **Blocking/Skeleton Pass** — size, zones, routes, focal points, and required anchors.
2. **Spatial Refinement Pass** — architecture, terrain, composition, passability, and staging quality.
3. **Mapper Compliance Pass** — self-check against work order, Bible, and locked story before handoff.

A map may remain visually rough while the CORE skeleton is being established. Decorative polish must not delay a functional story spine.

### C. Eventwright

The Eventwright converts the mapped stage and its anchors into executable RPG Maker story/system behavior.

Eventwright responsibility includes:

- event pages and triggers
- dialogue commands
- movement routes
- switches, variables, and self switches
- Common Event calls
- transfers and scene transitions
- cinematics and timing
- audio/visual presentation commands
- story gating
- battle calls where specified
- resulting state changes required by the work order

The Eventwright must use the supplied map and registered IDs rather than silently redesigning the map or allocating unapproved global state.

Typical Eventwright passes may include:

1. **Functional Spine Pass** — the scene can run from required entry state to required exit state.
2. **Narrative/Presentation Pass** — dialogue, movement, timing, cinematics, and cues match the intended scene.
3. **State/Edge-Case Pass** — event pages, gating, repeat interactions, save/load behavior, and local/global state are cleaned up before Validation.

If the map cannot support the required event logic, the issue is returned to Mapping rather than hidden through increasingly fragile event code.

### D. Validation

Validation is an independent acceptance stage, not merely a final polish pass.

Validation compares the implemented result against:

1. the locked story source
2. the Implementation Bible
3. the applicable blueprint/work order
4. registered IDs and state rules
5. upstream/downstream scene dependencies
6. executable RPG Maker behavior

Typical Validation passes may include:

1. **Technical Validation** — JSON/project integrity, transfers, passability, triggers, switches, variables, save/load, and absence of soft locks.
2. **Narrative Validation** — scene beats, character presence, information timing, tone, canon secrecy, and story order.
3. **Integration Validation** — entry from the preceding scene and clean handoff to the following scene, including regression checks when appropriate.

Validation does not casually rewrite upstream work. A failed requirement is returned to the responsible stage with a specific correction request.

### E. Rework Loop

The workflow is intentionally iterative:

`Mapping ↔ Eventwright → Validation`

Validation may return work to Eventwright or Mapping. Eventwright may return work to Mapping when the stage cannot physically support the required logic. Material changes to the blueprint may require both stages to be revisited.

A later pass is not presumed to be cosmetic. Any pass may correct structural problems discovered after implementation begins.

### F. Stage Ownership Rule

Each stage owns its domain:

- **Mapping owns space.**
- **Eventwright owns executable scene logic.**
- **Validation owns acceptance.**
- **The Bible/work order owns requirements.**
- **The locked story owns narrative canon.**

Downstream workers should not solve upstream specification problems by inventing new design without recording the change in the Bible/work order.

---

# Section 2 — Story & Narrative Implementation

Contains Prologue/Acts/Epilogue structure, scene order, scene implementation registry, mandatory beats, dialogue, choices, cinematics, main quest spine, quest-state logic, world-state changes, lore delivery, and deferred narrative content.

Primary question: **What happens, in what order, and what game state changes when it happens?**

The current Prologue spine is defined in `../design/Prologue_Implementation_Decomposition.md` as twelve implementation scenes `PRO-SC-001` through `PRO-SC-012`.

---

# Section 3 — Characters, Actors & Factions

Contains playable actors, temporary/guest actors, NPCs, classes, progression, equipment restrictions, recruitment conditions, visual states, factions, and political relationships.

Primary question: **Who exists, what can they do, and what state are they in?**

---

# Section 4 — World, Maps & Exploration

Contains regions, geography, map registry/hierarchy, map availability, tilesets, transfers, local events, travel/access rules, dungeons, towns, puzzles, treasure, environmental storytelling, and physical world-state changes.

Primary question: **Where is the player, what can they interact with, and where can they go?**

Maps are implemented through mapper work orders and advance through the Mapping stage before executable scene logic is added by Eventwright.

---

# Section 5 — Combat & Progression Systems

Contains battle rules, party rules, enemies, troops, bosses, encounters, skills, states, elements, experience, levels, stat progression, defeat/escape behavior, and balancing targets.

Primary question: **How does the RPG play when combat starts?**

The locked Prologue currently requires no CORE combat.

---

# Section 6 — Items, Equipment & Economy

Contains consumables, key items, quest items, weapons, armor, accessories, relics, shops, vendors, currency, prices, loot, rewards, and equipment progression.

Primary question: **What does the player acquire, equip, spend, consume, or carry?**

---

# Section 7 — Game State, Events & Logic

Contains global switches, variables, self-switch conventions, Common Events, event-state rules, story progression state, reusable variables, system flags, dependencies, and cross-reference registry.

Primary question: **What logic makes the story and systems behave correctly?**

`VR-0001 / SYS_StoryStage` is the primary linear story-spine variable. Persistent switches record facts that must remain independently queryable.

Event implementation belongs to the Eventwright stage and must follow approved IDs, state rules, scene specifications, and work orders.

---

# Section 8 — Presentation & Assets

Contains character sprites, faces, battlers, tilesets, pictures, story illustrations, UI graphics, animations, effects, music, ambient audio, sound effects, dialogue presentation, menus, and licensing/source tracking.

Primary question: **How does the player see and hear the game?**

Placeholder assets may be used during skeleton passes when permitted by the work order. Final asset quality is not allowed to block proof of the CORE story spine unless presentation itself is required to test the scene correctly.

---

# Section 9 — Production, Testing & Release

Contains asset/ID registries, implementation status, debug systems, development maps, continuity/event/transfer/combat/save/regression testing, sequence-breaking and soft-lock tests, packaging, credits/licensing, and deferred-content tracking.

Primary question: **How do we know the game is correct, reproducible, and ready to ship?**

## 9.1 Stage-Gated Production

Implementation progresses through Mapping, Eventwright, and Validation rather than through a single monolithic build step.

Each stage may have multiple passes. A stage is complete only when its work order acceptance conditions are met sufficiently for downstream work. Early passes prioritize the structural skeleton; later passes may add refinement and presentation.

## 9.2 Validation Authority

Validation may reject an implementation even if it runs technically, including when it violates canon, reveals information too early, fails a work-order requirement, produces an incorrect map scale, misuses global state, or creates a fragile scene transition.

Corrections should be returned to the stage that owns the defect.

## 9.3 Regression Principle

When Mapping or Eventwright changes a previously validated object, affected validation checks must be repeated. Locked content may be reopened when a necessary upstream change affects it, but the change must be recorded.

---

# Immediate Production Strategy

The first full implementation target is the **Prologue vertical slice**.

The Prologue is built end-to-end before production expands into later acts. Its purpose is to establish a repeatable workflow for story decomposition, database assignment, work-order generation, Mapping, Eventwright implementation, Validation, placeholder assets, testing, JSON generation, and revision.

Optional side quests, historical books, hidden content, decorative interactions, and similar additions remain DEFERRED until the core story spine is functioning.

The current spatial production target is `MAP-003 Brackenford` Mapping Pass 01, following `docs/design/maps/MAP-003_Brackenford_Blueprint.md`. MAP-002 Mapping has PASS and Eventwright static validation passes; user observed the morning sequence functioning but found clipped dialogue, for which a corrected wrapped candidate is committed. MAP-002 final runtime acceptance, including the wrapped text, Evening, save/load and integration, remains open for later manual proof. Advancing MAP-003 spatial work does not mark MAP-002 Locked or waive its regression gate.
