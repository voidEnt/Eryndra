# Eryndra

Eryndra is an RPG Maker MZ project built from a locked story canon and a living implementation Bible.

## Source-of-truth hierarchy

1. **Story canon** — the locked narrative source material.
2. **Implementation Bible** — the authoritative design and translation layer for converting story canon into RPG Maker MZ structures.
3. **RPG Maker project** — the current executable implementation state.

If the Bible and the RPG Maker project disagree, the discrepancy must be reviewed and resolved rather than silently accepted.

## Current production objective

Build the **Prologue as a complete vertical slice** containing the core story spine: required maps, actors, events, switches, variables, battles, dialogue, transitions, and supporting systems. Optional side quests, lore books, decorative content, hidden content, and other nonessential material are intentionally deferred until the core story spine is working.

## Repository layout

- `docs/bible/` — living implementation Bible, master index, and change log.
- `docs/story-reference/` — story-reference material when added.
- `docs/design/` — supporting design notes and system specifications.
- `game/` — RPG Maker MZ project files when added.
- `tools/` — utilities and validation scripts when needed.
- `tests/` — test plans, validation data, and regression references.
- `archive/` — retired or superseded development material that must remain available for traceability.

## Production classifications

Every implementation entry should use one production priority:

- **CORE** — required to complete the main story spine.
- **SUPPORT** — required for CORE content to function properly.
- **DEFERRED** — optional content intentionally postponed.

Every implementation entry should use one status:

`Concept → Defined → Assigned → Implemented → Tested → Locked`
