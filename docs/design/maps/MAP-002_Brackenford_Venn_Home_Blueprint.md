# MAP-002 Mapper Work Order - Brackenford - Venn Home

**Bible Map ID:** `MAP-002`  
**RPG Maker Map ID:** `2`  
**Runtime file:** `Map002.json`  
**Story scope:** Prologue  
**Priority:** CORE  
**Status:** Approved for Mapping Pass 01  
**Scenes:** `PRO-SC-002 Morning at the Venn House`, `PRO-SC-011 Home, But Changed`  
**Locked story source:** `PrologueStoryv0.3`, sections P-02 and P-07  
**Character source:** `Player1Backgroundv0.2`, The Venn Household

---

# 1. Mapper Objective

Build the single-floor Venn family home as a modest, practical and clearly lived-in household that can stage both the Prologue morning introduction and the evening return.

This map establishes what **home** means to Marek before the wider story makes that word costly. It must feel as though Davren, Elira, Nessa, Marek and Latch lived here before the player arrived. The house is neither impoverished nor prosperous: the Venns repair useful things, keep ordinary routines and use their space efficiently.

The same geometry must support two states:

1. **Morning:** active household routine, field-kit preparation, family introduction and release into Brackenford.
2. **Evening:** supper and ordinary concerns, followed by Marek in bed and Latch watching north from his bedroom threshold.

# 2. Narrative Style Gate

Before mapping, re-check the cited story and character sources.

## Required

- The home is modest, busy, affectionate and repair-minded.
- Family affection is expressed through shared space, work and routine rather than sentimental display.
- The common room is the household's center.
- Davren has a small practical repair area.
- Elira can work naturally between kitchen and common room.
- Nessa has a distinct but modest personal sleeping space.
- Marek has a simple room with a bed and a place for survey preparation.
- Latch belongs naturally in the house and can wait near doors and thresholds.
- A crooked front-door latch can be noticed and corrected.
- An ordinary field kit can be checked twice before departure.
- A small borrowed calibration weight can be remembered and added to the kit without becoming inventory.
- The evening layout supports supper, the family's normal conversation and Latch guarding Marek's bedroom threshold while facing north.

## Forbidden implications

Do not add:

- wealth, grandeur or extreme poverty
- a private library, rare books or scholarly collections
- shrines, altars, magical symbols or fractured-ring imagery
- weapons displays or military trophies
- hidden rooms, secret passages or unexplained locked doors
- treasure chests, loot or collectible staging
- supernatural behavior by Latch
- visible ancient technology or ominous foreshadowing during the morning
- an additional exterior door, cellar route or upper floor
- modern appliances or objects inconsistent with Brackenford

The family must not appear to know that this day is historically important.

# 3. Player and Camera Mode

- **Morning:** short controlled family beat, then player control.
- **Evening:** player arrival followed by controlled supper and bedroom sequences.
- **Encounters:** none.
- **Looping:** none.
- **Resolution assumption:** stock MZ 816x624 at 48 px per tile.
- The camera follows Marek normally after release; controlled framing may later use the common-room and bedroom anchors.

# 4. Required Dimensions

**Canvas:** `29 x 23 tiles`

**Active house footprint:** approximately `x=4..24`, `y=2..20`.

The remaining cells are dark, impassable buffer. Do not add decorative inaccessible rooms outside the active footprint.

Coordinate convention is zero-based MZ tile coordinates: x increases rightward and y increases downward.

# 5. Spatial Recipe

## Zone A - Parents' Room

**Bounds:** approximately `x=5..10`, `y=3..8`  
**Door:** south edge near `(8,8)`

Required: modest shared bed, small storage and no luxury objects.

## Zone B - Nessa's Room

**Bounds:** approximately `x=11..15`, `y=3..8`  
**Door:** south edge near `(13,8)`

Required: single bed and one or two harmless personal details. Do not reduce Nessa's identity to childish toys.

## Zone C - Marek's Room

**Bounds:** approximately `x=16..23`, `y=3..8`  
**Door/threshold:** south edge at `(19,8)` / `(19,9)`

Required: simple bed near `(21,5)`, small survey-preparation surface or wall hook, clear floor space for the night wake sequence. The south-facing doorway must allow Latch to rest on the threshold facing north toward Marek.

## Zone D - Interior Hall

**Bounds:** approximately `x=5..23`, `y=8..10`

Required: direct access to all three sleeping rooms and the common space. Keep it narrow and functional, not ceremonial.

## Zone E - Kitchen and Household Work

**Bounds:** approximately `x=5..10`, `y=10..16`

Required: hearth/cook area, preparation surface and ordinary storage. It must connect openly to the common room so Elira remains part of family activity.

## Zone F - Common and Supper Room

**Bounds:** approximately `x=11..18`, `y=10..16`

Required: table seating for four, navigable perimeter, morning family staging and evening supper staging. This is the dominant social space, not a formal dining hall.

## Zone G - Davren's Repair Nook

**Bounds:** approximately `x=19..23`, `y=10..16`

Required: compact work surface, tools/repair clutter and an unobstructed field-kit staging point. No forge or industrial workshop.

