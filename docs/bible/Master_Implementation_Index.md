# Eryndra Master Implementation Index

**Version:** 0.4  
**Purpose:** Compact cross-project registry linking story canon to RPG Maker MZ implementation.

Detailed specifications live in the main Bible and dedicated registry documents.

Key allocation references:

- `ID_Allocation_Plan.md`
- `Prologue_MZ_ID_Assignments.md`
- `../design/Prologue_Implementation_Decomposition.md`

---

## Status Legend

### Priority
- `CORE` — required for the main story spine
- `SUPPORT` — required for CORE content to function correctly
- `DEFERRED` — optional content postponed until later

### Implementation Status
- `Concept`
- `Defined`
- `Assigned`
- `Implemented`
- `Tested`
- `Locked`

`DEFERRED` is intentionally flexible. Priority may change later without forcing an implemented ID to move.

---

## Direct-ID Alignment Rule

Where practical, Bible IDs for direct RPG Maker data match the MZ numeric ID:

- `ACT-001` = Actor 1
- `MAP-001` = `Map001.json`
- `SW-0100` = Switch 100
- `VR-0001` = Variable 1

Story scene and named-NPC Bible IDs remain logical identifiers because they do not map one-to-one to a global MZ database ID.

---

## Master Registry

| Bible ID | Type | Name | Scope | Priority | MZ ID / File | Related Scene / Map | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| `ACT-001` | Actor | Marek Venn | Prologue+ | CORE | Actor 1 | `PRO-SC-002` onward | Assigned | Playable lead |
| `MAP-001` | Map | Forgotten Watcher Station | Prologue | CORE | `Map001.json` | `PRO-SC-001`, `PRO-SC-012` | Implemented | Pass-02 RUN-001 retracted; RUN-002 tint and RUN-003 Move Picture corrections applied; combined MZ runtime acceptance and promotion remain pending |
| `MAP-002` | Map | Brackenford - Venn Home | Prologue | CORE | `Map002.json` | `PRO-SC-002`, `PRO-SC-011` | Assigned | Family/home anchor |
| `MAP-003` | Map | Brackenford | Prologue | CORE | `Map003.json` | `PRO-SC-003`, `005`, `010` | Assigned | Primary town map |
| `MAP-004` | Map | Brackenford - Survey Office | Prologue | CORE | `Map004.json` | `PRO-SC-004`, `010` | Assigned | Assignment/report location |
| `MAP-005` | Map | Northern Road | Prologue | CORE | `Map005.json` | `PRO-SC-005`, `006` | Assigned | Main exploration route |
| `MAP-006` | Map | Old Place - Exterior | Prologue | CORE | `Map006.json` | `PRO-SC-007` | Assigned | Discovery/approach |
| `MAP-007` | Map | Old Place - Interior | Prologue | CORE | `Map007.json` | `PRO-SC-008`, `012` | Assigned | Contact location |
| `MAP-008` | Map | Network Echo Staging | Prologue | CORE | `Map008.json` | `PRO-SC-009`, `012` | Assigned | Cinematic abstraction; may split later |
| `VR-0001` | Variable | SYS_StoryStage | System | CORE | Variable 1 | All main-story scenes | Assigned | Linear story-spine controller |

---

## Scene Registry

| Scene ID | Scene Name | Maps | Actors / NPCs | Required State | State Changes | Battle | Next Scene | Priority | Status |
|---|---|---|---|---|---|---|---|---|---|
| `PRO-SC-001` | The Forgotten Place | `MAP-001` | None living | New Game | Prologue starts; watcher station awakens | None | `PRO-SC-002` | CORE | Implemented |
| `PRO-SC-002` | Morning at the Venn House | `MAP-002` | Marek, Davren, Elira, Nessa, Latch | Stage 1002 | Family intro complete | None | `PRO-SC-003` | CORE | Defined |
| `PRO-SC-003` | Brackenford Morning | `MAP-003` | Marek, Latch, generic NPCs | Stage 1003 | Survey Office reached | None | `PRO-SC-004` | CORE | Defined |
| `PRO-SC-004` | The Survey Assignment | `MAP-004` | Marek, Joren, Edrin, Latch | Stage 1004 | Assignment received | None | `PRO-SC-005` | CORE | Defined |
| `PRO-SC-005` | Leaving Brackenford | `MAP-003`, `MAP-005` | Marek, Edrin, Latch | Stage 1005 | Brackenford departed | None | `PRO-SC-006` | CORE | Defined |
| `PRO-SC-006` | Beyond the Familiar | `MAP-005` | Marek, Latch | Stage 1006 | Old Place discovered | None | `PRO-SC-007` | CORE | Defined |
| `PRO-SC-007` | The Exposed Structure | `MAP-006` | Marek, Latch | Stage 1007 | Interior access enabled | None | `PRO-SC-008` | CORE | Defined |
| `PRO-SC-008` | Contact | `MAP-007` | Marek; Latch outside | Stage 1008 | Contact; node awakened; Marek imprinted | None | `PRO-SC-009` | CORE | Defined |
| `PRO-SC-009` | The Echo | `MAP-008` | Cael, unnamed to audience | Stage 1009 | Network echo observed | None | `PRO-SC-010` | CORE | Defined |
| `PRO-SC-010` | The Report | `MAP-003`, `MAP-004` | Marek, Joren, Edrin, Latch | Stage 1010 | Survey report complete | None | `PRO-SC-011` | CORE | Defined |
| `PRO-SC-011` | Home, But Changed | `MAP-002` | Marek, Davren, Elira, Nessa, Latch | Stage 1011 | Evening home sequence complete | None | `PRO-SC-012` | CORE | Defined |
| `PRO-SC-012` | The Omen | `MAP-001`, `MAP-007`, `MAP-008` | Marek sleeping; cinematic only | Stage 1012 | Prologue complete; stage -> 2001 | None | Act I | CORE | Defined |

