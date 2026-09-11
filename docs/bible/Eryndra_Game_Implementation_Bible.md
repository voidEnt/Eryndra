# Eryndra Game Implementation Bible

**Version:** 0.1  
**Status:** Living document  
**Role:** Authoritative implementation reference for translating locked story canon into RPG Maker MZ data and project structure.

---

# Section 0 — Master Implementation Index

The compact cross-project registry lives in `Master_Implementation_Index.md` and links story scenes, actors, maps, switches, variables, events, assets, battles, and implementation status.

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

## 1.3 Implementation Status

`Concept → Defined → Assigned → Implemented → Tested → Locked`

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
| Switch | `SW-####` | `SW-0021` |
| Variable | `VR-####` | `VR-0010` |
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

## 1.6 RPG Maker Database Naming

RPG Maker database names should remain human-readable. Bible codes are tracked in the Bible rather than embedded everywhere in player-facing database names.

Examples:

- Actor database name: `Marek`
- Enemy database name: `Ash Wolf`
- Map database name: `Eastwatch Village`

Switches and variables should include readable scope prefixes because they appear in large lists:

- `PRO_Marek_Intro_Complete`
- `A1_Council_Meeting_Complete`
- `SYS_Current_Act`
- `SYS_Current_Story_Stage`

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
- `Tile_Eastwatch_Exterior_A.png`
- `BGM_MarekTheme.ogg`

Rules:

- No spaces.
- Use underscores between concepts.
- Avoid runtime asset version numbers unless technically required.
- Do not rename referenced runtime assets casually after implementation.

## 1.8 Map Naming

Maps should describe the physical location directly.

Examples:

- `Eastwatch Village`
- `Eastwatch - Inn`
- `Eastwatch - Blacksmith`
- `Old Shrine - Entrance`
- `Old Shrine - Lower Hall`

Bible map IDs remain stable independently of displayed map names.

## 1.9 Event Naming

Name events by purpose rather than visual appearance.

Preferred:

- `EV_Story_MarekArrival`
- `EV_Transfer_Inn`
- `EV_NPC_Blacksmith`
- `EV_Chest_NorthRoom`
- `EV_Controller_AttackScene`
- `DEC_Fireplace`

Avoid generic names such as `Event001`, `Guy`, or `Thing` except for temporary experiments.

## 1.10 Switch and Self-Switch Policy

Use global switches only when state must be known outside the local event/map.

Prefer self switches for local persistent states such as:

- chest opened
- one-time local dialogue complete
- local lever activated
- local door permanently opened

## 1.11 ID Stability Rule

**Once an ID has entered an implemented build, never reuse it for a different object.**

Deleted IDs become **retired** rather than recycled. Renaming an object does not change its Bible ID.

## 1.12 Reserved ID Ranges

To be assigned before Prologue implementation begins. Ranges should separate system, Prologue, Acts, debug, and deferred content where practical.

## 1.13 Versioning and Change Control

Meaningful structural changes must be recorded in `CHANGELOG.md`.

Changes that affect dependencies should record affected IDs, especially:

- actor IDs
- map IDs
- switch IDs
- variable IDs
- item/equipment IDs
- common-event IDs
- scene IDs

## 1.14 Plugin and Custom-Code Policy

Default to stock RPG Maker MZ behavior unless a plugin or custom JavaScript solves a demonstrated need.

Every plugin must record:

- purpose
- version
- source
- license
- dependencies
- configuration notes
- affected systems

Custom JavaScript should be kept narrow, documented, and avoid replacing stock systems unnecessarily.

---

# Section 2 — Story & Narrative Implementation

Contains:

- Prologue, Acts I–V, and Epilogue structure
- story scenes and scene order
- scene implementation registry
- mandatory story beats
- dialogue implementation
- choices and branching logic
- cinematics and scripted sequences
- main quest spine
- quest-state registry
- world-state changes
- lore delivery
- deferred narrative content

Primary question: **What happens, in what order, and what game state changes when it happens?**

---

# Section 3 — Characters, Actors & Factions

Contains:

- playable actors
- temporary/guest actors
- NPCs and recurring story characters
- classes
- stat progression
- learned skills
- equipment restrictions
- recruitment conditions
- character visual states
- factions and political relationships

Primary question: **Who exists, what can they do, and what state are they in?**

---

# Section 4 — World, Maps & Exploration

Contains:

- world regions and geography
- map registry and hierarchy
- map availability by story stage
- tilesets
- map transfers
- local map events
- travel/access rules
- dungeon structure
- town structure
- puzzles
- treasure locations
- environmental storytelling
- physical world-state changes

Primary question: **Where is the player, what can they interact with, and where can they go?**

---

# Section 5 — Combat & Progression Systems

Contains:

- battle rules
- party rules
- enemies
- troops
- bosses
- encounter rules
- skills
- states
- elements and damage types
- experience and levels
- stat progression
- defeat/escape behavior
- balancing targets

Primary question: **How does the RPG play when combat starts?**

---

# Section 6 — Items, Equipment & Economy

Contains:

- consumables
- key items
- quest items
- weapons
- armor
- accessories
- relics
- shops and vendors
- currency
- prices
- loot
- chest rewards
- boss rewards
- equipment progression

Primary question: **What does the player acquire, equip, spend, consume, or carry?**

---

# Section 7 — Game State, Events & Logic

Contains:

- global switches
- variables
- self-switch conventions
- common events
- event-state rules
- story progression state
- reusable temporary variables
- system flags
- event dependencies
- cross-reference registry

Primary question: **What logic makes the story and systems behave correctly?**

---

# Section 8 — Presentation & Assets

Contains:

- character sprites
- face graphics
- battlers
- tilesets
- pictures and story illustrations
- interface graphics
- animations and visual effects
- music
- ambient audio
- sound effects
- dialogue presentation rules
- menus and title/game-over presentation
- asset licensing/source tracking

Primary question: **How does the player see and hear the game?**

---

# Section 9 — Production, Testing & Release

Contains:

- asset registry
- ID registry
- implementation status
- debug systems
- development maps
- continuity testing
- event testing
- transfer testing
- combat testing
- save/load testing
- regression testing
- sequence-breaking and soft-lock testing
- release packaging
- credits and licensing
- deferred-content tracking

Primary question: **How do we know the game is correct, reproducible, and ready to ship?**

---

# Immediate Production Strategy

The first full implementation target is the **Prologue vertical slice**.

The Prologue should be built end-to-end before full production expands into later acts. Its purpose is to establish a repeatable workflow for:

1. story scene decomposition
2. actor/database assignment
3. map planning
4. switches and variables
5. event construction
6. dialogue implementation
7. battle implementation
8. visual/audio placeholders
9. testing and regression checks
10. JSON generation and validation

Optional side quests, historical books, hidden content, decorative interactions, and similar additions remain **DEFERRED** until the core story spine is functioning.