## Zone H - Entry and Mud Area

**Bounds:** approximately `x=11..17`, `y=17..20`  
**Front door:** `(14,20)`

Required: a single exterior door, crooked-latch interaction position near `(14,19)`, room for Latch and an unobstructed route into the common room.

# 6. Layout Diagram

```text
                         NORTH

      +----------+--------+--------------+
      | Parents  | Nessa  | Marek        |
      | room     | room   | room / bed   |
      +----D-----+---D----+---D----------+
      |           interior hall          |
      +----------+-----------+-----------+
      | kitchen  | common /  | repair /  |
      | & hearth | supper    | field kit |
      +----------+-----+-----+-----------+
                       |
                  entry / mud
                       D
                     SOUTH
```

`D` indicates a doorway, not an additional transfer.

# 7. Geometry and Route Rules

- One floor and one map only.
- One exterior transfer door only, at the south entry.
- All family spaces must be connected without a maze-like route.
- Marek must be able to move from common room to front latch, repair/kit nook, Marek's room and front door without obstruction.
- The supper table must allow four NPC positions plus Marek's approach/exit route.
- The common-room camera frame centered near `(14,13)` must not expose the outer map edge.
- The bedroom camera frame centered near `(20,6)` must show Marek's bed, doorway threshold and Latch's evening position together.
- Do not create unused space merely to make the house look larger.

# 8. Tileset and Placeholder Policy

**Mapping Pass 01 fixture:** stock RPG Maker MZ `Inside` tileset, database slot 3, may be used as a documented placeholder.

The sample archive may be inspected read-only for stock MZ schema and tile behavior. It is not an editable fixture, a project base or a source of imported maps.

Pass 01 must document every required stock sheet and passage dependency. Production tileset ownership remains pending until the map proves its geometry. Do not assign a new tileset ID or copy stock runtime assets into the repository during Mapping Pass 01.

# 9. Required Environment Elements

- fitted but ordinary Brackenford interior walls and floor
- four-person supper table
- hearth/cooking area
- modest food and household storage
- Davren repair surface and tools
- Marek field-kit preparation surface/hook
- parents' bed, Nessa's bed and Marek's bed
- single front door with crooked latch staging
- Latch-appropriate floor space near entry and Marek's threshold
- restrained wear showing maintenance and repeated use

Decorative completeness is not required for the skeleton, but required functional footprints must exist.

# 10. Actors and Event Representation

Mapping Pass 01 places named **blank stubs only**. It does not implement actor graphics, dialogue, movement, switches, audio or autoruns.

Required story characters for later Eventwright work:

- `ACT-001` Marek Venn
- `NPC-001` Davren Venn
- `NPC-002` Elira Venn
- `NPC-003` Nessa Venn
- `NPC-004` Latch

# 11. Required Event Anchors

Use the exact local event IDs, names and coordinates for Pass 01 unless a collision or geometry defect requires a documented one-tile adjustment.

| Local ID | Anchor | Position | Mapping purpose |
|---:|---|---:|---|
| 1 | `EV_Story_MorningController` | `(14,13)` | `PRO-SC-002` controller |
| 2 | `EV_Story_EveningController` | `(14,13)` | `PRO-SC-011` controller |
| 3 | `EV_Spawn_Morning` | `(14,14)` | entry from MAP-001/title sequence |
| 4 | `EV_Spawn_Evening` | `(14,19)` | return from Brackenford |
| 5 | `EV_NPC_Davren` | `(21,13)` | repair-nook staging |
| 6 | `EV_NPC_Elira` | `(7,13)` | kitchen/common staging |
| 7 | `EV_NPC_Nessa` | `(13,12)` | common-room staging |
| 8 | `EV_NPC_Latch_Morning` | `(13,18)` | entry-area staging |
| 9 | `EV_NPC_Latch_EveningThreshold` | `(19,9)` | night threshold, facing north |
| 10 | `EV_Prop_CrookedLatch` | `(14,19)` | Marek's small correction beat |
| 11 | `EV_Prop_FieldKit` | `(21,12)` | double-check field kit |
| 12 | `EV_Prop_CalibrationWeight` | `(22,12)` | remembered small obligation |
| 13 | `EV_Prop_SupperTable` | `(14,12)` | evening family staging reference |
| 14 | `EV_Prop_MarekBed` | `(21,5)` | night wake sequence |
| 15 | `EV_Transfer_Brackenford` | `(14,20)` | sole exterior transfer anchor |
| 16 | `EV_Camera_CommonRoom` | `(14,13)` | morning/evening family frame |
| 17 | `EV_Camera_MarekRoom` | `(20,6)` | bed and threshold frame |

Overlapping anchors are allowed because they are non-executing registration stubs in this pass.

Each stub has one blank unconditional action-button page, no graphic, no autonomous movement, Through ON, Below Characters priority and only the terminating event command. Mapping must not add executable story logic.

# 12. State Dependencies

The map must support, but the Mapper does not program:

## Morning entry and output