---

## Actor Registry

| Bible ID | Name | MZ Actor ID | Class | First Scene | Starting Level | Graphics | Priority | Status |
|---|---|---:|---|---|---:|---|---|---|
| `ACT-001` | Marek Venn | 1 | TBD | `PRO-SC-002` | TBD | TBD | CORE | Assigned |

---

## NPC Registry

| Bible ID | Name | Role | First Scene | Primary Map(s) | Graphic | Priority | Status |
|---|---|---|---|---|---|---|---|
| `NPC-001` | Davren Venn | Marek's father | `PRO-SC-002` | `MAP-002` | TBD | CORE | Assigned |
| `NPC-002` | Elira Venn | Marek's mother | `PRO-SC-002` | `MAP-002` | TBD | CORE | Assigned |
| `NPC-003` | Nessa Venn | Marek's younger sister | `PRO-SC-002` | `MAP-002` | TBD | CORE | Assigned |
| `NPC-004` | Latch | One-eared road dog / companion event NPC | `PRO-SC-002` | Multiple | TBD | CORE | Assigned |
| `NPC-005` | Joren Pell | Survey mentor | `PRO-SC-004` | `MAP-004` | TBD | CORE | Assigned |
| `NPC-006` | Edrin Holt | Road Warden / Marek's oldest friend | `PRO-SC-004` | `MAP-004`, `MAP-005` | TBD | CORE | Assigned |
| `NPC-007` | Cael Veyran | Hidden-identity observer | `PRO-SC-009` | Cinematic staging | TBD | CORE | Assigned |

---

## Map Registry

| Bible ID | MZ Map ID | Map Name | Parent | Required Scenes | Priority | Status |
|---|---:|---|---|---|---|---|
| `MAP-001` | 1 | Forgotten Watcher Station | TBD | `PRO-SC-001`, `012` | CORE | Implemented - Static PASS; runtime test pending |
| `MAP-002` | 2 | Brackenford - Venn Home | `MAP-003` | `PRO-SC-002`, `011` | CORE | Assigned |
| `MAP-003` | 3 | Brackenford | TBD | `PRO-SC-003`, `005`, `010` | CORE | Assigned |
| `MAP-004` | 4 | Brackenford - Survey Office | `MAP-003` | `PRO-SC-004`, `010` | CORE | Assigned |
| `MAP-005` | 5 | Northern Road | TBD | `PRO-SC-005`, `006` | CORE | Assigned |
| `MAP-006` | 6 | Old Place - Exterior | `MAP-005` | `PRO-SC-007` | CORE | Assigned |
| `MAP-007` | 7 | Old Place - Interior | `MAP-006` | `PRO-SC-008`, `012` | CORE | Assigned |
| `MAP-008` | 8 | Network Echo Staging | TBD | `PRO-SC-009`, `012` | CORE | Assigned |

---

## Switch Registry

| Bible ID | MZ ID | MZ Name | Purpose | Set By | Priority | Status |
|---|---:|---|---|---|---|---|
| `SW-0100` | 100 | `PRO_Started` | Prologue begun | `PRO-SC-001` | CORE | Assigned |
| `SW-0101` | 101 | `PRO_WatcherStation_Awakened` | Watcher station activated | `PRO-SC-001` | CORE | Assigned |
| `SW-0102` | 102 | `PRO_VennHome_Intro_Complete` | Initial home scene complete | `PRO-SC-002` | CORE | Assigned |
| `SW-0103` | 103 | `PRO_Survey_Assignment_Received` | Survey task assigned | `PRO-SC-004` | CORE | Assigned |
| `SW-0104` | 104 | `PRO_Left_Brackenford` | Marek departed town | `PRO-SC-005` | CORE | Assigned |
| `SW-0105` | 105 | `PRO_OldPlace_Discovered` | Exposed structure found | `PRO-SC-006` | CORE | Assigned |
| `SW-0106` | 106 | `PRO_Contact_Complete` | Ring contact completed | `PRO-SC-008` | CORE | Assigned |
| `SW-0107` | 107 | `PRO_LocalNode_Awakened` | Local ancient node activated | `PRO-SC-008` | CORE | Assigned |
| `SW-0108` | 108 | `PRO_Marek_Imprinted` | Hidden imprint state | `PRO-SC-008` | CORE | Assigned |
| `SW-0109` | 109 | `PRO_Network_Echo_Observed` | Echo montage occurred | `PRO-SC-009` | CORE | Assigned |
| `SW-0110` | 110 | `PRO_Report_Complete` | Survey report complete | `PRO-SC-010` | CORE | Assigned |
| `SW-0111` | 111 | `PRO_HomeEvening_Complete` | Home evening complete | `PRO-SC-011` | CORE | Assigned |
| `SW-0112` | 112 | `PRO_Complete` | Prologue complete | `PRO-SC-012` | CORE | Assigned |

