# MAP-004 Eventwright Dependency and Deviation Report

## Inputs honored

- Locked narrative: `PrologueStoryv0.3`, P-03 and P-07.
- Character continuity: `Player1Backgroundv0.2` for Marek, Joren and Edrin.
- Normative Bible workflow, role boundaries and assigned IDs.
- Approved `MAP-004 Eventwright Work Order — Survey Assignment and Report`.
- Accepted MAP-004 Mapping Pass 03 baseline SHA-256: `56e6080854d7c77498db66256eb28cb44d8ad808d7b6119a29a785f8c1e5d4b4`.
- Accepted MAP-003 Mapping Pass 02 baseline SHA-256: `f96b341538c0bf33b19844a6b276b879ebbed6ebdf296c58b7424ccad568f128`.

## Runtime dependencies

- RPG Maker MZ runtime and normal project data structure.
- Actor 1 remains Marek.
- Stock character sheet `img/characters/People1.png` for provisional Joren and Edrin graphics.
- Existing IDs and names: variable 1 `SYS_StoryStage`; switch 103 `PRO_Survey_Assignment_Received`; switch 110 `PRO_Report_Complete`.

No plugin, custom JavaScript, new audio, picture, item, battle, Common Event, quest or additional global state is required.

## Geometry and integration preservation

- MAP-004 `data`, dimensions, tileset, map properties and all eight anchor identities/coordinates are preserved; only the map note and authorized event pages differ.
- MAP-004 anchors 6–8 remain byte-equivalent to the accepted baseline.
- MAP-003 candidate changes event ID 2 only; its tile array and events 1 and 3–10 remain byte-equivalent.
- The installer patches only MAP-003 event ID 2, installs MAP-004, updates only MapInfos ID 4, and fills only blank assigned System names. Conflicting nonblank System names cause refusal.
- MapInfos ID 4 must be absent, null, blank, named `MAP004`, or already carry the exact `Brackenford - Survey Office` registration. Any unrelated registration is refused during preflight with zero writes.

## Explicit implementation interpretation

MZ page variable conditions are greater-than-or-equal. Each controller therefore includes the required exact internal equality/completion guard plus a blank next-stage ceiling page. The ceiling prevents a malformed debug/save combination (later stage with a missing completion switch) from leaving an autorun page continuously active. This adds no state and changes no normal story path.

Followers are forced OFF before and after each office controller because the approved Prologue exploration state is solo and Latch remains outside this room.

## Deviations and blockers

No dialogue, state, transfer, anchor or geometry deviation from the approved work order is known. Stock placeholders remain provisional by authority. Independent Eventwright Validation and RPG Maker MZ runtime testing are pending; this report does not claim either.
