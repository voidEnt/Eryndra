# MAP-002 Event Command Manifest

## Controllers

| Event | Active page gate | Exact internal gate | Trigger | Completion page(s) |
|---|---|---|---|---|
| `1 EV_Story_MorningController` | `SW101 ON` and `VR1 >= 1002` | `VR1 == 1002` and `SW102 OFF` | Autorun | `SW102 ON` or `VR1 >= 1003` |
| `2 EV_Story_EveningController` | `SW110 ON` and `VR1 >= 1011` | `VR1 == 1011` and `SW111 OFF` | Autorun | `SW111 ON` or `VR1 >= 1012` |

The higher blank pages prevent replay and prevent an autorun lock if a valid later story stage is loaded. No self switch or new global state is introduced.

Each speaker message uses a single MZ Show Text command with one to four continuation lines, each no longer than 36 characters. Wrapping changes display layout only: concatenating the physical lines reproduces the approved spoken line exactly.

## Morning command sequence

1. Fade out; reveal the player, hide followers, and place Marek `(14,14)` facing north.
2. Reset Davren `(21,13)`, Elira `(7,13)`, Nessa `(13,12)` and Latch `(13,18)`.
3. Clear MAP-001's inherited black tint, fade in, and hold 36 frames.
4. Play the five-line established-routine exchange.
5. Turn Latch south and play stock `Dog` once at volume 55.
6. Play the four-line door exchange.
7. Move Marek south to `(14,19)`, play stock `Equip1` once at volume 45/pitch 95, and play the two-line latch exchange.
8. Move Marek by the collision-safe path `(14,19) → (14,14) → (19,14) → (19,12) → (21,12)`.
9. Use two left/right facing pairs with 22-frame pauses to show the two inspections.
10. Play the field-kit, calibration-weight and departure exchanges in approved order.
11. Move Marek by `(21,12) → (19,12) → (19,14) → (14,14)` and face north.
12. Write `SW102 ON`, then `VR1 = 1003`; reveal the player and leave followers hidden.

The Morning controller contains the work order's 22 exact dialogue lines. The field kit and calibration weight never enter inventory.

## Evening command sequence

1. Fade out; reveal the player, hide followers, and place Marek `(14,19)`, family at ordinary anchors and Latch adjacent at `(13,19)`.
2. Clear any inherited tint, fade in, and hold 36 frames.
3. Play the eight exact entry/ordinary-household lines. Latch does not bark.
4. Fade out; stage supper at Marek `(15,13)`, Davren `(16,12)`, Elira `(14,11)`, Nessa `(13,12)`; fade in and hold 36 frames.
5. Play the 14 exact supper lines.
6. Fade out; hide the common-room family and morning Latch.
7. Place threshold Latch `(19,9)` facing north and Marek on the bed `(21,5)` using temporary stock `Damage1` presentation.
8. Scroll to the deterministic top-right bedroom frame using stock commands; apply restrained night tint; fade in; hold 75 frames.
9. Play `Ancient_ThreeNote_Resonance` exactly once at volume 35; change Marek's pose after 105 frames; continue for 219 frames. With the 3.4-second source cue, this leaves approximately 120 frames of silence before the fade. No dialogue and no repeated cue.
10. Fade out; restore Marek's `Actor1` runtime graphic.
11. Write `SW111 ON`, then `VR1 = 1012`, then transfer to MAP-001 `(14,10)`, facing south, fade None.

The Evening controller contains the work order's 22 exact dialogue lines.

## Character pages

| Event | Base placeholder | Post-morning action line |
|---|---|---|
| `5 EV_NPC_Davren` | `People1`, index 4 | `If the latch catches again, leave it for this evening.` |
| `6 EV_NPC_Elira` | `People1`, index 5 | `The survey office will still be there. Breakfast will not.` |
| `7 EV_NPC_Nessa` | `People2`, index 2 | `Latch thinks every closed door is a personal insult.` |
| `8 EV_NPC_Latch_Morning` | `Nature`, index 0 | None |
| `9 EV_NPC_Latch_EveningThreshold` | Hidden base page; controller reveals stock `Nature`, index 0 | None |

## Remaining anchors

Events 3-4 and 10-14, 16-17 retain their accepted locations and inert pages. Event 15 contains only the explicit `HOOK MAP-003` comment; it has no transfer. All 17 anchor IDs, names and coordinates are unchanged from Mapping Pass 01.

## MAP-001 authorized patch

Everything before the existing `HOOK PRO-SC-002` comment remains byte-equivalent to the accepted MAP-001 event data. The old unresolved ending comments are replaced by:

1. `HOOK PRO-SC-002: approved transfer to MAP-002 Morning.`
2. Transfer to MAP-002 `(14,14)`, facing north, fade None.

The validated title, pictures, sound, timing, state writes `SW101 ON` and `VR1=1002`, and the Omen controller are unchanged.
