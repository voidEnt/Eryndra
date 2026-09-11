# MAP-001 Event Command Manifest — Pass 02

**Map:** MAP-001 / `Map001.json`  
**Scenes:** PRO-SC-001 opening; MAP-001 portion of PRO-SC-012  
**Implementation:** stock RPG Maker MZ commands; no plugin commands or script calls

## Runtime presentation

- `TIL-007` supplies transparent blocked/passable A5 tiles. Accepted Pass-01 floor cells become passable tile 1537; walls and outer buffer become blocked tile 1536.
- The map uses `!MAP001_WatcherStation_Base` as a fixed, map-aligned parallax. The installer copies the approved `MAP001_WatcherStation_Base.png` under that MZ runtime filename.
- Ring, dust and title pictures use screen coordinates `(0,0)`, upper-left origin, 100% scale and normal blend.
- The hidden player starts at `(14,10)`, which produces the approved chamber camera. Scrolling north two tiles produces the approved ring camera.

## MAP-001-EV-001 — EV_Story_PrologueOpening

### Page 1

**Condition:** none  
**Trigger:** Autorun  
**Purpose:** PRO-SC-001

Command order:

1. Hide the player and followers. Autorun locks input.
2. Set `SW-0100 PRO_Started` ON and `VR-0001 SYS_StoryStage` to `1001`.
3. Tint immediately to full black and wait 30 frames.
4. Reveal the dormant chamber over 180 frames using a restrained dark/desaturated tone; hold 150 frames.
5. Scroll north two tiles to the registered ring camera.
6. Show `PIC-005 MAP001_Dust_Tremor`, apply a restrained 36-frame shake, and clear the dust overlay.
7. Fade in `PIC-002 MAP001_Ring_Pulse` over 15 frames.
8. Play `SE-001 Ancient_ThreeNote_Resonance` exactly once. The OGG contains all three notes and their equal intertone silence. Hold 210 frames for its measured 3.4-second duration plus a small tail.
9. Fade out and erase the full pulse, then hold 24 frames with the ring fully dark.
10. A moment later, show `PIC-003 MAP001_Ring_Residual` for 120 frames.
11. Fade the screen to black, erase the residual, and set the underlying map tint to full black before screen brightness returns.
12. Show `PIC-006 SYS_Eryndra_Title` at zero opacity, fade the screen back in over the still-black-tinted map, then fade the title itself in over 45 frames, hold 90, fade it over 45, and erase it.
13. Set `SW-0101 PRO_WatcherStation_Awakened` ON and `VR-0001 SYS_StoryStage` to `1002`.
14. End on black at comment hook `HOOK PRO-SC-002`. No transfer command exists in this proof build.

### Page 2

**Condition:** `SW-0101` ON  
**Trigger:** Action Button, inert  
**Purpose:** Stops opening replay after its state commit.

## MAP-001-EV-002 — EV_Story_PrologueOmen

### Page 1

**Condition:** `VR-0001 SYS_StoryStage >= 1012`  
**Trigger:** Autorun  
**Purpose:** The MAP-001 portion of PRO-SC-012

Command order:

1. Hide player and followers; tint immediately to black.
2. Reveal the same chamber over 120 frames and scroll north two tiles.
3. Show `PIC-004 MAP001_Ring_Propagated` with the fracture left black by the asset.
4. Play `SE-001` exactly once and hold 210 frames.
5. Hold 90 frames at `HOOK DISTANT_ANSWER`; MAP-008 will own the off-map answering montage.
6. Fade to black and erase the propagated overlay.
7. End at `HOOK PRO-SC-012 CONTINUE` for later MAP-007/MAP-008 integration.
8. Set local Self Switch A ON to prevent a proof-build autorun loop.

This page does not set `SW-0112 PRO_Complete` or advance the story stage to `2001`.

### Page 2

**Condition:** local Self Switch A ON  
**Trigger:** Action Button, inert  
**Purpose:** Stops proof-build replay while the multi-map montage is absent.

### Page 3

**Condition:** `SW-0112 PRO_Complete` ON  
**Trigger:** Action Button, inert  
**Purpose:** Final high-priority replay guard for the integrated Prologue.

## Registration anchors

Events 3–6 retain their accepted IDs, names and coordinates and contain only the terminating command:

| Event | Coordinate | Role |
|---|---:|---|
| `EV_Visual_FracturedRing` | `(14,6)` | Ring registration |
| `EV_FX_DustTremor` | `(14,12)` | Dust/shake reference |
| `EV_Camera_Chamber` | `(14,10)` | Chamber framing |
| `EV_Camera_Ring` | `(14,8)` | Ring framing |

## Explicit exclusions

The event lists contain no dialogue, transfer, battle, inventory, choice, script, plugin, character, location/date label, explanation, reward, or completion of the full closing montage.
