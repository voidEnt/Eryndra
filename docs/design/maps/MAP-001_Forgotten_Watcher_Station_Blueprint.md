# MAP-001 Mapper Work Order - Forgotten Watcher Station

**Bible Map ID:** `MAP-001`  
**RPG Maker Map ID:** `1`  
**Runtime file:** `Map001.json`  
**Story Scope:** Prologue  
**Priority:** CORE  
**Status:** Blueprint Defined  
**Scenes:** `PRO-SC-001 The Forgotten Place`, `PRO-SC-012 The Omen`  
**Locked story source:** `PrologueStoryv0.3`, sections `P-01 The Forgotten Place` and `P-08 The Omen`

---

# 1. Mapper Objective

Build a compact, sealed ancient chamber that can stage both the opening and closing Prologue cinematics.

This is not a dungeon or explorable ruin. It is a buried piece of forgotten infrastructure that has been dormant for centuries and begins to wake without any living character present.

The map must communicate:

- impossible age
- precision beyond Brackenford-era construction
- complete abandonment
- a single dominant focal object: the fractured ring
- restrained unease rather than spectacle

The same geometry must support two cinematic states:

1. **Opening / dormant awakening** - nearly dark; one pulse; three-note signal; one narrow light line remains.
2. **Closing / propagated omen** - same chamber; more of the ring is illuminated; fracture remains black; distant response confirms wider activity.

---

# 2. Narrative Style Gate

Before mapping, re-check the cited locked story sections and verify:

## Required

- No living character is present.
- The chamber appears to have been without useful light for centuries.
- Dust shows no recent traffic.
- Fitted stone and dull unfamiliar metal coexist.
- Roots entered through fine seams and later died.
- The circular form is deliberately divided by a narrow fracture.
- The fracture reads as intentional design, not accidental breakage.
- The chamber feels older than any living kingdom.
- The ring is the visual focal point.
- Opening and closing sequences clearly use the same physical chamber.

## Forbidden implications

Do not add:

- torches, braziers, candles, or evidence of recent habitation
- furniture
- treasure chests or loot
- readable books or inscriptions
- recognizable religious symbolism
- skeletons for atmosphere
- weapons/armor displays
- obvious active machinery
- doors inviting exploration
- visible exits
- explanatory signs
- obvious magical runes
- throne, altar, temple, or royal layout

The map must not itself explain the Convergence, Intermediary, node, network, or watcher-station terminology.

**Theme:** OMEN, not revelation.

---

# 3. Player / Camera Mode

- **Player control:** None
- **Function:** Cinematic staging only
- **Encounters:** None
- **Normal player access:** None in the Prologue
- **Looping:** None

Assume standard MZ rendering at 816x624 with 48 px tiles, approximately a 17x13 tile visible field.

The principal composition should work in one screen with a modest buffer for subtle reframing.

---

# 4. Required Dimensions

**Canvas:** `29 x 21 tiles`

**Active chamber footprint:** approximately `x=5..23`, `y=4..17`.

The outer area is solid/dark buffer so camera movement never exposes map edges.

Do not enlarge the location into a multi-room complex.

---

# 5. Spatial Zones

## Zone A - North Focal Wall

**Approximate bounds:** `x=7..21`, `y=4..7`

Required:

- integrated fractured-ring form centered near `x=14`
- precise fitted stone
- dull metal integrated into the wall
- clean visual area for later ring-light overlays

The ring must not read as a normal doorway or obvious portal.

## Zone B - Central Chamber Floor

**Approximate bounds:** `x=8..20`, `y=8..15`

Required:

- largely uncluttered fitted stone floor
- dust accumulation
- room for visible dust tremor/light staging
- no recent-use path

## Zone C - West Structural Edge

**Approximate bounds:** `x=5..7`, `y=5..16`

Required:

- stone/metal transition
- mild age damage allowed
- no usable passage

## Zone D - East Root/Seam Edge

**Approximate bounds:** `x=21..23`, `y=5..16`

Required:

- dead roots entering through hairline seams
- no daylight opening

## Zone E - South Shadow Foreground

**Approximate bounds:** `x=7..21`, `y=16..17`

Required:

- dark foreground framing
- no usable exit or staircase
- may imply depth only if it does not suggest a playable route

---

# 6. Composition Recipe

```text
                NORTH

        fitted stone / dull metal
      -----------------------------
      |                           |
      |       FRACTURED RING      |
      |            |              |
      |                           |
      |       open dusty floor    |
      |                           |
      | dead roots      seams     |
      |                           |
      -----------------------------
           shadow foreground
```

The ring should sit above center so the floor remains available for dust/vibration effects.

Original construction may be near-symmetrical; age, dead roots, dust, and minor settlement may disturb that symmetry.

---

# 7. Geometry Rules

- One room only.
- No player-facing doorway required.
- Map edges must never be visible in intended camera positions.
- Walls should feel thick and load-bearing.
- Construction should be more exact than ordinary medieval stonework.
- No maze, puzzle, combat lane, platforming, or traversal challenge.
- No elevation mechanic required.

---

# 8. Tileset / Environment Requirements

**Final tileset:** TBD  
**Required family:** Ancient buried technical-stone interior.

Must support:

- dark fitted stone
- dull unfamiliar metal
- dust
- fine seams
- dead roots
- subtle age damage
- clean backing for fractured-ring visual state

