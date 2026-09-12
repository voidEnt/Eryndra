# MAP-003 Mapper Work Order — Brackenford

**Bible Map ID:** `MAP-003`  
**MZ Map ID / runtime filename:** `3` / `Map003.json`  
**Priority/status:** CORE / approved spatial work order; Mapping Pass 01 not yet submitted  
**Scenes:** `PRO-SC-003` Brackenford Morning; `PRO-SC-005` Leaving Brackenford; `PRO-SC-010` The Report  
**Narrative references:** locked `PrologueStoryv0.3` P-02, P-03 and P-07; `Player1Backgroundv0.2` (Life Before the Story, Latch, Edrin and Joren)  
**Implementation references:** Bible and Production Roles & Handoff Contract; `Prologue_Implementation_Decomposition.md`; accepted MAP-002 Mapping Pass 01 and Eventwright candidate  
**Map tree:** parent/location map for `MAP-002` Venn Home and `MAP-004` Survey Office; `MAP-005` Northern Road connects at the northern boundary. Neither parent linkage nor transfers are Eventwright-authorized in Mapping Pass 01.

## 1. Narrative purpose and style gate

Build Marek's modest, familiar Aurelian town. The first outdoor play space should read as a place of work, family, repaired things and ordinary travel: several short lived-in lanes, the Venn home, a plain survey office and a road out of town. It must serve an unhurried morning, a routine work departure and an unchanged-looking late-afternoon return without needing three separate town maps.

Before constructing tiles, compare this plan to all three cited Prologue sections. P-03 contains distant *ordinary* uncertainty (supplies, travelers, soldiers, proclamations); do not visualize a recognized ancient crisis. P-07 requires Brackenford to look as Marek left it. Do not introduce ring/fracture symbolism, magical light, ominous ruin masonry, a battle encounter, an emergency evacuation, conspicuous military occupation, a grand capital plaza or a large church/palace. The locked story specifies no detailed street plan; the coordinate scheme below is an implementation choice, not a new historical fact.

## 2. Player and camera

Top-down walking and optional observation; no forced camera pan required for the Mapping pass. Base MZ tile 48 px, default 816×624 viewport approximately 17×13 tiles. Nonlooping town `45×35` tiles. The main route from home to office and the northern road must scroll without exposing blank canvas, and have no required diagonal movement. Keep approximately two tile widths clear on the principal lane and around each destination so later NPCs/Latch do not obstruct it. The player controls Marek throughout `PRO-SC-003` except for separately authored event moments.

## 3. Zone plan and spatial recipe

Coordinates are zero-based MZ `(x,y)`; anchor coordinates below are exact for Pass 01. Zone bounds may shift *only inside their envelopes* without moving named anchor cells. Impassable background/roofing can occupy the map perimeter; never rely on an empty black border as an implied exit.

| Zone | Envelope | Required construction and adjacency |
|---|---|---|
| Venn frontage | `x=7..16, y=18..27` | One modest house facade near `(11,24)`; readable south-facing doorway `(11,25)` and clear outdoor arrival `(11,26)`. This is the **only** active Venn doorway. Do not reveal or duplicate MAP-002's interior. |
| Central work lane | `x=10..24, y=17..28` | Wear-marked north/south and east/west walking lanes, readable 2-tile clear route from `(11,26)` via `(22,26)` to `(22,17)`. Drainage, repaired fencing and ordinary road markings may support Marek's surveyor perspective. |
| Survey-office spur | `x=22..36, y=8..19` | Simple municipal/workplace facade at `x=27..36, y=8..14`; doorway `(31,15)`, outside approach `(31,16)`. Walkable east/west spur from `(22,17)` toward the office; no pomp or secret archive. |
| Northern approach | `x=19..26, y=2..18` | Maintained road from the central lane to the north exit `(22,4)`; clear northern arrival `(22,6)`. The exit should look like an ordinary surveyed road, not a dungeon/ruin or city gate under siege. |
| Community backdrop | west `x=4..16, y=6..16`; east `x=34..42, y=19..29` | A few small, distinct occupied-looking facades, fences, cart/wood-storage or laundry-like neutral work details; no functional interior doors, merchants, rewards, or named landmarks. Set dressing may imply more town beyond the camera but cannot imply an explorable exit. |
| Boundary and buffer | full outer band, mainly `x=0..3`, `x=42..44`, `y=0..2`, `y=32..34` | Visually intentional impassable architecture/land/vegetation. North road only is the eventual world exit; other edges must be sealed. |

These envelopes intentionally overlap at their walking links. Priority is traversability and correct anchor placement, not perfectly rectangular blocks. Do not copy another project's town layout wholesale.

## 4. Required routes and entrances

- Home outside spawn `(11,26)`, facing south; one clear tile immediately in front and a north-facing interaction/entry cell `(11,25)`. MAP-002 south doorway is event ID 15 near `(14,20)`; its eventual output into this map uses `(11,26)`. Mapping must **not** edit MAP-002.
- Survey office outside spawn `(31,16)`, facing south; entry hotspot `(31,15)` facing north. `MAP-004` is not yet mapped, so this is an inert spatial anchor, not a live transfer.
- North-road exit hotspot `(22,4)` approached from `(22,5)`; return from MAP-005 eventually spawns `(22,6)`, facing south. Keep the approach passable from both directions. On first morning, Eventwright must gate departure until after Joren's assignment (`SW-0103`, stage `1005`); the mapper only reserves the gate footprint.
- `PRO-SC-010` returns through the same north-road arrival, then crosses the same routes to the survey office and eventually home. No duplicate evening-only door or alternate north entrance.
- Straight and branch routes between home, office and north road must remain passable for a player with no collision-avoidance tricks; leave side pockets for optional stationary townspeople.

