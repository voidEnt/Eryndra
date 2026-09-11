# Eryndra Implementation Bible — Document Index

The Eryndra Implementation Bible is a controlled set of normative documents, not a single file. The documents below collectively define implementation canon.

## Core Bible

- `Eryndra_Game_Implementation_Bible.md` — top-level implementation rules, project structure, production workflow, and domain definitions.
- `Master_Implementation_Index.md` — compact cross-reference registry for scenes, maps, actors, state, assets, and implementation status.
- `Production_Roles_and_Handoff_Contract.md` — binding authority limits, inputs, outputs, escalation rules, and PASS gates for Foreman, Mapping, Eventwright, Validation, Asset, and Technical workers.
- `ID_Allocation_Plan.md` — RPG Maker MZ numeric allocation policy.
- `Prologue_MZ_ID_Assignments.md` — concrete Prologue MZ IDs.
- `CHANGELOG.md` — structural and implementation-reference history.

## Supporting Design Specifications

The Bible may reference supporting specifications in `../design/`. These become controlling requirements for the production unit when cited by an approved work order.

Current examples include:

- `../design/Prologue_Implementation_Decomposition.md`
- `../design/Map_Work_Order_Standard.md`

## Authority

When documents conflict, use the source-of-truth hierarchy in the main Bible. The role contract is normative for worker authority and handoffs; task-specific work orders may narrow a worker's authority but may not silently expand it beyond the Bible.

## Production Chain

**Foreman → Blueprint / Work Order → Mapping → Eventwright → Validation → Accepted Build**

A worker's ability to edit repository files does not grant authority to redesign the domain represented by those files.
