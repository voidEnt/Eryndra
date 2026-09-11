# Eryndra Master Implementation Index

**Version:** 0.2  
**Purpose:** Compact cross-project registry linking story canon to RPG Maker MZ implementation.

This file is intentionally concise. Detailed specifications belong in the main Bible or dedicated registry documents.

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

---

## Master Registry

| Bible ID | Type | Name | Scope | Priority | MZ ID / File | Related Scene / Map | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| `ACT-001` | Actor | Marek Venn | Prologue+ | CORE | TBD | `PRO-SC-002` onward | Assigned | Playable lead; MZ numeric ID pending |
| `MAP-001` | Map | Forgotten Watcher Station | Prologue | CORE | TBD | `PRO-SC-001`, `PRO-SC-012` | Assigned | Opening/closing cinematic map |
| `MAP-002` | Map | Brackenford - Venn Home | Prologue | CORE | TBD | `PRO-SC-002`, `PRO-SC-011` | Assigned | Family/home anchor |
| `MAP-003` | Map | Brackenford | Prologue | CORE | TBD | `PRO-SC-003`, `005`, `010` | Assigned | Primary town map |
| `MAP-004` | Map | Brackenford - Survey Office | Prologue | CORE | TBD | `PRO-SC-004`, `010` | Assigned | Assignment/report location |
| `MAP-005` | Map | Northern Road | Prologue | CORE | TBD | `PRO-SC-005`, `006` | Assigned | Main exploration route |
| `MAP-006` | Map | Old Place - Exterior | Prologue | CORE | TBD | `PRO-SC-007` | Assigned | Discovery/approach |
| `MAP-007` | Map | Old Place - Interior | Prologue | CORE | TBD | `PRO-SC-008` | Assigned | Contact location |
| `MAP-008` | Map | Network Echo Staging | Prologue | CORE | TBD | `PRO-SC-009`, `012` | Assigned | Cinematic abstraction; may split later |

---

## Scene Registry

| Scene ID | Scene Name | Story Scope | Maps | Actors / NPCs | Required State | State Changes | Battle | Next Scene | Priority | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `PRO-SC-001` | The Forgotten Place | Prologue | `MAP-001` | None living | New Game | Prologue started; watcher station awakened | None | `PRO-SC-002` | CORE | Defined |
| `PRO-SC-002` | Morning at the Venn House | Prologue | `MAP-002` | Marek, Davren, Elira, Nessa, Latch | `PRO_Started` | Family intro complete | None | `PRO-SC-003` | CORE | Defined |
| `PRO-SC-003` | Brackenford Morning | Prologue | `MAP-003` | Marek, Latch, generic NPCs | Home intro complete | Survey Office reached | None | `PRO-SC-004` | CORE | Defined |
| `PRO-SC-004` | The Survey Assignment | Prologue | `MAP-004` | Marek, Joren, Edrin, Latch | Office reached | Assignment received | None | `PRO-SC-005` | CORE | Defined |
| `PRO-SC-005` | Leaving Brackenford | Prologue | `MAP-003`, `MAP-005` | Marek, Edrin, Latch | Assignment received | Brackenford departed | None | `PRO-SC-006` | CORE | Defined |
| `PRO-SC-006` | Beyond the Familiar | Prologue | `MAP-005` | Marek, Latch | Left Brackenford | Old Place discovered | None | `PRO-SC-007` | CORE | Defined |
| `PRO-SC-007` | The Exposed Structure | Prologue | `MAP-006` | Marek, Latch | Old Place discovered | Interior access enabled | None | `PRO-SC-008` | CORE | Defined |
| `PRO-SC-008` | Contact | Prologue | `MAP-007` | Marek; Latch remains outside | Interior access | Contact complete; node awakened; Marek imprinted | None | `PRO-SC-009` | CORE | Defined |
| `PRO-SC-009` | The Echo | Prologue | `MAP-008` | Cael (unnamed to audience) | Contact complete | Network echo shown; Cael detects activity | None | `PRO-SC-010` | CORE | Defined |
| `PRO-SC-010` | The Report | Prologue | `MAP-003`, `MAP-004` | Marek, Joren, Edrin, Latch | Network echo sequence complete | Survey report complete | None | `PRO-SC-011` | CORE | Defined |
| `PRO-SC-011` | Home, But Changed | Prologue | `MAP-002` | Marek, Davren, Elira, Nessa, Latch | Report complete | Evening home sequence complete | None | `PRO-SC-012` | CORE | Defined |
| `PRO-SC-012` | The Omen | Prologue | `MAP-001`, `MAP-007`, `MAP-008` | Marek sleeping; no active player control | Home evening complete | Prologue complete | None | Act I | CORE | Defined |

