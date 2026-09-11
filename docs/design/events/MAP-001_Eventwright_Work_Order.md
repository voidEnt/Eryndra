# MAP-001 Eventwright Work Order - Forgotten Watcher Station

**Scenes:** PRO-SC-001 The Forgotten Place; reusable controller for PRO-SC-012 The Omen  
**Map:** MAP-001 / Map001.json  
**Priority:** CORE  
**Required inputs:** accepted Mapping Pass 01, accepted MAP-001 Asset pass, Bible, P-01/P-08 canon  
**Implementation mode:** stock RPG Maker MZ event commands; no plugins

## Eventwright objective

Turn the accepted chamber and named anchors into a playable in-engine opening cinematic and a gated closing-omen sequence while preserving the map geometry and canon secrecy.

## Opening controller

MAP-001-EV-001 / EV_Story_PrologueOpening page 1 is an autorun opening controller active before SW-0101 PRO_WatcherStation_Awakened.

Required sequence:

1. Hide player and followers; lock player control through autorun.
2. Set SW-0100 PRO_Started ON and VR-0001 SYS_StoryStage to 1001.
3. Begin black, then reveal the dormant chamber slowly.
4. Hold long enough to establish abandonment.
5. Apply restrained low-pressure presentation and a brief dust tremor.
6. Present one restrained ring pulse.
7. Play SE-001 once; the audio asset itself contains three equally spaced notes.
8. Remove the full pulse.
9. Leave the narrow residual line visible briefly.
10. Fade to black.
11. Display PIC-006 title ERYNDRA, then remove it.
12. Set SW-0101 PRO_WatcherStation_Awakened ON.
13. Set VR-0001 SYS_StoryStage to 1002.
14. End on black at an explicit PRO-SC-002 transfer hook.

The MAP-002 destination is not yet assigned. Do not guess it. In this MAP-001 proof build, terminate the controller cleanly on a blank higher-priority page after committing state. The later integration pass inserts the approved transfer at the marked hook.

Page 2 is a blank non-autorun page conditioned on SW-0101.

## Omen controller

MAP-001-EV-002 / EV_Story_PrologueOmen page 1 is an autorun closing controller conditioned on VR-0001 SYS_StoryStage at least 1012 and before SW-0112 PRO_Complete.

Required MAP-001 portion:

1. Begin black and reveal the same chamber.
2. Show the propagated ring state with the fracture black.
3. Play SE-001.
4. Hold for the distant answer hook; MAP-008 owns the off-map answer montage.
5. Fade to black.
6. Leave an explicit continuation hook for MAP-007/MAP-008 montage integration.

Do not set SW-0112 or advance to 2001 until the complete multi-map P-08 montage exists. A blank page conditioned on SW-0112 prevents replay after later integration.

## Presentation anchors

- EV_Visual_FracturedRing remains the registration anchor.
- EV_FX_DustTremor remains the dust/shake reference.
- EV_Camera_Chamber and EV_Camera_Ring remain camera references.
- Presentation may use full-screen pictures aligned to the approved camera frames.

## State and safety rules

- Use only assigned switches 100, 101, 111, 112 and variable 1 where required.
- Opening must not replay after switch 101.
- Closing must not run during opening or normal post-opening state.
- No dialogue, explanatory terminology, date, location name, character, combat, inventory, reward or choice.
- The player must remain invisible and unable to interrupt the sequence.
- No transfer destination is invented.
- No Go To Title substitute for the narrative title reveal.

## Required proof-build outputs

- Map001.json with event commands and asset references.
- Event_Command_Manifest.md listing commands, timing, state writes and continuation hooks.
- install_into_blank_mz_project.py that installs the MAP-001 proof package into a newly created user-owned blank MZ project, creates backups, registers TIL-007, updates MapInfos/System names, copies assets and leaves reference ZIPs untouched.
- validate_eventwright.py and machine-readable results.
- Local playtest instructions for opening and closing entry states.

## Acceptance

Eventwright may hand off when JSON and asset references validate, opening/closing pages are correctly gated, the opening commits switch 100/101 and variable 1002, the title and three-note cue are present, the closing defers global completion until its future montage, and no unapproved behavior exists. Actual visual/audio playtest evidence is required before MAP-001 is considered fully built.
