# Eryndra Master Implementation Index

**Version:** 0.1  
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
| TBD | — | — | — | — | — | — | — | Initial registry awaiting Prologue decomposition |

---

## Scene Registry

| Scene ID | Scene Name | Story Scope | Maps | Actors / NPCs | Required State | State Changes | Battle | Next Scene | Priority | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `PRO-SC-001` | TBD | Prologue | TBD | TBD | TBD | TBD | TBD | TBD | CORE | Concept |

---

## Actor Registry

| Bible ID | Name | MZ Actor ID | Class | First Scene | Starting Level | Graphics | Priority | Status |
|---|---|---:|---|---|---:|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | CORE | Concept |

---

## NPC Registry

| Bible ID | Name | Role | First Scene | Primary Map(s) | Graphic | Priority | Status |
|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | Concept |

---

## Map Registry

| Bible ID | MZ Map ID | Map Name | Parent | Story Scope | Tileset | Required Scenes | Priority | Status |
|---|---:|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | CORE | Concept |

---

## Switch Registry

| Bible ID | MZ Switch ID | MZ Name | Scope | Purpose | Set By | Read By | Priority | Status |
|---|---:|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | CORE | Concept |

---

## Variable Registry

| Bible ID | MZ Variable ID | MZ Name | Scope | Purpose | Values / Range | Written By | Read By | Priority | Status |
|---|---:|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | SUPPORT | Concept |

---

## Common Event Registry

| Bible ID | MZ Common Event ID | Name | Scope | Purpose | Called By | Priority | Status |
|---|---:|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | SUPPORT | Concept |

---

## Item / Equipment Registry

| Bible ID | Type | MZ ID | Name | Story Scope | Acquisition | Story Critical | Priority | Status |
|---|---|---:|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Concept |

---

## Enemy / Troop Registry

| Bible ID | Type | MZ ID | Name | Scope / Region | Used In | Priority | Status |
|---|---|---:|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | CORE | Concept |

---

## Asset Registry Summary

| Bible ID | Asset Type | Filename | Subject / Location | Used By | Source / License | Priority | Status |
|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | Concept |

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