Detailed scene specification: `docs/design/Prologue_Implementation_Decomposition.md`.

---

## Actor Registry

| Bible ID | Name | MZ Actor ID | Class | First Scene | Starting Level | Graphics | Priority | Status |
|---|---|---:|---|---|---:|---|---|---|
| `ACT-001` | Marek Venn | TBD | TBD | `PRO-SC-002` | TBD | TBD | CORE | Assigned |

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

| Bible ID | MZ Map ID | Map Name | Parent | Story Scope | Tileset | Required Scenes | Priority | Status |
|---|---:|---|---|---|---|---|---|---|
| `MAP-001` | TBD | Forgotten Watcher Station | TBD | Prologue | TBD | `PRO-SC-001`, `012` | CORE | Assigned |
| `MAP-002` | TBD | Brackenford - Venn Home | `MAP-003` | Prologue | TBD | `PRO-SC-002`, `011` | CORE | Assigned |
| `MAP-003` | TBD | Brackenford | TBD | Prologue | TBD | `PRO-SC-003`, `005`, `010` | CORE | Assigned |
| `MAP-004` | TBD | Brackenford - Survey Office | `MAP-003` | Prologue | TBD | `PRO-SC-004`, `010` | CORE | Assigned |
| `MAP-005` | TBD | Northern Road | TBD | Prologue | TBD | `PRO-SC-005`, `006` | CORE | Assigned |
| `MAP-006` | TBD | Old Place - Exterior | `MAP-005` | Prologue | TBD | `PRO-SC-007` | CORE | Assigned |
| `MAP-007` | TBD | Old Place - Interior | `MAP-006` | Prologue | TBD | `PRO-SC-008`, `012` | CORE | Assigned |
| `MAP-008` | TBD | Network Echo Staging | TBD | Prologue | TBD | `PRO-SC-009`, `012` | CORE | Assigned |

---

## Switch Registry

Numeric MZ switch IDs remain unassigned until reserved ranges are established.

| Bible ID | MZ Switch ID | MZ Name | Scope | Purpose | Set By | Read By | Priority | Status |
|---|---:|---|---|---|---|---|---|---|
| TBD | TBD | `PRO_Started` | Prologue | Prologue has begun | `PRO-SC-001` | Prologue flow | CORE | Defined |
| TBD | TBD | `PRO_WatcherStation_Awakened` | Prologue+ | Ancient watcher station activated | `PRO-SC-001` | Later ancient-system logic | CORE | Defined |
| TBD | TBD | `PRO_VennHome_Intro_Complete` | Prologue | Initial home scene complete | `PRO-SC-002` | `PRO-SC-003` | CORE | Defined |
| TBD | TBD | `PRO_Survey_Assignment_Received` | Prologue | Northern survey task assigned | `PRO-SC-004` | Route/event gates | CORE | Defined |
| TBD | TBD | `PRO_Left_Brackenford` | Prologue | Marek has departed town | `PRO-SC-005` | `PRO-SC-006` | CORE | Defined |
| TBD | TBD | `PRO_OldPlace_Discovered` | Prologue+ | Exposed structure found | `PRO-SC-006` | Old Place events; later continuity | CORE | Defined |
| TBD | TBD | `PRO_Contact_Complete` | Prologue+ | Ring contact sequence completed | `PRO-SC-008` | Echo/return/later continuity | CORE | Defined |
| TBD | TBD | `PRO_LocalNode_Awakened` | Prologue+ | Local ancient node activated | `PRO-SC-008` | Ancient-system continuity | CORE | Defined |
| TBD | TBD | `PRO_Marek_Imprinted` | Prologue+ | Hidden intermediary imprint state | `PRO-SC-008` | Later story logic | CORE | Defined |
| TBD | TBD | `PRO_Network_Echo_Observed` | Prologue | Audience echo montage completed | `PRO-SC-009` | Return sequence gate | CORE | Defined |
| TBD | TBD | `PRO_Report_Complete` | Prologue | Marek reported discovery | `PRO-SC-010` | Home return gate | CORE | Defined |
| TBD | TBD | `PRO_HomeEvening_Complete` | Prologue | Evening scene complete | `PRO-SC-011` | Closing omen gate | CORE | Defined |
| TBD | TBD | `PRO_Complete` | Prologue+ | Prologue fully completed | `PRO-SC-012` | Act I start and later continuity | CORE | Defined |