## 5. Tiles, lighting and reuse

Pass 01 may use MZ's stock `Outside` tileset **MZ tileset ID 2** as inspected read-only from the sample. Use ordinary earth, stone or beaten-lane surfaces, modest roof/fence/woodwork and restrained vegetation. Exact individual stock tile IDs and any future dedicated Eryndra tileset must be recorded in the Mapper's asset/dependency report. Neither the sample ZIP nor its project/database/IDs may be modified or incorporated as Eryndra canon.

Morning is the base geometry. Afternoon return reuses the exact same tile grid; Eventwright may change lighting/tint and NPC pages later, but Mapping must not imply destruction or a new building. Avoid perpetual evening-specific lighting painted into ground tiles. Keep roofs/objects from visually covering the three required arrival cells in both time states. No parallax, plugin or new bespoke artwork is required for the skeleton.

## 6. Characters and event anchor stubs

Marek is the playable actor, not a duplicated stationary town NPC. Latch is an ordinary one-eared dog: reserve his appearance near the northern-road departure when stage `1005` begins, so he can follow Marek out despite no invitation; do not imply he has been following Marek during the initial town-morning exploration. Joren and Edrin's assignment conversation belongs at MAP-004 unless a later Eventwright work order explicitly stages Edrin outside. Up to two anonymous background-townsperson placeholder stubs can show the town is inhabited; dialogue, occupations and identities remain unassigned.

All named events below must exist, be inert in Mapping Pass 01, have exact IDs/names/cells, and use no global writes, text or executable transfer. Each may consist of one stock empty event page with a comment noting its intended later owner. Blank markers must be visually nonblocking; character-graphic decisions belong to a later authorized pass.

| Local event ID | Event name | `(x,y)` | Later owner / purpose |
|---:|---|---|---|
| 1 | `EV_Transfer_VennHome` | `(11,25)` | Eventwright: guarded entry to MAP-002. |
| 2 | `EV_Transfer_SurveyOffice` | `(31,15)` | Eventwright: guarded entry to MAP-004. |
| 3 | `EV_Transfer_NorthernRoad` | `(22,4)` | Eventwright: assignment-gated MAP-005 departure and return. |
| 4 | `EV_Story_TownMorning` | `(12,27)` | Eventwright: morning arrival/optional framing at stage `1003`. |
| 5 | `EV_Story_TownDeparture` | `(22,7)` | Eventwright: `PRO-SC-005` town-side departure staging. |
| 6 | `EV_Story_TownReturn` | `(23,7)` | Eventwright: `PRO-SC-010` homeward arrival staging. |
| 7 | `EV_NPC_Latch_Departure` | `(21,8)` | Eventwright: stage-dependent ordinary Latch appearance at the northern-road departure. |
| 8 | `EV_NPC_Townsperson_West` | `(16,22)` | Optional background presence; no dialogue in Mapping. |
| 9 | `EV_NPC_Townsperson_East` | `(28,18)` | Optional background presence; no dialogue in Mapping. |
| 10 | `EV_Visual_RoadMarker` | `(22,12)` | Ordinary surveyed-road landmark, noninteractive in Mapping. |

Do not allocate more local IDs without documenting why. None of the three outside spawn cells `(11,26)`, `(31,16)`, `(22,6)` may be occupied by an event anchor; MZ editor placement and transfers need these cells clear. Add no named residents, shops, treasure, lore signs, encounter events or new global state.

## 7. State and presentation dependencies (not Mapper commands)

| Input or result | Scope of this map |
|---|---|
| `VR-0001 / SYS_StoryStage = 1003` and `SW-0102 = ON` | MAP-002 Morning is complete; town becomes Marek's free-exploration stage. MAP-002's existing south door is still a nonfunctional hook until an authorized Eventwright integration pass. |
| `SW-0103 = ON`, `VR-0001 = 1005` | Assignment complete in MAP-004; northern-road departure and visible Latch become eligible. Town geometry supports the gate, but Mapping does not set it. |
| `VR-0001 = 1010` | Return from the north; Brackenford remains spatially normal and survey office is reachable. |
| `SW-0110 = ON`, `VR-0001 = 1011` | Evening Venn Home is handled inside MAP-002 after Joren's report; no duplicate indoor event here. |

No new switch/variable/self-switch/common event is assigned by this work order. Audio is ordinary town ambience if later specified; **no** three-note cue, ancient-network motif, alarm, battle music or supernatural screen effect in the town-morning Mapping pass. All exact dialogue and transfer commands await Eventwright approval.

## 8. Mapper freedom, constraints and acceptance

Mapper may choose subtle house silhouette variation, fences, nonfunctional carts, modest civic details, road-wear and drains within zone envelopes. Mark proposed exceptions before implementation. The priority is a legible first walking loop, not decorative density.

Pass 01 acceptance requires: `45×35`, nonlooping MZ map ID 3; stock Outside tileset ID 2 (or a documented work-order correction before build); the three entrances and route network at exact cells; 10 inert anchors at exact IDs/names/cells; no unintended transfers or global writes; ordinary morning style with credible unchanged afternoon reuse; stock-passability and no unintended off-map exits; MZ loads the map; and review views for home frontage, office approach, north gate and overall geometry. Mapper self-check cannot substitute for independent Validation.

Deliver to `work/mapping/MAP-003/pass-01/`: `Map003.json`, deterministic builder if generated, tile/dependency manifest, screenshots or equivalent full-map and route views, mapper handoff/deviation report and static validation evidence. A separate Validator checks Mapping acceptance before any MAP-003 Eventwright work. Runtime linkage to MAP-002/MAP-004/MAP-005 remains conditional until those transfers are explicitly authorized and implemented.
