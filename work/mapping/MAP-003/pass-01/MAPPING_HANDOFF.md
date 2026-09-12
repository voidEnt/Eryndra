# MAP-003 Mapping Pass 01 Handoff — Awaiting Independent Validation

## Assignment and output

The Foreman's approved Brackenford blueprint calls for one reusable outdoor stage covering free morning exploration, the northbound departure and the later normal-looking return. The Mapper produced the original `Map003.json` at 45×35 with 10 exact blank named anchors and stock Outside tile set 2. All event pages contain only the terminating command, so there are no active transfers, switches, conversations, shops or encounters.

`Map003.json` SHA-256: `b6a8babbcd8790b8c1a29f64540e116c2aad48dede54092b6b9418f33964d64c`.

## Narrative style and spatial acceptance evidence

- Read locked P-02/P-03/P-07 and the Marek/Latch/Joren/Edrin character guidance before mapping; no ancient-ring art, named additional NPCs, recognized ancient crisis, occupation, treasure or combat was introduced.
- Base morning terrain and facades remain reusable unchanged after Marek returns; no baked-in night/damage state.
- The Venn house is west-south at `(11,25)`, the office is northeast at `(31,15)`, and the maintained road leaves north at `(22,4)`. Entry spawn cells `(11,26)`, `(31,16)` and `(22,6)` have no overlapping event anchor.
- A connected walkable road carries Marek from home to office and north road. Main paths maintain a two-cell band. The northern roadway is the only unsealed visual approach at the perimeter.
- Review composites show a complete overall map and the three principal camera locations at 816×624. Warm timber facades and everyday lanes establish the ordinary-town skeleton. Independent visual style acceptance is still required.
- Mapper's deterministic JSON/schema/collision checks: 14/14 PASS; this is **self-check evidence only**.

## Deliberately incomplete or deferred

- The office and home doorways are spatial openings, without door graphics or active triggers. Eventwright (or approved asset integration) must select a graphic/trigger that does not block the walkable transfer cell. Stock door B tiles are impassable and were intentionally *not* placed over these cells.
- Facades are blockout-scale and the green backdrop is sparse. Mapping refinement may add fences, practical clutter and vegetation **within** the blueprint, provided routes, spawns, style and IDs remain intact.
- Townspeople and Latch are inert invisible stubs; no Latch follower handling or NPC dialogue yet.
- `MAP-002` exit event 15 is untouched. `MAP-004` and `MAP-005` are not built; there is no authorized live transfer to invent.
- MAP-003 is not wired into the cumulative review project's `MapInfos.json`, starting position, switches or audio. That integration is a later Eventwright/technical package after Validation.
- Preview-only renderer reuses the existing MAP-002 builder's stock MZ tile-rendering table, but MAP-003's JSON build is self-contained. The sample project contributed no map layout, NPCs, database IDs or story content.

## Next gate

A separate Validator should verify exact anchors, actual MZ passage (including door approach), tone, camera crops, no unauthorized logic, build determinism, input immutability and all three temporal uses. If a route or facade fails, send it to Mapping; if the blueprint itself is contradictory, send it to Foreman. Only after Mapping PASS should Eventwright specify dialogue, staging and cross-map transfer hooks.