- Entry: `VR-0001 SYS_StoryStage = 1002`
- Prior state: `SW-0101 PRO_WatcherStation_Awakened = ON`
- Output: `SW-0102 PRO_VennHome_Intro_Complete = ON`
- Exit stage: `VR-0001 SYS_StoryStage = 1003`

## Evening entry and output

- Entry: `VR-0001 SYS_StoryStage = 1011`
- Prior state: `SW-0110 PRO_Report_Complete = ON`
- Output: `SW-0111 PRO_HomeEvening_Complete = ON`
- Exit stage: `VR-0001 SYS_StoryStage = 1012`

Minor optional household interactions must use local state when Eventwright work begins.

# 13. Transfer and Spawn Contract

- MAP-001 opening transfers into MAP-002 at the morning spawn `(14,14)`, facing up, under controlled fade. Eventwright owns the actual transfer.
- The south door `(14,20)` is the only normal transfer to `MAP-003 Brackenford`.
- MAP-003 destination coordinates remain unresolved until the MAP-003 blueprint exists. Mapping places the anchor but no transfer command.
- Evening return uses `(14,19)`, facing up.
- `PRO-SC-011` exits under cinematic control toward `PRO-SC-012`; no visible second doorway is required.

# 14. Passability and Collision

- Outer buffer is fully impassable.
- Walls, furniture, counters, hearth and beds block movement as their stock passage rules require.
- Door thresholds and all mandatory routes must remain passable.
- The common table must not trap any staged character.
- No damage floors, ladders, bush terrain, counter interactions or gameplay regions are required in Pass 01.
- All region cells remain zero.

# 15. Morning Spatial Beats Supported

Mapping must provide positions/routes for the later Eventwright to stage:

1. ordinary family activity in the common room
2. Latch impatient near the front door
3. Marek notices and straightens the crooked latch
4. Marek checks his ordinary field kit twice
5. Marek remembers Joren's borrowed calibration weight and adds it to the kit
6. player control begins
7. player leaves through the south door for the survey office

The calibration weight is a scene prop, not an inventory/database item.

# 16. Evening Spatial Beats Supported

Mapping must provide positions/routes for:

1. Marek and muddy Latch enter from Brackenford
2. Nessa asks why Latch is muddy
3. Davren and Elira discuss ordinary household concerns
4. four-person supper staging
5. transition to Marek asleep in his room
6. Latch rests at `(19,9)`, facing north toward Marek, and refuses to enter
7. Marek wakes after believing he heard three distant notes
8. the notes do not repeat
9. controlled transition to `PRO-SC-012`

Morning and evening must use the same physical house. Lighting and character positions are downstream Eventwright/Asset responsibilities.

# 17. Mapper Freedom

The Mapper may decide:

- exact ordinary floor/wall tile variation
- small furniture adjustments within zone bounds
- harmless cookware, baskets, linens and repair clutter
- minor wear and asymmetry consistent with a maintained home
- one-tile anchor adjustments when required for passability, if documented

The Mapper may propose but not implement a different canvas, additional floor, extra exit or materially different room arrangement.

# 18. Mapper Non-Goals

Do not:

- write dialogue or movement routes
- add autorun/parallel events
- assign or change global state
- create items, quests, shops, treasure or combat
- choose final character graphics
- create the MAP-003 destination
- add supernatural or ancient-system presentation
- turn the home into a showcase interior that contradicts its modest function

# 19. Mapping Pass 01 Acceptance Checklist

- [ ] `Map002.json` exists and opens in RPG Maker MZ.
- [ ] Canvas is 29x23 with no looping, encounters, autoplay or parallax.
- [ ] The active one-floor footprint stays within `x=4..24`, `y=2..20`.
- [ ] Three sleeping spaces, hall, kitchen, common room, repair nook and south entry exist.
- [ ] There is one exterior door and no hidden/additional route.
- [ ] Required morning and evening routes are passable.
- [ ] Common-room and Marek-room camera frames do not expose map edges.
- [ ] The bed and threshold are visible together in the bedroom frame.
- [ ] Table staging supports four family positions without trapping movement.
- [ ] All 17 exact named stubs exist with blank Mapper-safe pages.
- [ ] No unauthorized story logic or canon implication is present.
- [ ] Stock Inside placeholder dependencies and deviations are documented.
- [ ] The locked Prologue and Marek background were rechecked for style.

# 20. Mapper Deliverables

1. `work/mapping/MAP-002/pass-01/Map002.json`
2. full-map composite
3. common-room 816x624 camera composite
4. Marek-bedroom 816x624 camera composite
5. tile/dependency manifest
6. Mapping handoff/deviation report
7. repeatable build and validation scripts

# 21. Foreman Authorization

**Authorized production unit:** MAP-002 Mapping skeleton Pass 01 only.

The Mapper owns geometry, collision and named blank anchors. The Eventwright must not begin until independent Validation accepts the Mapping handoff. Asset polish, character graphics, dialogue, state logic, transfers and presentation are downstream.

`EryndraStory.zip` and `SampleGenerated.zip` remain immutable. They may be read or temporarily extracted for inspection, but no file inside either archive or extracted reference project may be altered.

