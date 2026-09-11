# Eryndra Prologue RPG Maker MZ ID Assignments

**Version:** 0.1  
**Scope:** Prologue CORE implementation  
**Status:** Assigned; not yet implemented

These assignments are the first concrete bridge from the living Bible to RPG Maker MZ JSON data.

Until an entry enters an implemented build, an assignment may still be corrected if a structural problem is found. After implementation, the normal ID stability/retirement rule applies.

---

# Actor Assignments

| Bible ID | MZ Actor ID | Name | Status |
|---|---:|---|---|
| `ACT-001` | 1 | Marek Venn | Assigned |

The remaining named Prologue characters are currently map/story NPCs rather than Actors database entries.

---

# Map Assignments

Bible map IDs intentionally match MZ map IDs.

| Bible ID | MZ Map ID / File | Map Name | Required Scenes | Status |
|---|---|---|---|---|
| `MAP-001` | `Map001.json` | Forgotten Watcher Station | `PRO-SC-001`, `PRO-SC-012` | Assigned |
| `MAP-002` | `Map002.json` | Brackenford - Venn Home | `PRO-SC-002`, `PRO-SC-011` | Assigned |
| `MAP-003` | `Map003.json` | Brackenford | `PRO-SC-003`, `PRO-SC-005`, `PRO-SC-010` | Assigned |
| `MAP-004` | `Map004.json` | Brackenford - Survey Office | `PRO-SC-004`, `PRO-SC-010` | Assigned |
| `MAP-005` | `Map005.json` | Northern Road | `PRO-SC-005`, `PRO-SC-006` | Assigned |
| `MAP-006` | `Map006.json` | Old Place - Exterior | `PRO-SC-007` | Assigned |
| `MAP-007` | `Map007.json` | Old Place - Interior | `PRO-SC-008`, `PRO-SC-012` | Assigned |
| `MAP-008` | `Map008.json` | Network Echo Staging | `PRO-SC-009`, `PRO-SC-012` | Assigned |

`MAP-008` may later be split if one reusable staging map cannot cleanly present the distant echo/omen locations. Any additional Prologue maps should use `MAP-009` through `MAP-049`.

---

# Global Switch Assignments

| Bible ID | MZ Switch ID | MZ Name | Set By | Purpose | Status |
|---|---:|---|---|---|---|
| `SW-0100` | 100 | `PRO_Started` | `PRO-SC-001` | Prologue has begun | Assigned |
| `SW-0101` | 101 | `PRO_WatcherStation_Awakened` | `PRO-SC-001` | Ancient watcher station has activated | Assigned |
| `SW-0102` | 102 | `PRO_VennHome_Intro_Complete` | `PRO-SC-002` | Initial family/home introduction complete | Assigned |
| `SW-0103` | 103 | `PRO_Survey_Assignment_Received` | `PRO-SC-004` | Northern survey assignment received | Assigned |
| `SW-0104` | 104 | `PRO_Left_Brackenford` | `PRO-SC-005` | Marek departed Brackenford | Assigned |
| `SW-0105` | 105 | `PRO_OldPlace_Discovered` | `PRO-SC-006` | Old Place exposed structure discovered | Assigned |
| `SW-0106` | 106 | `PRO_Contact_Complete` | `PRO-SC-008` | Marek completed contact with the fractured ring | Assigned |
| `SW-0107` | 107 | `PRO_LocalNode_Awakened` | `PRO-SC-008` | Local ancient node awakened | Assigned |
| `SW-0108` | 108 | `PRO_Marek_Imprinted` | `PRO-SC-008` | Invisible intermediary imprint state recorded | Assigned |
| `SW-0109` | 109 | `PRO_Network_Echo_Observed` | `PRO-SC-009` | Network echo montage has occurred | Assigned |
| `SW-0110` | 110 | `PRO_Report_Complete` | `PRO-SC-010` | Survey report completed | Assigned |
| `SW-0111` | 111 | `PRO_HomeEvening_Complete` | `PRO-SC-011` | Evening home sequence completed | Assigned |
| `SW-0112` | 112 | `PRO_Complete` | `PRO-SC-012` | Prologue completed | Assigned |

IDs 113-299 remain free inside the Prologue switch range.

### Switch design note

These global switches represent facts that may matter outside the event that sets them. Minor local interactions, doors, chests, one-time ambient lines, and similar event-local state should use Self Switches A-D where possible.

---

# Variable Assignments

| Bible ID | MZ Variable ID | MZ Name | Purpose | Status |
|---|---:|---|---|---|
| `VR-0001` | 1 | `SYS_StoryStage` | Main story spine state / next required implementation scene | Assigned |

No Prologue-local variable is assigned yet. IDs 50-99 remain reserved for Prologue variables when counters, puzzle values, or temporary cross-map state are actually demonstrated to be necessary.

---

# `SYS_StoryStage` Prologue Values

| Value | Current / Next Required Scene |
|---:|---|
| 1001 | `PRO-SC-001` |
| 1002 | `PRO-SC-002` |
| 1003 | `PRO-SC-003` |
| 1004 | `PRO-SC-004` |
| 1005 | `PRO-SC-005` |
| 1006 | `PRO-SC-006` |
| 1007 | `PRO-SC-007` |
| 1008 | `PRO-SC-008` |
| 1009 | `PRO-SC-009` |
| 1010 | `PRO-SC-010` |
| 1011 | `PRO-SC-011` |
| 1012 | `PRO-SC-012` |
| 2001 | Prologue complete; Act I opening is current/next |

At New Game initialization, `SYS_StoryStage` should be set to `1001` before or as the opening Prologue controller begins.

At successful completion of each scene, the stage advances to the next value. `PRO-SC-012` sets both `SW-0112 PRO_Complete = ON` and `SYS_StoryStage = 2001`.

---

# Common Events

No Common Event is numerically assigned yet.

The recurring three-note resonance presentation remains a candidate system Common Event, but it should receive an ID only after the first map implementation proves that shared event logic is actually useful rather than merely shared audio assets.

---

# Items / Equipment

No Prologue CORE Item, Weapon, or Armor IDs are assigned yet.

Marek's ordinary field kit should not become database inventory merely because it exists in prose. Only objects that require gameplay inventory behavior, equipment behavior, or explicit state tracking should consume database IDs.

---

# Enemies / Troops

No Prologue CORE Enemy or Troop IDs are assigned.

The reserved Prologue ranges 001-024 remain empty. This is intentional: the locked Prologue contains no required combat.

---

# Next Implementation Target

With the allocation layer established, the next technical target is `MAP-001 / Map001.json` and `PRO-SC-001 The Forgotten Place`.

That implementation should define:

1. map dimensions and tileset strategy
2. opening cinematic event controller(s)
3. New Game initialization of `VR-0001`
4. setting `SW-0100` and `SW-0101`
5. title transition
6. handoff to `MAP-002` / `PRO-SC-002`
7. placeholder visual/audio assets where final assets do not yet exist
8. a repeatable JSON validation/playtest checklist