A temporary stock tileset is acceptable for first geometry only if all placeholders are documented and stock fantasy-dungeon decoration is kept out.

---

# 9. Required Visual States

The map must leave clean visual support for:

1. **Dormant** - ring nearly invisible.
2. **Pulse** - ring can flash once.
3. **Opening residual** - one narrow illuminated line remains.
4. **Closing propagated** - light has spread farther around circumference; fracture remains black.

Implementation may later use tiles, event graphics, pictures, overlays, animation, or a combination. The mapper must keep the ring area unobstructed.

---

# 10. Actors / NPCs / Sprites

**None.**

Do not place player actors, NPCs, animals, monsters, or corpses.

---

# 11. Required Event Anchors

The mapper places named stubs only. The Eventwright implements command logic later.

| Anchor | Approx. Position | Purpose |
|---|---:|---|
| `EV_Story_PrologueOpening` | `(14,10)` | Controller anchor for `PRO-SC-001` |
| `EV_Story_PrologueOmen` | `(14,10)` | Controller anchor for `PRO-SC-012` |
| `EV_Visual_FracturedRing` | `(14,6)` | Ring graphic/state anchor |
| `EV_FX_DustTremor` | `(14,12)` | Dust/vibration effect anchor |
| `EV_Camera_Chamber` | `(14,10)` | Default framing reference |
| `EV_Camera_Ring` | `(14,8)` | Closer ring framing reference |

Coordinates may move by 1-2 tiles to fit final composition.

No other story events should be invented on this map.

---

# 12. State Dependencies

The map must support, but the mapper does not program:

- `SW-0100 PRO_Started`
- `SW-0101 PRO_WatcherStation_Awakened`
- `SW-0111 PRO_HomeEvening_Complete`
- `SW-0112 PRO_Complete`
- `VR-0001 SYS_StoryStage`
  - `1001` for `PRO-SC-001`
  - `1012` for `PRO-SC-012`

Opening and closing should use the same map rather than duplicate geometry.

---

# 13. Transfers / Spawn

## Opening

The game begins here under cinematic control. The player sprite should not appear in-frame.

After the opening sequence, the Eventwright will transfer to `MAP-002 Brackenford - Venn Home`.

## Closing

The Prologue closing montage returns here under cinematic control. No walk-in entrance is required.

No normal transfer event or visible exit should be created by the mapper.

---

# 14. Passability / Collision / Regions

- Treat outer buffer as fully impassable.
- Chamber edges are sealed.
- No player pathing requirement for the Prologue.
- Do not assign gameplay regions unless a later Eventwright work order explicitly calls for them.
- Do not add ladders, counters, damage floors, or interaction terrain.

---

# 15. Audio / Presentation Dependencies

Spatial design must support later placement of:

- near-silence / low-pressure ambience
- dust tremor
- three evenly spaced notes
- ring pulse and residual light
- fade to black
- title reveal
- later call-and-response in `PRO-SC-012`

No source object other than the fractured ring should visually compete with these cues.

---

# 16. Asset Dependencies

Required or anticipated:

- ancient fitted-stone tiles
- dull-metal tiles/overlay elements
- dead-root detail
- fractured-ring graphic or ring-compatible wall construction
- optional dust FX sprite/animation
- optional light overlay(s)

All may use placeholders in the geometry pass if documented.

---

# 17. Mapper Freedom

Mapper may decide:

- exact crack and seam placement
- minor rubble distribution
- root shapes
- dust/debris texture variation
- subtle wall asymmetry caused by age
- exact 1-2 tile adjustments to event-anchor coordinates

Mapper may not alter the room's one-chamber concept, focal-ring placement, absence of exits, or narrative implications.

---

# 18. Mapper Non-Goals

Do not:

- write dialogue
- implement the cinematic commands
- assign new switches/variables
- add combat
- add treasure
- add optional interactions
- create lore text
- add NPCs
- change story order
- explain the ancient system
- build adjacent rooms

---

# 19. Acceptance Checklist

Map is ready for Eventwright handoff only if:

- [ ] `Map001.json` exists and opens correctly in MZ
- [ ] canvas is 29x21
- [ ] chamber is one compact sealed room
- [ ] fractured ring is the dominant focal point
- [ ] no living entities are placed
- [ ] no visible/player-usable exits exist
- [ ] dust, fitted stone, unfamiliar metal, seams, and dead roots are represented or documented placeholders
- [ ] map supports all four required ring visual states
- [ ] all six required event anchors exist and are named correctly
- [ ] camera framing cannot expose map edges
- [ ] map works for both `PRO-SC-001` and `PRO-SC-012`
- [ ] no forbidden dungeon/temple/loot implications were introduced
- [ ] mapper rechecked the locked Prologue style before handoff

---

# 20. Mapper Deliverables

1. `Map001.json`
2. screenshot of dormant/default chamber
3. screenshot or mock-up showing the intended lit-ring state area
4. list of placeholder assets still needing replacement
5. deviation note for any requirement not satisfied exactly

---

# Handoff

When Mapping is accepted, the package advances to:

**Mapping -> Eventwright -> Validation**

The Eventwright should not need to redesign geometry; Validation should be able to compare both map and events directly against this work order, the Bible, and the locked story source.
