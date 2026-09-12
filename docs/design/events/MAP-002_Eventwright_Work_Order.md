# MAP-002 Eventwright Work Order - Venn Home Prologue Scenes

**Primary map:** `MAP-002 Brackenford - Venn Home`  
**Runtime file:** `Map002.json`  
**Integration patch:** accepted MAP-001 opening controller only  
**Scenes:** `PRO-SC-002 Morning at the Venn House`, `PRO-SC-011 Home, But Changed`  
**Priority:** CORE  
**Status:** Approved for Eventwright Functional Spine Pass 01  
**Upstream:** MAP-002 Mapping Pass 01 final PASS  
**Locked sources:** `PrologueStoryv0.3` P-02/P-07; `Player1Backgroundv0.2` Venn household and voice guide

---

# 1. Objective

Turn the accepted MAP-002 spatial skeleton into two executable in-engine scenes without changing its geometry:

1. a warm, ordinary morning that establishes Marek, Davren, Elira, Nessa and Latch before releasing the player; and
2. the late-evening return that restores normality, then ends with Latch at Marek's threshold and one distant three-note signal.

This pass must prove event-page gating, character staging, dialogue, movement, player release, state transitions and the two connections to MAP-001. It is not final art, final audio mixing or MAP-003 integration.

# 2. Authority and Restrictions

The Eventwright owns executable scene logic only.

Do not:

- alter MAP-002 tile geometry, furniture or collision
- move or rename the 17 accepted anchors without a returned Mapping defect
- invent additional family members, rooms, quests, rewards, items or lore
- make Latch supernatural or unusually intelligent
- introduce ancient-system terminology, ring imagery or overt foreshadowing in the morning
- turn the calibration weight or field kit into database inventory
- make Marek eloquent, heroic, mystical or certain about the Old Place
- add combat, plugins or custom runtime JavaScript
- create a guessed MAP-003 coordinate
- rewrite MAP-001 beyond the exact transfer hook authorized below

Stock character/face graphics are placeholders and do not establish final appearance canon.

# 3. Inputs

- Accepted mapping candidate: `work/mapping/MAP-002/pass-01/Map002.json`
- Accepted MAP-001 event candidate: `work/mapping/MAP-001/pass-02/eventwright/Map001.json`
- Existing audio assignment: `SE-001 Ancient_ThreeNote_Resonance`
- Exact MAP-002 anchors from the mapper blueprint
- Stock MZ `Inside` tileset in database slot 3
- Stock MZ character and face sheets for temporary presentation

# 4. Placeholder Presentation Assignments

Use these only for Functional Spine testing:

| Character | Character sheet/index | Face sheet/index | Notes |
|---|---|---|---|
| Marek | `Actor1`, index 0 | `Actor1`, index 0 | Actor 1; canonical default name Marek |
| Davren | `People1`, index 4 | `People1`, index 4 | Temporary practical older man |
| Elira | `People1`, index 5 | `People1`, index 5 | Temporary older woman |
| Nessa | `People2`, index 2 | `People2`, index 2 | Temporary younger family member |
| Latch | `Nature`, index 0 | none | Temporary ordinary dark road dog |

Dialogue windows use speaker names. Latch receives no speech or thought text.

# 5. State Contract

## Morning

**Entry requirements:**

- `VR-0001 SYS_StoryStage = 1002`
- `SW-0101 PRO_WatcherStation_Awakened = ON`
- `SW-0102 PRO_VennHome_Intro_Complete = OFF`

**Output:**

- `SW-0102 = ON`
- `VR-0001 = 1003`
- player visible and controllable on MAP-002
- family and Latch remain available for simple local interaction

## Evening

**Entry requirements:**

- `VR-0001 SYS_StoryStage = 1011`
- `SW-0110 PRO_Report_Complete = ON`
- `SW-0111 PRO_HomeEvening_Complete = OFF`

**Output:**

- `SW-0111 = ON`
- `VR-0001 = 1012`
- transfer under black to MAP-001 `(14,10)`, facing down, fade type None
- MAP-001's existing Omen controller owns the next sequence

Do not allocate new global switches, variables or Common Events. Local pages/self switches may be used only where required to prevent replay.

# 6. MAP-001 Opening Transfer Patch

The accepted MAP-001 opening currently ends on black after the `ERYNDRA` title. Preserve its complete validated sequence and state writes.

After the title is erased and the screen is black, add exactly one transfer:

- destination: MAP-002 `(14,14)`
- direction: up
- fade type: None

MAP-002 owns the subsequent fade-in and player reveal. This change requires MAP-001 regression validation of its opening presentation and final state.

# 7. Event Architecture

## `EV_Story_MorningController` - Local Event 1

- Autorun only when the Morning entry contract is true.
- Use an exact internal variable comparison; MZ's page-level variable condition is greater-than-or-equal and must not be treated as equality.
- Start with the screen black after the MAP-001 transfer.
- Place/finalize Marek and family staging before Fade In.
- Keep followers hidden.
- Run the exact Morning sequence below.
- Set `SW-0102`, then `VR-0001 = 1003` only after the family beat completes.
- End autorun and release player control without replay.

