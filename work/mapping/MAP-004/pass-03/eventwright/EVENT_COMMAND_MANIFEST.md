# MAP-004 Event Command Manifest

## MAP-004 event changes

| ID | Event | Pages and effects |
|---:|---|---|
| 1 | `EV_Story_SurveyAssignment` | Autorun at `VR-0001>=1004`, internally requires exact `1004` and `SW-0103 OFF`. Followers remain off, Marek walks from `(12,15)` to `(12,12)`, nine exact speaker-named messages run, then `SW-0103=ON` followed by `VR-0001=1005`. Blank stage-ceiling and completion pages stop replay. |
| 2 | `EV_Story_SurveyReport` | Autorun at `VR-0001>=1010`, internally requires exact `1010` and `SW-0110 OFF`. Marek stages identically, thirteen exact messages run, then `SW-0110=ON` followed by `VR-0001=1011`. Blank stage-ceiling and completion pages stop replay. |
| 3 | `EV_NPC_Joren` | Fixed `People1` index 4 placeholder, facing down. No action dialogue or state. |
| 4 | `EV_NPC_Edrin` | `People1` index 0 placeholder: hidden below 1004, visible at 1004, hidden 1005–1009, visible from 1010. No state or action dialogue. |
| 5 | `EV_Transfer_Brackenford` | Action button; transfer to MAP-003 `(31,16)`, facing south, normal black fade. |
| 6–8 | Approved prop/camera anchors | Preserved byte-equivalently from Mapping Pass 03. |

`Marek` is Actor 1/player and is not duplicated as a map event. Placeholder sheets establish no final appearance canon.

## MAP-003 isolated integration

Only event ID 2, `EV_Transfer_SurveyOffice`, changes. Its action page is available from `VR-0001>=1003`:

1. If `VR-0001` equals exactly `1003`, set it to `1004`.
2. Transfer to MAP-004 `(12,15)`, facing north, normal black fade.

At later eligible stages the same door transfers without changing story state. No other MAP-003 event, tile, collision value or property changes.

## Command types used

The candidate uses only comments, conditional branches, Show Text/continuation, switch and variable control, player follower control, forced player movement, transfer player, and branch terminators. It contains no battle, item, audio, picture, tint, shake, plugin, JavaScript, Common Event or unassigned-state command.

All physical Show Text content lines are at most 40 characters; the measured maximum is 40.
