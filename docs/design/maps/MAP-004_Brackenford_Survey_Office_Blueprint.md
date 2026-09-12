# MAP-004 Mapper Work Order — Brackenford Survey Office

**Bible Map ID / MZ map ID:** `MAP-004` / 4 (`Map004.json`)  
**Priority / stage:** CORE / approved spatial work order; Mapping Pass 01  
**Scenes:** `PRO-SC-004` The Survey Assignment; `PRO-SC-010` The Report  
**Canon gate:** locked `PrologueStoryv0.3` P-03 and P-07; `Player1Backgroundv0.2` (Joren Pell and Edrin Holt)  
**Dependencies:** Bible roles/handoffs and Prologue MZ ID assignments; `docs/design/maps/MAP-003_Brackenford_Blueprint.md` and accepted MAP-003 Mapping Pass 02. The MAP-003 office door is presently an inert hook, not a working transfer.

## Narrative and scope

Make one unpretentious working survey office, reused without physical changes for the morning assignment and late-afternoon report. Joren keeps ordinary road and boundary records here; Marek is a junior surveyor accustomed to this room. Edrin, Marek's friend and Road Warden, can stand nearby for their familiar exchange. On return the room looks unchanged. Joren takes a professional report seriously, without panic; Edrin has only mundane news. Stage no ancient-network revelation here.

Before touching the grid, read both cited Prologue sections. The assignment concerns old road/boundary marks and a ledger correction; the later report concerns undocumented masonry and possible road risk. These facts call for ordinary records, measurements and work surfaces, **not** a fantastical cartography lab, crypt, temple, military command room, identified ancient site, ominous ring, secret archive, loot or adventure-board quests. Paper and maps may be visually generic; the mapper must not invent legible survey data, names or prophetic diagrams.

Mapping owns tiles, passability, event-anchor footprints and stock-asset reporting. It does not author conversation, new world facts, switches, screen effects, NPC pages, or transfers. Marek is the player actor; do not duplicate him as a stationary event. Latch's departure placement is on MAP-003 near the northern road, not inside this office.

## Grid and geometry

MZ coordinates are zero-based `(x,y)`; canvas **25×19**, 48px tiles, nonlooping; default camera 816×624 (about 17×13 tiles). Single ground-floor room, interior footprint roughly `x=3..21, y=2..16`. Dark buffer around the room must be visibly intentional and impassable. No other room, basement, upstairs, alternate door or exit.

| Zone | Envelope | Required structure |
|---|---|---|
| Working back wall | `x=4..20, y=3..8` | Plain plaster/timber or ordinary masonry wall; modest generic record storage and a nonlegible wall chart. Leave Joren's anchor `(16,8)` visible with clear interaction from below. |
| Joren's records desk | `x=14..19, y=8..11` | Ordinary desk/counter and ledger surface at `(16,9)`; front viewing position `(16,11)` and clear west-side approach to stand at `(15,8)` beside Joren. No sealed ceremonial dais. |
| Shared work floor | `x=6..18, y=10..15` | Clear two-tile walking lane from door to desk and Edrin; Marek dialogue staging `(12,12)` stays clear. Optional modest measuring rods and supplies at the perimeter only. |
| Edrin side position | `x=7..11, y=9..13` | Edrin anchor `(9,11)` has sight of desk and Marek, without blocking entrance or desk approach. |
| Front entry | `x=10..14, y=14..17` | Only entry hotspot `(12,16)`; **interior arrival `(12,15)` is a separate, unoccupied, walkable tile**, facing north. Passable aisle to the desk. Do not place a blocking graphic over it. |

This layout is an implementation choice, not a newly established canon floorplan. Furniture can shift within the zone envelopes while keeping every named anchor, doorway, player arrival and required route exact. Preserve enough camera-safe negative space for morning and afternoon dialogue windows. Reuse this identical grid for both time states; Eventwright may apply appropriate presentation later.

## Connection and event-anchor contract