---

## Variable Registry

| Bible ID | MZ Variable ID | MZ Name | Scope | Purpose | Values / Range | Written By | Read By | Priority | Status |
|---|---:|---|---|---|---|---|---|---|---|
| TBD | TBD | `SYS_StoryStage` | System | Sequential main-story stage gate | Enumerated story-stage values TBD | Main scene controllers | Story/map/event gating | CORE | Defined |

---

## Common Event Registry

| Bible ID | MZ Common Event ID | Name | Scope | Purpose | Called By | Priority | Status |
|---|---:|---|---|---|---|---|---|
| TBD | TBD | Three-note resonance presentation | System/Prologue | Standardize recurring ring/audio motif if reusable event logic proves useful | `PRO-SC-001`, `008`, `009`, `011`, `012` | SUPPORT | Concept |

---

## Item / Equipment Registry

No story-critical Prologue item/equipment entry has yet been identified. Marek's field kit is ordinary narrative equipment unless later implementation requires database objects.

| Bible ID | Type | MZ ID | Name | Story Scope | Acquisition | Story Critical | Priority | Status |
|---|---|---:|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Concept |

---

## Enemy / Troop Registry

The locked Prologue contains **no required combat** and therefore requires no CORE enemies or troops.

| Bible ID | Type | MZ ID | Name | Scope / Region | Used In | Priority | Status |
|---|---|---:|---|---|---|---|---|
| — | — | — | None required for Prologue | Prologue | — | — | Defined |

---

## Asset Registry Summary

| Bible ID | Asset Type | Filename | Subject / Location | Used By | Source / License | Priority | Status |
|---|---|---|---|---|---|---|---|
| TBD | Visual motif | TBD | Fractured ring | `PRO-SC-001`, `008`, `009`, `012` | TBD | CORE | Concept |
| TBD | Audio | TBD | Three-note resonance | `PRO-SC-001`, `006`, `008`, `009`, `011`, `012` | TBD | CORE | Concept |
| TBD | Character graphics | TBD | Marek Venn | Prologue playable scenes | TBD | CORE | Concept |
| TBD | Character graphics | TBD | Venn family / Joren / Edrin / Latch / Cael | Prologue story scenes | TBD | CORE | Concept |

---

## Cross-Reference Pattern

The target dependency chain is:

`Story Scene → Map → Event → Actor/NPC → Switch/Variable → Item/Battle/Asset → Resulting State → Next Scene`

Every CORE story scene should eventually be traceable through this chain without rereading the full narrative source.

---

## Reserved ID Range Registry

Reserved ranges are not yet assigned. Once assigned, do not casually move implemented IDs between ranges.

| Resource | System | Prologue | Act I | Act II | Act III | Act IV | Act V | Epilogue | Debug | Deferred |
|---|---|---|---|---|---|---|---|---|---|---|
| Switches | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Variables | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Common Events | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Maps | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Items | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Enemies | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
