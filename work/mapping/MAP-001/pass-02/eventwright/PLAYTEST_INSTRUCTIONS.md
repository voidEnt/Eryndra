# MAP-001 Pass 02 — Local RPG Maker MZ Playtest

Runtime playtesting must use a newly created, user-owned blank RPG Maker MZ project. Do not point the installer at either reference ZIP or an extracted reference project.

## Install

1. In RPG Maker MZ, create a new blank project and close the editor.
2. Keep this entire `pass-02` package together so the installer can see both `eventwright/` and `assets/`.
3. Run:

   ```text
   python install_into_blank_mz_project.py "C:\full\path\to\your\blank\project"
   ```

4. The installer verifies that the target has only a blank Map 001, then creates a timestamped backup under `.eryndra-backups/` before changing project files.
5. Open the target project's `.rmmzproject` file. Map 001 should be named `Forgotten Watcher Station` and use tileset `Cinematic Parallax Collision`.

## Opening test — fresh New Game

1. Start a New Game without changing switches or variables.
2. Confirm the player and followers never appear and movement/menu input cannot interrupt the autorun.
3. Confirm the view starts black, reveals the abandoned chamber slowly, reframes toward the wall ring, and shows a restrained dust tremor.
4. Confirm one full ring pulse appears.
5. Confirm exactly three low notes play from a single sound effect, with equal silence between notes.
6. Confirm the pulse clears, a narrow residual line remains briefly, and the screen fades to black.
7. Confirm `ERYNDRA` appears alone and fades away.
8. Confirm the proof build remains cleanly black without looping. This is the unresolved MAP-002 handoff, not a freeze.
9. During a test play with the developer console/debug tools, verify Switch 100 and 101 are ON and Variable 1 equals 1002.

## Closing-omen test — controlled debug state

Use a fresh test instance or erase MAP-001 Self Switch A before this test.

1. Set Switch 101 `PRO_WatcherStation_Awakened` ON and Variable 1 `SYS_StoryStage` to 1012 before MAP-001's events refresh. Leave Switch 112 OFF. Switch 101 disables the opening controller, matching the state produced by normal Prologue progression.
2. Enter or restart MAP-001 at `(14,10)`.
3. Confirm the same chamber reveals and reframes toward the ring.
4. Confirm substantially more of the ring is illuminated while the narrow fracture stays black.
5. Confirm the same three-note cue plays once.
6. Confirm the scene holds briefly for the future distant answer, fades to black, and does not loop.
7. Verify Switch 112 remains OFF and Variable 1 remains 1012. The proof build must not declare the full Prologue complete.

## Visual checks in both entries

- No character, label, date, rune, readable explanation, exit, treasure, furniture or active machinery appears.
- Camera motion does not expose a map edge.
- Ring overlays align with the wall ring throughout the ring-camera shot.
- The pulse, residual and propagated states are clearly distinct.
- The title is centered and readable against black.
- Audio is restrained and free of clipping or an unintended fourth tone.

Capture one opening screenshot, one propagated-state screenshot, and a short playtest note recording PASS/FAIL for timing, alignment, audio and state behavior. Actual runtime evidence is required before MAP-001 is considered built.