MAP-003's exterior office doorway is event ID 2 at `(31,15)` with outside arrival `(31,16)` facing south. Its later Eventwright transfer should deliver to MAP-004 `(12,15)` facing north. The MAP-004 doorway event ID 5 at `(12,16)` should later deliver to MAP-003 `(31,16)` facing south. Neither is a live transfer in Mapping. The exterior/interior arrival cells must remain clear even when events later gain pages.

All local anchors below must have exact ID, name and coordinate. In Mapping Pass 01 use one inert, blank, visually nonblocking MZ event page per anchor (`priorityType=0`, `through=true`, empty commands). No overlap with the player arrival. A schematic camera marker is not a second NPC.

| ID | Name | `(x,y)` | Eventwright use, not Mapper instructions |
|---:|---|---|---|
| 1 | `EV_Story_SurveyAssignment` | `(5,5)` | Morning scene `PRO-SC-004`. |
| 2 | `EV_Story_SurveyReport` | `(6,5)` | Afternoon report `PRO-SC-010`. |
| 3 | `EV_NPC_Joren` | `(16,8)` | Joren's ordinary work position. |
| 4 | `EV_NPC_Edrin` | `(9,11)` | Friend/warden's ordinary conversation staging. |
| 5 | `EV_Transfer_Brackenford` | `(12,16)` | Single return door; player arrival remains `(12,15)`. |
| 6 | `EV_Prop_SurveyLedger` | `(16,9)` | Generic ledger on work surface; no text or item pickup in Mapping. |
| 7 | `EV_Visual_RecordStorage` | `(19,7)` | Ordinary records only. |
| 8 | `EV_Camera_WorkFloor` | `(12,10)` | Nonphysical scene-framing marker. |

Do not add background NPCs, functional prop events, extra doors, global flags or named objects without Foreman approval. Record decorative tiles in the manifest, not as events.

## State and script dependencies — Eventwright only

| State | Required later behavior |
|---|---|
| Enter from town after `PRO-SC-003` | Eventwright advances `VR-0001 / SYS_StoryStage` from `1003` to `1004` exactly once on eligible morning entry; no dialogue authored in Mapping. |
| Finish morning `PRO-SC-004` | Set existing `SW-0103 / PRO_Survey_Assignment_Received` and `VR-0001=1005`; permit return to town and then north-road departure. No departure before assignment. |
| Afternoon after return north, `VR-0001=1010` | Reuse room for Marek's professional report and Edrin's mundane return. |
| Finish `PRO-SC-010` | Set existing `SW-0110 / PRO_Report_Complete` and `VR-0001=1011`; permit ordinary return home. No replay of either scripted scene on revisits or reload. |

Do not allocate new switches, variables, common events, quest rewards or items here. Exact dialogue must follow the canon and its separate Eventwright work order, with text wrapping verified in MZ. No combat, random encounters, three-note cue, ancient glowing rings, shakes, supernatural light, alarms or ominous music in the office.

## Stock dependencies and gate

Mapping Pass 01 may use stock MZ **Inside tileset ID 3** for regular floors, walls, furniture and blank record-like details. The read-only `SampleGenerated.zip` may be consulted for engine schema and stock tile-sheet previews only. Do not alter either ZIP, borrow its map layouts, or copy its game/database into Eryndra. Record tile IDs, stock image names, preview assumptions and any known ambiguity in the dependency manifest. Deliver map JSON to `work/mapping/MAP-004/pass-01/`, not to the sample project or a new standalone game.

Mapping acceptance: 25×19 map, tileset 3, one sealed working room, clear walk from `(12,15)` to front desk `(16,11)`, Joren-side `(15,8)`, and Edrin `(9,11)`; recognizable ordinary records; eight exact inert anchor IDs/names/cells; no events on arrivals, scripted commands, live transfers, or new global state; same intact office usable in both scenes; full-map and entrance/desk review views; machine-readable self-check and handoff/dependency notes. A **separate Validator** must approve Mapping before Eventwright receives this map. MZ runtime appearance and story dialogue remain separate gates after that static review.
