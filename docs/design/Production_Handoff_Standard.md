# Eryndra Production Handoff Standard

The canonical implementation chain is:

**Mapping -> Eventwright -> Validation**

All three stages work from the locked story, Implementation Bible, and the applicable work order. Each stage has a separate responsibility so creative decisions are made upstream rather than improvised during implementation.

## 1. Mapping

The Mapper receives a map work order and builds the spatial substrate.

Primary responsibilities:

- map dimensions
- geometry and composition
- tileset use
- environmental layout
- passability/collision
- transfer/spawn locations defined by the blueprint
- event anchor/stub placement
- camera/staging space
- support for required visual states

The Mapper does **not** invent dialogue, story logic, new quests, new global state, combat, treasure, or canon.

Primary deliverable: `Map###.json` plus documented placeholder/deviation notes.

## 2. Eventwright

The Eventwright receives an accepted map plus an event work order and turns the spatial anchors into executable RPG Maker MZ story logic.

Primary responsibilities:

- event pages
- triggers
- autoruns/parallel events where specified
- dialogue commands
- movement routes
- switches and variables already assigned by the Bible/work order
- self-switches/local state
- transfers
- audio/visual cues
- conditional branches
- common-event calls
- scene entry/exit state

The Eventwright does **not** redesign the map, invent new story beats, create new persistent global state without Bible assignment, or reinterpret canon.

Primary deliverable: executable event logic using the approved map and assigned IDs.

## 3. Validation

Validation checks the combined map and event implementation against all upstream requirements.

Validation references:

1. locked story source
2. Implementation Bible
3. map work order
4. event work order
5. RPG Maker MZ project state

Primary checks:

- story beat completeness
- canon/style compliance
- geometry and map requirements
- event-anchor use
- correct switches/variables/IDs
- correct scene-state transitions
- transfer correctness
- passability and soft-lock checks
- dialogue/cinematic sequencing
- save/load persistence
- absence of unauthorized additions
- JSON integrity and MZ loadability

Validation does not silently repair design discrepancies. Failed requirements are returned to the responsible stage with a specific correction request.

## Handoff Rule

A stage should not require the downstream worker to reinterpret the narrative from scratch.

The intended information flow is:

`Locked Story + Bible -> Blueprint/Work Order -> Implementation -> Validation`

For maps specifically:

`Map Blueprint -> Mapping -> Event Work Order -> Eventwright -> Validation`

Only after Validation passes should the implementation be treated as ready for the next production unit.
