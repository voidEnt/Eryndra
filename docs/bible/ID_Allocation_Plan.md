# Eryndra RPG Maker MZ ID Allocation Plan

**Version:** 0.1  
**Status:** Active allocation policy  
**Purpose:** Reserve stable numeric ranges before JSON implementation begins.

---

## Core Rule

Where an Eryndra Bible object has a direct one-to-one RPG Maker MZ numeric ID, the Bible numeric suffix should match the MZ ID whenever practical.

Examples:

- `ACT-001` = RPG Maker Actor ID 1
- `MAP-001` = `Map001.json`
- `SW-0100` = RPG Maker Switch 100
- `VR-0001` = RPG Maker Variable 1
- `CE-020` = RPG Maker Common Event 20

This reduces translation errors during JSON generation and debugging.

Bible IDs that do **not** correspond to a global MZ database ID, such as story scenes and named NPC identities, remain independent logical IDs.

---

## ID Stability

An ID is considered structurally locked once it has entered an implemented game build.

Before implementation, an Assigned entry may still be moved if required by architecture changes. After implementation:

- do not recycle deleted IDs
- do not renumber merely to make a table prettier
- renamed content keeps its numeric ID
- promoted/demoted production priority keeps its numeric ID

Retired IDs remain retired.

---

## Deferred Content Policy

`DEFERRED` means **optional content not yet required by the story spine**. It is deliberately flexible.

Deferred content may be:

- added
- removed
- renamed
- reorganized
- promoted to SUPPORT or CORE
- replaced entirely

A deferred entry does not become numerically protected merely because space was reserved for it. Protection begins when the actual entry enters an implemented build.

If an already implemented deferred entry is later promoted to CORE, its ID remains where it is; only the priority classification changes.

The Deferred ranges are therefore **holding pools, not promises about final content count or placement**.

---

# Scope-Based Ranges

## Maps

The initial project deliberately stays within IDs 001-999 for simple filenames and conservative compatibility, even if a later MZ version permits more.

| Scope | MZ Map IDs |
|---|---:|
| Prologue | 001-049 |
| Act I | 050-149 |
| Act II | 150-249 |
| Act III | 250-349 |
| Act IV | 350-449 |
| Act V | 450-549 |
| Epilogue | 550-599 |
| System / utility | 600-649 |
| Debug / development | 650-699 |
| Deferred / optional | 700-899 |
| Unallocated reserve | 900-999 |

Current Prologue map assignments occupy 001-008.

---

## Switches

RPG Maker MZ supports 5,000 game switches. Eryndra reserves large story blocks so later acts can grow without renumbering earlier work.

| Scope | MZ Switch IDs |
|---|---:|
| System | 0001-0099 |
| Prologue | 0100-0299 |
| Act I | 0300-0799 |
| Act II | 0800-1299 |
| Act III | 1300-1799 |
| Act IV | 1800-2299 |
| Act V | 2300-2799 |
| Epilogue | 2800-2999 |
| Debug | 3000-3199 |
| Deferred / optional | 3200-4499 |
| Unallocated reserve | 4500-5000 |

Local one-event state should continue to use Self Switches A-D instead of consuming global switch IDs.

---

## Variables

RPG Maker MZ supports 5,000 variables. Eryndra intentionally reserves far fewer initially because variables should represent values/counters rather than boolean facts.

| Scope | MZ Variable IDs |
|---|---:|
| System | 0001-0049 |
| Prologue | 0050-0099 |
| Act I | 0100-0249 |
| Act II | 0250-0399 |
| Act III | 0400-0549 |
| Act IV | 0550-0699 |
| Act V | 0700-0849 |
| Epilogue | 0850-0899 |
| Debug | 0900-0949 |
| Deferred / optional | 0950-1249 |
| Unallocated reserve | 1250-5000 |

`VR-0001 / SYS_StoryStage` is the first assigned system variable.

---

## Common Events