## `EV_Story_EveningController` - Local Event 2

- Autorun only when the Evening entry contract is true.
- Use an exact internal variable comparison.
- Begin from black or fade immediately to black before repositioning.
- Run the exact Evening sequence below.
- Set `SW-0111`, then `VR-0001 = 1012` immediately before the black transfer to MAP-001.
- Do not set `SW-0112 PRO_Complete`; MAP-001/closing montage owns Prologue completion.

## Family events - Local Events 5-7

- Use approved placeholder graphics.
- Morning starting positions remain at their accepted anchors unless the controller temporarily relocates them within the approved zones.
- After `SW-0102` turns ON, each may provide one short ordinary action-button line. These lines must not create new facts or state.
- Evening controller may reposition them around the supper table; restore/hide them as needed for the bedroom cut.

Allowed post-intro ambient lines:

- Davren: `If the latch catches again, leave it for this evening.`
- Elira: `The survey office will still be there. Breakfast will not.`
- Nessa: `Latch thinks every closed door is a personal insult.`

## Latch events - Local Events 8-9

- Morning Latch is visible near the entry and may use one stock `Dog` SE during the controlled sequence.
- Evening threshold Latch is visible only for the bedroom beat, at `(19,9)`, facing north.
- No bark during the final waiting silence.
- Latch must not activate a switch, lead Marek, detect a named force or imply supernatural comprehension.

## Props and cameras - Local Events 10-17

- Convert only the anchors needed for controlled movement/reference.
- Crooked latch, field kit and calibration weight are scene actions, not item pickups.
- The front-door event must not transfer to MAP-003 in this pass. It remains a documented inactive integration hook after player release.
- Camera anchors are registration references; use stock scrolling/centering only if required.

# 8. Morning Sequence - Exact Script and Beat Order

## Initial staging

- Marek/player at `(14,14)`, facing up.
- Davren at `(21,13)` in the repair nook.
- Elira at `(7,13)` in the kitchen.
- Nessa at `(13,12)` near the table.
- Latch at `(13,18)` near the entry.
- Fade In at normal MZ speed.
- Pause briefly so the household reads before dialogue begins.

## Dialogue A - established routine

**Elira:** `If you check that strap again, it may start charging you for the inspection.`

**Marek:** `The stitching was loose.`

**Nessa:** `It was loose the first time you checked it.`

**Marek:** `Then the second check confirmed an excellent memory.`

**Davren:** `A sound professional result.`

Delivery is dry and familiar, not performed as a comedy routine.

## Latch and crooked-latch beat

- Latch turns toward the front door; play stock `Dog` once at restrained volume.

**Nessa:** `Latch has been arguing with the door since sunrise.`

**Marek:** `He dislikes closed questions.`

**Nessa:** `Doors.`

**Marek:** `Those too.`

- Move Marek to the latch position `(14,19)`.
- Briefly face the door and play one restrained stock repair/equip sound.

**Davren:** `It would have held another day.`

**Marek:** `That's what it said yesterday.`

The latch is corrected as habit, not as a puzzle or player reward.

## Field-kit and remembered-obligation beat

- Move Marek to the repair/kit staging area near `(21,12)` without crossing blocked furniture.
- Face the field-kit anchor.
- Use two small inspection pauses or facing motions to visibly represent checking twice.

**Elira:** `You checked it last night.`

**Marek:** `I checked the measure. This is the buckle.`

**Nessa:** `A separate crisis.`

**Marek:** `Potentially.`

- Marek turns toward `EV_Prop_CalibrationWeight`.

**Marek:** `Joren's calibration weight.`

**Davren:** `He would have remembered.`

**Marek:** `Tomorrow, perhaps.`

No item-acquisition sound, inventory message or database item is permitted.

## Departure expectation and release

**Elira:** `Back before supper?`

**Marek:** `That was the assignment.`

**Davren:** `Assignments and roads both change.`

**Marek:** `Then I will write down which one.`

- Return Marek to a clear player-release cell near `(14,14)`.
- Set the Morning output state.
- End autorun.
- Player control begins.

Do not display a supernatural cue, title card or ancient terminology. The front door remains the obvious next route, but its MAP-003 transfer is intentionally pending.

# 9. Evening Sequence - Exact Script and Beat Order

## Entry and muddy Latch

- Start Marek at `(14,19)`, facing up.
- Latch is adjacent in the entry area.
- Place Davren, Elira and Nessa in their ordinary common-level zones.
- Fade In at normal MZ speed.

**Nessa:** `What happened to Latch?`

**Marek:** `Mud.`

**Nessa:** `I can see the mud. Why is he wearing half the north road?`

**Marek:** `He found a ditch he disagreed with.`

