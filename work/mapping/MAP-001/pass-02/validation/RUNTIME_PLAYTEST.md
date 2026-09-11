# MAP-001 Pass 02 — Runtime Playtest

Use a newly created blank RPG Maker MZ project. Keep the whole `pass-02` directory together; the installer resolves its assets relative to the `eventwright` folder.

## Install

1. Create a blank RPG Maker MZ project named `Eryndra_MAP001_Review`, then close the editor.
2. From `work/mapping/MAP-001/pass-02/eventwright`, run:

   ```text
   py install_into_blank_mz_project.py "C:\full\path\to\Eryndra_MAP001_Review"
   ```

   If `py` is unavailable, use `python` instead.
3. Open the review project's `.rmmzproject` file. Confirm Map 001 is named `Forgotten Watcher Station` and its tileset is `Cinematic Parallax Collision`.

## Opening sequence

1. Start a New Game.
2. Let the complete opening run without pressing through it.
3. Confirm:
   - no player or follower becomes visible;
   - movement and menu input cannot interrupt the autorun;
   - the screen begins black and slowly reveals the chamber;
   - the whole ring is visible before and after the northward reframe;
   - the reframe exposes no map edge;
   - the dust tremor remains restrained;
   - the ring gives one full pulse with its top division black;
   - exactly three low tones play, with equal silence and no clipping;
   - the pulse dies completely, darkness holds briefly, and one narrow residual arc returns;
   - the scene cuts to black and `ERYNDRA` appears alone against black;
   - the sequence ends on black without replaying.
4. Press F9 after the sequence. Confirm Switch 100 and Switch 101 are ON and Variable 1 equals 1002.

## Closing-omen controller

The opening leaves the camera in the ring frame, so reset the camera before testing the closing controller.

1. Return to the running map after the opening check and press F8 to open the playtest developer tools.
2. In the Console, paste this one line and press Enter:

   ```javascript
   $gamePlayer.locate(14,10); $gamePlayer.center(14,10); $gameVariables.setValue(1,1012);
   ```

3. Return focus to the game window. Confirm:
   - the same chamber reveals from black;
   - the camera reframes north without exposing an edge;
   - substantially more of the ring lights while the top division stays black;
   - the same three-note phrase plays exactly once;
   - the scene holds for the future distant answer, fades to black, and does not replay.
4. Press F9. Confirm Switch 112 remains OFF and Variable 1 remains 1012.

## Evidence to return

- One screenshot of the opening pulse or residual state.
- One screenshot of the closing propagated state.
- A short note stating PASS or FAIL for player visibility, camera alignment, title background, three-note playback, timing, and final state values.
- A short video of the opening is welcome and can replace the first screenshot plus the timing/audio note.

Do not run this installer against either supplied ZIP or any extracted reference-project directory.
