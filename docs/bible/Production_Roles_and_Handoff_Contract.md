# Eryndra Production Roles & Handoff Contract

**Status:** Normative Bible document  
**Applies to:** All implementation work unless a task-specific work order explicitly narrows authority further  
**Extends:** Main Bible Sections 1.15 and 9

---

# 1. Purpose

Eryndra is produced through specialized roles rather than by giving one worker unrestricted authority over an entire scene. Each role receives defined inputs, owns a limited domain, produces a defined deliverable, and hands work to the next stage.

Canonical chain:

**Foreman → Blueprint / Work Order → Mapping → Eventwright → Validation → Accepted Build**

Shorthand implementation chain:

**Mapping → Eventwright → Validation**

The same human or AI may perform more than one role at different times, but must adopt the authority limits of the role currently being performed. A worker may not use access to the repository or project as permission to exceed the role's design authority.

---

# 2. Universal Worker Rules

These rules apply to every role.

## 2.1 Canon and Requirement Hierarchy

When instructions conflict, use this precedence:

1. Locked story canon
2. Implementation Bible and normative Bible documents
3. Approved task-specific blueprint/work order
4. Validated upstream implementation
5. Worker preference

A lower level may not silently override a higher level.

## 2.2 No Silent Design Expansion

Workers may identify opportunities outside their authority, but must record them as **proposals** rather than implement them without approval.

Examples include:

- new story beats
- additional characters
- new quests
- new treasure or rewards
- new global switches or variables
- new maps
- new combat encounters
- new lore implications
- plugin or custom-code additions
- changes to chronology or geography

## 2.3 Minimum Necessary Change

A worker should make the smallest change that satisfies the approved requirement. Do not redesign unrelated content while completing a localized work order.

## 2.4 Preserve Stable IDs

Workers may not renumber, recycle, or repurpose implemented IDs. New global IDs must come from an approved allocation or be escalated to the Foreman/Bible before use.

## 2.5 Upstream Defects Must Be Returned Upstream

A downstream worker must not conceal an upstream problem with brittle compensation.

Examples:

- Eventwright finds insufficient staging space → return to Mapping.
- Validator finds missing canonical requirement → return to the responsible stage or Foreman.
- Mapper finds contradictory geometry requirements → stop and escalate to Foreman rather than choose a new canon interpretation.

## 2.6 No Unrecorded Requirement Changes

If implementation reveals that an approved requirement must change, the controlling Bible/work-order document must be revised before the change is treated as authoritative.

## 2.7 Passes Are Expected

No worker should optimize for appearing complete in one pass. Skeleton, refinement, correction, and regression passes are normal production behavior.

---

# 3. Foreman

## 3.1 Purpose

The Foreman is the production coordinator and specification owner. The Foreman converts project-level intent and canon into work that specialized roles can execute without inventing missing requirements.

## 3.2 Required Inputs

- locked story canon
- Implementation Bible
- current repository/project state
- prior validation reports
- current production objective

## 3.3 Foreman May

- choose the next production unit
- create and revise blueprints/work orders
- resolve contradictions between implementation documents
- allocate or approve new IDs within established policy
- approve changes to Bible requirements
- decide whether a proposal becomes CORE, SUPPORT, or DEFERRED
- assign defects to the responsible production stage
- approve progression to the next stage
- decide when additional passes are warranted
- coordinate Git/version-control milestones

## 3.4 Foreman May Not

- contradict locked story canon without an explicit story-canon revision decision
- silently treat implementation convenience as canon
- mark work Validated without the required validation evidence
- bypass stage ownership merely because a downstream implementation is faster
- redefine an implemented stable ID for an unrelated object

## 3.5 Foreman Output

At minimum, the Foreman supplies an approved work order containing enough information for the next role to proceed without inventing major requirements.

## 3.6 Foreman Escalation Rule

If the locked story itself is genuinely ambiguous in a way that materially affects implementation, the Foreman records the ambiguity and makes an explicit implementation interpretation. That interpretation becomes implementation canon unless the locked story is later formally revised.

---

# 4. Mapper

## 4.1 Purpose

The Mapper creates the physical stage on which approved scenes will run.

**Mapping owns space.**

## 4.2 Required Inputs

- approved map work order
- relevant map entry in Master Implementation Index
- cited scene decomposition
- cited locked-story section(s)
- applicable Bible world/asset rules
- upstream validated map dependencies where relevant

The Mapper must check the locked-story source for tone and spatial implications before construction.

## 4.3 Mapper May Decide

Only within work-order freedom, the Mapper may determine:

- minor decorative placement
- noncanonical rubble/crack/prop variation
- exact tile-level shaping inside approved zone boundaries
- minor visual asymmetry
- harmless environmental details that do not imply new lore
- small passability adjustments that preserve required routes and staging

## 4.4 Mapper May Propose but Not Implement Without Approval