---

## Variable Registry

| Bible ID | MZ ID | MZ Name | Purpose | Values | Priority | Status |
|---|---:|---|---|---|---|---|
| `VR-0001` | 1 | `SYS_StoryStage` | Main story spine controller | Prologue 1001-1012; Act I begins 2001 | CORE | Assigned |

---

## Common Event Registry

| Bible ID | MZ Common Event ID | Name | Scope | Purpose | Priority | Status |
|---|---:|---|---|---|---|---|
| TBD | TBD | Three-note resonance presentation | System/Prologue | Candidate reusable presentation logic; assign only if implementation proves useful | SUPPORT | Concept |

---

## Item / Equipment Registry

No story-critical Prologue item/equipment entry has yet been identified. Marek's field kit remains narrative equipment unless gameplay requires inventory/database behavior.

---

## Enemy / Troop Registry

The locked Prologue contains **no required combat** and therefore requires no CORE enemies or troops. Enemy/Troop IDs 001-024 are reserved for the Prologue but intentionally empty.

---

## Asset Registry Summary

| Asset Type | Subject / Location | Used By | Priority | Status |
|---|---|---|---|---|
| Visual motif | Fractured ring | `PRO-SC-001`, `008`, `009`, `012` | CORE | Concept |
| Audio | Three-note resonance | `PRO-SC-001`, `006`, `008`, `009`, `011`, `012` | CORE | Concept |
| Character graphics | Marek Venn | Prologue playable scenes | CORE | Concept |
| Character graphics | Venn family / Joren / Edrin / Latch / Cael | Prologue story scenes | CORE | Concept |
| Tileset TIL-007 | Cinematic Parallax Collision | MAP-001 and later cinematic maps | SUPPORT | Implemented |
| Parallax PIC-001 | MAP001 Watcher Station Base | MAP-001 | CORE | Implemented |
| Picture PIC-002 | MAP001 Ring Pulse | PRO-SC-001, 012 | CORE | Implemented |
| Picture PIC-003 | MAP001 Ring Residual | PRO-SC-001 | CORE | Implemented |
| Picture PIC-004 | MAP001 Ring Propagated | PRO-SC-012 | CORE | Implemented |
| Picture PIC-005 | MAP001 Dust Tremor | PRO-SC-001 | CORE | Implemented |
| Picture PIC-006 | Eryndra Title | PRO-SC-001 | CORE | Implemented |
| Audio SE-001 | Ancient Three-Note Resonance | PRO-SC-001, 006, 008, 009, 011, 012 | CORE | Implemented |

---

## Cross-Reference Pattern

`Story Scene → Map → Event → Actor/NPC → Switch/Variable → Item/Battle/Asset → Resulting State → Next Scene`

Every CORE story scene should eventually be traceable through this chain without rereading the full narrative source.

---

# Reserved ID Range Summary

See `ID_Allocation_Plan.md` for policy and rationale.

| Resource | System | Prologue | Act I | Act II | Act III | Act IV | Act V | Epilogue | Debug | Deferred | Reserve |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Maps | 600-649 | 001-049 | 050-149 | 150-249 | 250-349 | 350-449 | 450-549 | 550-599 | 650-699 | 700-899 | 900-999 |
| Switches | 0001-0099 | 0100-0299 | 0300-0799 | 0800-1299 | 1300-1799 | 1800-2299 | 2300-2799 | 2800-2999 | 3000-3199 | 3200-4499 | 4500-5000 |
| Variables | 0001-0049 | 0050-0099 | 0100-0249 | 0250-0399 | 0400-0549 | 0550-0699 | 0700-0849 | 0850-0899 | 0900-0949 | 0950-1249 | 1250-5000 |
| Common Events | 001-019 | 020-039 | 040-079 | 080-119 | 120-159 | 160-199 | 200-239 | 240-259 | 260-299 | 300-399 | 400+ |
| Items | 001-099 | 100-149 | 150-299 | 300-449 | 450-599 | 600-749 | 750-899 | 900-949 | 950-999 | 1000-1499 | 1500+ |
| Enemies | 700-749 | 001-024 | 025-149 | 150-274 | 275-399 | 400-524 | 525-649 | 650-699 | 750-799 | 800-999 | 1000+ |
| Troops | 700-749 | 001-024 | 025-149 | 150-274 | 275-399 | 400-524 | 525-649 | 650-699 | 750-799 | 800-999 | 1000+ |

Actors/classes/skills/weapons/armor/states/animations/tilesets are handled semantically rather than by Act; see `ID_Allocation_Plan.md`.