| Scope | MZ Common Event IDs |
|---|---:|
| System | 001-019 |
| Prologue | 020-039 |
| Act I | 040-079 |
| Act II | 080-119 |
| Act III | 120-159 |
| Act IV | 160-199 |
| Act V | 200-239 |
| Epilogue | 240-259 |
| Debug | 260-299 |
| Deferred / optional | 300-399 |
| Unallocated reserve | 400+ |

Common Events that later prove genuinely global should use the System range even if first introduced during the Prologue.

---

## Items

Item ranges describe where an item is first introduced or primarily owned by the design, not every act in which it may later appear.

| Scope | MZ Item IDs |
|---|---:|
| System / common consumables | 001-099 |
| Prologue | 100-149 |
| Act I | 150-299 |
| Act II | 300-449 |
| Act III | 450-599 |
| Act IV | 600-749 |
| Act V | 750-899 |
| Epilogue | 900-949 |
| Debug | 950-999 |
| Deferred / optional | 1000-1499 |
| Unallocated reserve | 1500+ |

No Prologue CORE item currently requires assignment.

---

## Enemies and Troops

Enemies and troops use the same scope boundaries so related encounter content remains easy to locate.

| Scope | Enemy IDs | Troop IDs |
|---|---:|---:|
| Prologue | 001-024 | 001-024 |
| Act I | 025-149 | 025-149 |
| Act II | 150-274 | 150-274 |
| Act III | 275-399 | 275-399 |
| Act IV | 400-524 | 400-524 |
| Act V | 525-649 | 525-649 |
| Epilogue | 650-699 | 650-699 |
| System / utility | 700-749 | 700-749 |
| Debug | 750-799 | 750-799 |
| Deferred / optional | 800-999 | 800-999 |
| Unallocated reserve | 1000+ | 1000+ |

The Prologue currently uses none of its reserved enemy/troop range. That empty space is intentional and does not imply combat will be added.

---

# Identity / Semantic Databases

Some databases should **not** be organized by story act because their contents persist across the whole game.

## Actors

| Purpose | Actor IDs |
|---|---:|
| Core playable cast | 001-009 |
| Temporary / guest playable actors | 010-029 |
| Optional / future playable actors | 030-099 |
| General reserve | 100-899 |
| Debug/test actors | 900-999 |

`ACT-001 / Marek Venn` is assigned Actor ID 1.

## Classes, Skills, Weapons, Armor, States, Animations, Tilesets

Detailed ranges remain intentionally **unassigned** until their underlying systems are designed. These resources are better grouped semantically—by class family, character use, equipment family, element, or system role—than by Act.

Assigning them now would create artificial structure before combat/progression design exists.

---

# Story Stage Value Convention

`VR-0001 / SYS_StoryStage` is a system variable used to identify the next/current required main-story implementation scene.

Value families:

- `1001-1999` — Prologue
- `2001-2999` — Act I
- `3001-3999` — Act II
- `4001-4999` — Act III
- `5001-5999` — Act IV
- `6001-6999` — Act V
- `7001-7999` — Epilogue
- `9001-9999` — debug/test staging if needed

For the current Prologue decomposition:

| Value | Meaning |
|---:|---|
| 1001 | `PRO-SC-001` is current/next |
| 1002 | `PRO-SC-002` is current/next |
| 1003 | `PRO-SC-003` is current/next |
| 1004 | `PRO-SC-004` is current/next |
| 1005 | `PRO-SC-005` is current/next |
| 1006 | `PRO-SC-006` is current/next |
| 1007 | `PRO-SC-007` is current/next |
| 1008 | `PRO-SC-008` is current/next |
| 1009 | `PRO-SC-009` is current/next |
| 1010 | `PRO-SC-010` is current/next |
| 1011 | `PRO-SC-011` is current/next |
| 1012 | `PRO-SC-012` is current/next |
| 2001 | Prologue is complete; Act I opening is current/next |

The stage variable controls the linear spine. Persistent switches record facts that later scenes may need to know independently.
