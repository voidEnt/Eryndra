# Eryndra Map Work Order Standard

**Purpose:** Define the handoff format for every RPG Maker MZ map so a mapper follows a recipe rather than improvising story implementation.

## Production Principle

A map work order is a **build blueprint**, not a creative prompt. The mapper must be able to determine the map's required size, geometry, staging, assets, event anchor locations, passability, and narrative tone before opening RPG Maker MZ.

The mapper is responsible for **spatial implementation**. The mapper is not responsible for inventing story beats, changing canon, balancing combat, writing dialogue, or designing event logic beyond the anchor/stub requirements explicitly listed in the work order.

A later event work order may convert the anchors into full event commands.

---

# Required Preflight

Before mapping begins, the mapper must read:

1. The map's entry in `Master_Implementation_Index.md`.
2. The relevant scene specification(s) in the implementation decomposition.
3. The cited section(s) of the locked story source.
4. Any applicable Bible rules for characters, world state, assets, switches, or presentation.

The mapper must perform a **Narrative Style Gate** before generation. If the requested map concept conflicts with the locked story's tone, scale, geography, or canon, mapping stops and the discrepancy is returned for resolution.

---

# Work Order Fields

Every map blueprint should contain the following sections.

## 1. Work Order Identity

- Bible Map ID
- RPG Maker Map ID / filename
- Map name
- Story scope
- Priority
- Status
- Story scenes using the map
- Story source sections
- Parent map, if any

## 2. Narrative Function

A short statement explaining **why this map exists in the story** and what the audience/player must understand or feel while using it.

Include:

- Theme or emotional target
- Core story outcome
- Information the map may reveal
- Information the map must conceal

## 3. Narrative Style Gate

A mapper-facing checklist derived directly from the locked story.

Include:

- Required visual characteristics
- Required atmosphere
- Forbidden visual implications
- Canon locks
- Reuse requirements for later scenes

The mapper must confirm this section before construction.

## 4. Player / Camera Mode

- Player control: yes/no/partial
- Camera mode
- Expected visible footprint
- Scrolling requirements
- Whether the map is exploratory, cinematic, transitional, combat, puzzle, or mixed

## 5. Map Scale and Dimensions

Specify:

- Exact or target canvas width/height in MZ tiles
- Native tile size assumption
- Visible camera footprint assumption
- Active playable/staging footprint
- Required buffer areas
- Whether looping is permitted

If dimensions are flexible, provide a permitted range and the reason.

## 6. Spatial Zones

Break the map into named zones.

For each zone provide:

- Approximate tile bounds or relative placement
- Function
- Required features
- Required adjacency
- Whether player-accessible

## 7. Geometry and Composition Rules

Specify:

- Walls/floors/terrain
- Entrances/exits
- Elevation cues
- Corridors/rooms
- Sightlines
- Focal points
- Camera composition
- Required negative space

This should be enough to prevent the mapper from inventing a different spatial concept.

## 8. Tileset and Environmental Requirements

Include:

- Required tileset family / Bible tileset ID if assigned
- Placeholder policy
- Architecture/material vocabulary
- Terrain/vegetation/prop requirements
- Forbidden stock-looking elements if they would contradict canon

## 9. Lighting and Visual States

Specify all states the map must support, especially when reused.

Examples:

- day/night
- intact/damaged
- dormant/activated
- pre-event/post-event
- weather variants

The mapper must leave visual and event-layer capacity for each required state.

## 10. Actors, NPCs, and Sprites

List every required visible character or explicitly state that none are present.

Include staging needs such as:

- standing locations
- movement lanes
- crowd capacity
- companion pathing
- battle formation space

## 11. Event Anchor Plan

The mapper does not need to implement full event logic unless assigned separately, but must place and name required anchor/stub events.

For each anchor include:

- Event name
- Bible event ID if assigned
- Approximate coordinates
- Trigger purpose
- Downstream eventer's intended use

Examples: story controller, transfer point, interaction hotspot, camera anchor, environmental effect anchor.

## 12. State Dependencies

List relevant:

- switches
- variables
- self-switch expectations
- common events
- story-stage values

This tells the mapper which alternate map states or event pages must have spatial support.

## 13. Transfers and Spawn Points

Define:

- incoming transfer locations
- outgoing transfer locations
- player facing direction
- cinematic spawn locations
- disabled or hidden exits

No transfer should be invented without the work order.

## 14. Passability, Regions, and Collision

Define:

- inaccessible areas
- edge sealing
- counters/ladders/damage terrain if any
- region IDs if required
- path widths
- companion movement requirements

## 15. Audio / Presentation Dependencies

List music, ambience, sound cues, screen tint, pictures, animations, weather, overlays, or other presentation elements that influence spatial design.

The mapper does not need to author these assets, but must preserve room for their presentation.

## 16. Asset Dependencies

List all required map-specific assets and whether each may use a placeholder.

Examples:

- tileset sheets
- parallax
- character sprites
- object sprites
- animated props
- story pictures
- lighting overlays

## 17. Mapper Freedom

Explicitly state what the mapper **may** decide, such as minor decorative placement, crack patterns, rubble distribution, or prop variation.

Anything not listed as mapper freedom should be treated as constrained by the blueprint and Bible.

## 18. Mapper Non-Goals

Explicitly state what is outside the mapper's assignment.

Typical non-goals:

- writing dialogue
- changing story order
- inventing NPCs
- creating side quests
- adding treasure
- adding combat encounters
- assigning new global switches
- altering canon geography

## 19. Acceptance Checklist

Objective conditions that must be true before the map is accepted.

At minimum verify:

- dimensions
- tileset
- required zones
- required anchors
- passability
- transfers
- story-style compliance
- required visual states
- no unintended content
- map opens correctly in MZ

## 20. Mapper Deliverables

Normally:

- completed `Map###.json`
- any newly required tileset/asset dependency list
- screenshot(s) showing the completed map and major states
- short deviation note if any blueprint requirement could not be satisfied

---

# Handoff Chain

Preferred production chain:

`Locked Story -> Bible -> Map Blueprint -> Mapper -> Event Work Order -> Event Implementation -> Asset Pass -> QA`

A downstream worker should not need to reinterpret the locked story from scratch. The blueprint should carry forward the decisions already made while still citing the story source for verification.