- different map dimensions outside permitted tolerance
- additional rooms or explorable branches
- changed entrances/exits
- new landmarks with lore significance
- additional transfer destinations
- new gameplay interactions
- additional story/event spaces not required by the work order

## 4.5 Mapper Must Not

- write or rewrite story dialogue
- change scene order
- invent story beats
- invent named NPCs or factions
- add quests, treasure, shops, enemies, or battles unless specified
- assign new global switches/variables/common events
- implement substantial story event logic
- add lore-significant imagery not approved by canon/work order
- expose information the scene is required to conceal
- redesign neighboring maps by implication
- add inaccessible decorative areas that falsely imply explorable destinations without a production reason

## 4.6 Mapper Required Output

- spatially complete `Map###.json` skeleton/refinement appropriate to the assigned pass
- required named event anchors/stubs
- required transfer/spawn locations
- correct passability/regions/collision for the assigned pass
- dependency/deviation note
- screenshots or equivalent review representation when requested

## 4.7 Mapping PASS Gate

Mapping may advance to Eventwright only when:

- required dimensions/tolerance are satisfied
- all required spatial zones exist
- required routes and staging spaces function
- required anchors exist and are identifiable
- passability supports the planned scene
- visual structure passes the Narrative Style Gate at the current production fidelity
- no unauthorized story/gameplay content was introduced
- known deviations are documented

Decorative completeness is not required for a skeleton PASS unless the work order says the presentation itself is functionally necessary.

---

# 5. Eventwright

## 5.1 Purpose

The Eventwright converts an accepted mapped stage into executable RPG Maker MZ scene behavior.

**Eventwright owns executable scene logic.**

## 5.2 Required Inputs

- accepted map-stage deliverable
- approved map/event work order
- scene decomposition
- locked-story source for the scene
- registered switches, variables, common events, IDs, actors, NPCs, items, battles, audio/presentation dependencies
- relevant preceding/following scene handoff requirements

## 5.3 Eventwright May Decide

Within approved requirements, the Eventwright may determine:

- exact event-page arrangement
- event command sequencing
- reasonable wait-frame values and movement timing
- self-switch usage for purely local implementation state
- event-anchor utilization
- technically equivalent stock-MZ command structure
- minor pacing adjustments that do not alter story content or information timing

## 5.4 Eventwright May Propose but Not Implement Without Approval

- new global switches/variables/common events outside approved allocation
- map geometry changes
- new dialogue or substantive dialogue rewrites
- extra interactions affecting characterization or lore
- plugin/custom-JavaScript solutions
- new rewards, items, enemies, or encounters
- alternate story branches

## 5.5 Eventwright Must Not

- materially redesign map geometry to solve an event problem
- invent or omit mandatory story beats
- reveal hidden information early
- change character identity, motive, relationship, chronology, or canon outcome
- create unapproved global state
- add battles merely for pacing or tutorial purposes
- create rewards/loot not in the work order
- use fragile event logic to conceal a Mapping defect that should be returned upstream
- alter stable IDs
- silently substitute a different scene outcome because it is easier to implement

## 5.6 Eventwright Required Output

- executable event implementation for the assigned scene/pass
- correct use of approved IDs and state
- defined entry condition and exit condition
- resulting state exactly documented
- any required dependency/deviation report
- no hidden change to the controlling work order

## 5.7 Eventwright PASS Gate

Eventwright may advance to Validation only when:

- the scene runs from required entry state to required exit state
- all mandatory beats are represented
- required switches/variables/self switches end in the expected state
- transfers and handoffs function
- repeat interactions do not obviously corrupt state
- required presentation hooks are present at the assigned fidelity
- no unauthorized design expansion was introduced
- known limitations are documented

---

# 6. Validator

## 6.1 Purpose

Validation independently determines whether the implementation satisfies its controlling requirements.

**Validation owns acceptance.**

The Validator is not a cleanup worker whose purpose is to make the build pass by editing whatever is convenient.

## 6.2 Required Inputs

- locked story source
- Implementation Bible
- applicable map/event work orders
- actual RPG Maker implementation
- prior validation report when performing regression
- expected upstream/downstream state

## 6.3 Validator May

- inspect all relevant project data
- execute/playtest the assigned flow
- compare implementation against canon and Bible
- identify defects and classify ownership
- require regression testing
- issue PASS, CONDITIONAL PASS, or FAIL when the work order allows those outcomes
- recommend improvements as nonblocking proposals

## 6.4 Validator May Not

- silently rewrite Mapping or Eventwright work to make a test pass
- change canon or requirements during validation
- downgrade an unmet CORE requirement because it is inconvenient
- introduce new design while labeling it a bug fix
- approve known story/state corruption without explicit Foreman acceptance
- treat visual preference as a defect unless it violates the work order/style gate

## 6.5 Defect Ownership

Every blocking defect should identify at least:

- requirement violated
- evidence/observed behavior
- owning stage: Blueprint/Foreman, Mapping, Eventwright, Asset, or other explicit owner
- severity
- required correction outcome
- regression scope

The Validator should describe the required result, not micromanage the implementation method unless the method itself is constrained by the Bible.

## 6.6 Validation Outcomes

### PASS
All acceptance criteria for the assigned production fidelity are satisfied.

### CONDITIONAL PASS
May be used only when the remaining issues are explicitly nonblocking for the next stage and are recorded for later correction. A CONDITIONAL PASS may not hide a missing CORE dependency that downstream work requires.

### FAIL
One or more blocking requirements are unmet. Work returns to the responsible stage.

## 6.7 Validation PASS Gate

A scene/map can be considered Validated for its current milestone only after applicable checks cover:

- technical integrity
- narrative/canon fidelity
- state integrity
- transfers/handoffs
- passability where relevant
- repeat/save-load behavior where relevant
- absence of obvious soft locks or sequence breaks
- integration with required neighboring scene states

A later change to validated content triggers regression validation of affected requirements.

---

# 7. Asset Worker / Asset Pass

Assets may be produced by a separate worker or within an explicitly assigned asset task. Asset creation is not automatically part of Mapping or Eventwright authority.

## 7.1 Asset Worker May

- create or select assets meeting an approved asset specification
- produce placeholder or final assets according to assigned fidelity
- propose alternatives when technical constraints prevent the requested asset

## 7.2 Asset Worker Must Not

- introduce new canonical symbols, costumes, architecture, technology, creatures, or cultural implications without approval
- change character identity or established visual requirements
- rename runtime assets after implementation without dependency review
- substitute a lore-significant visual merely because it is aesthetically preferable

Asset work returns to Mapping/Eventwright only through documented asset dependencies so spatial and event logic remain traceable.

---

# 8. Technical / Tooling Worker

A Technical worker may create scripts, validators, JSON transforms, build helpers, or custom code when assigned.

## 8.1 Technical Worker May

- automate repetitive transformations
- build schema/consistency validators
- manipulate project JSON according to approved specifications
- add tests and diagnostics
- propose tooling improvements

## 8.2 Technical Worker Must Not

- infer missing game design and encode it as fact
- allocate new story/database IDs without approval
- change narrative data to satisfy a technical constraint without escalation
- introduce plugins/custom runtime code contrary to the plugin policy
- alter valid content merely to simplify a script

Automation must conform to the Bible; the Bible does not conform to accidental limitations of automation unless the Foreman explicitly changes the specification.

---

# 9. Git and Version-Control Responsibilities

## 9.1 Every Stage Must Leave a Traceable State

Meaningful production changes should be committed with messages that identify the production unit and pass where practical.

Examples:

- `MAP-001 mapping skeleton pass`
- `PRO-SC-001 eventwright functional pass`
- `MAP-001 validation corrections`

## 9.2 Do Not Mix Unrelated Work

A worker should avoid bundling unrelated map/scene/database changes into one handoff unless the work order explicitly spans them.

## 9.3 Validation Baseline

Validation should identify the commit or project state being validated when practical so later changes can trigger targeted regression.

## 9.4 Work Orders and Reports Are Versioned Artifacts

Blueprints, event work orders, validation reports, and substantive deviation records belong under version control alongside the game implementation.

---

# 10. Handoff Contract

Every handoff must answer five questions:

1. **What was assigned?**
2. **What was produced?**
3. **What requirements are satisfied?**
4. **What remains incomplete, provisional, or deviated?**
5. **What does the next role need to know before proceeding?**

A worker may not represent a task as complete when known blocking deviations remain undisclosed.

---

# 11. Anti-Drift Rule

The production pipeline exists specifically to prevent cumulative interpretation drift.

Each downstream role must use the Bible/work order as its specification and the locked story as its narrative verification source. A downstream worker should not reinterpret the full story independently and then replace upstream decisions with its own preferred version.

If a worker believes the specification is wrong, the correct action is **escalate and revise the specification**, not silently diverge from it.

---

# 12. Summary Authority Matrix

| Role | Owns | May propose outside domain? | May silently change another domain? | Can approve final acceptance? |
|---|---|---:|---:|---:|
| Foreman | Requirements, coordination, explicit interpretations | Yes | No | Coordinates acceptance; does not replace required Validation |
| Mapper | Space | Yes | No | Mapping-stage handoff only |
| Eventwright | Executable scene logic | Yes | No | Eventwright-stage handoff only |
| Validator | Acceptance/testing | Yes | No | Yes, for defined validation scope |
| Asset Worker | Assigned visual/audio assets | Yes | No | Asset-spec handoff only |
| Technical Worker | Assigned tooling/automation/code | Yes | No | Technical handoff only |

**Core rule:** The ability to edit a file does not grant authority to redesign what the file represents.