**Elira:** `Then both of you can leave the disagreement by the door.`

## Ordinary household concern

**Davren:** `The west shutter caught again.`

**Elira:** `Because the frame is warped.`

**Davren:** `The hinge remains more cooperative.`

This exchange is domestic continuity, not setup for a quest or repair interaction.

## Supper

- Fade or move the group cleanly to four distinct positions around the common table.
- Preserve a readable, unhurried pause before the next exchange.

**Elira:** `You are very quiet.`

**Marek:** `I was checking whether I had anything useful to say.`

**Elira:** `And?`

**Marek:** `Not yet.`

**Nessa:** `That has never stopped Father.`

**Davren:** `It has slowed me considerably.`

**Davren:** `Was the marker wrong?`

**Marek:** `The marker or the ground. There was old masonry behind the slope.`

**Davren:** `Road risk?`

**Marek:** `Maybe. Joren will send a proper crew.`

**Elira:** `And the rest?`

**Marek:** `I do not know enough yet.`

**Elira:** `Then say that.`

**Marek:** `I just did.`

Marek does not say the stone answered him. No family member panics or names the disturbance.

## Bedroom and distant notes

- Fade Out.
- Hide the common-room family events.
- Move the player/camera to Marek's bedroom composition.
- Represent Marek asleep using a stock temporary sleeping/downed presentation that does not alter permanent actor graphics.
- Place Latch at `(19,9)`, facing north, outside the room.
- Apply a restrained night tint and Fade In.
- Hold long enough to establish quiet.
- Play `SE-001 Ancient_ThreeNote_Resonance` exactly once at faint volume. Do not use the full MAP-001 opening volume.
- Marek wakes or changes pose without leaving the bed.
- Wait in silence. The sound does not repeat.
- Do not add dialogue explaining the sound. A brief `...` from Marek is permitted only if required to make waking legible.
- Fade Out to full black.
- Set the Evening output state and transfer to MAP-001 as defined.

# 10. Presentation Timing Targets

These are pass targets, not frame-locked canon:

- opening household read before first line: 24-45 frames
- small conversational pauses: 8-18 frames
- inspection motions/checks: 15-30 frames each
- supper establishing pause: 30-45 frames
- bedroom silence before notes: 60-90 frames
- silence after notes: 90-150 frames
- final Fade Out: normal MZ fade

Avoid rapid-fire dialogue and excessive camera motion.

# 11. Functional Test Modes

Provide repeatable instructions for:

## Test A - MAP-001 into Morning

- New Game starts MAP-001.
- Existing validated opening plays unchanged.
- Title clears under black.
- Transfer arrives at MAP-002 `(14,14)`.
- Morning sequence plays once and releases control with `[SW102=true, VR1=1003]`.

## Test B - Evening direct setup

Provide an F8 console setup that safely establishes:

- MAP-002
- player at `(14,19)`
- `SW110=true`
- `SW111=false`
- `VR1=1011`

The evening scene then plays once, sets `[SW111=true, VR1=1012]`, and transfers under black to MAP-001 for its existing Omen controller.

# 12. Installer and Deliverables

Produce under `work/mapping/MAP-002/pass-02/eventwright/`:

1. integrated `Map002.json`
2. MAP-001 transfer-patched candidate, clearly named and never confused with the accepted baseline
3. Event Command Manifest documenting pages, triggers, dialogue, movement and state writes
4. guarded installer for an Eryndra review project
5. installer tests proving all preflight checks occur before writes
6. Eventwright validator and machine-readable results
7. playtest instructions for Test A and Test B
8. dependency/deviation report

The installer must:

- refuse any path representing `SampleGenerated` or either immutable source archive
- require an RPG Maker MZ project structure
- verify compatible MAP-001 and MAP-002 baselines before changing files
- update only explicitly documented data/runtime dependencies
- make recoverable backups after all refusal checks and before replacement
- leave a refused target tree byte-identical
- never edit the supplied ZIPs or an extracted reference project

# 13. Eventwright PASS Gate

The pass may advance to independent Validation only when:

- both controllers use exact entry gating and do not replay
- all required morning/evening beats and exact dialogue are present
- all movement routes remain on the accepted walkable geometry
- Marek is released visibly and controllably after Morning
- Morning ends with `SW102 ON`, `VR1=1003`
- Evening ends with `SW111 ON`, `VR1=1012`
- MAP-001 opening transfers to the exact approved MAP-002 spawn without changing its prior presentation/state
- MAP-002 evening transfers under black to the accepted MAP-001 Omen entry
- Latch remains ordinary and silent except for one allowed morning dog SE
- the distant three-note cue occurs exactly once and does not repeat
- no new global IDs, items, quests, combat, plugins or canon claims are introduced
- MAP-003 remains an explicit unresolved hook rather than a guessed transfer
- all deviations are disclosed

Static PASS does not equal runtime acceptance. Independent Validation and user-side MZ playtesting remain required.

