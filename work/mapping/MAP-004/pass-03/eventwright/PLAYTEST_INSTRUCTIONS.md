# MAP-004 Eventwright Runtime Playtest

Run these checks only after independent static Validation approves the Eventwright candidate.

## Install

From this directory, use the existing cumulative Eryndra review project—not a new project per map:

```powershell
py install_into_eryndra_review.py "C:\full\path\to\Eryndra_MAP001_Review" --dry-run
py install_into_eryndra_review.py "C:\full\path\to\Eryndra_MAP001_Review"
```

The installer creates a timestamped `.eryndra_backups\MAP-004-eventwright-*` folder before changing project data. Both source/reference ZIPs are prohibited targets.

## Morning path

1. Start or load the cumulative build at MAP-003 with `SYS_StoryStage=1003`.
2. Confirm MAP-003 office door interaction changes the stage to `1004` and transfers to MAP-004 `(12,15)`, facing north, with black fade.
3. Confirm Marek walks three tiles north and stops at `(12,12)`.
4. Confirm Joren and Edrin are visible and distinct; Latch is absent.
5. Read all nine message boxes. Check speaker labels, exact order, and that no text clips horizontally.
6. Confirm completion sets switch 103 ON and stage `1005`, then releases player control.
7. Confirm Edrin disappears after the assignment and the scene does not replay on movement, save/load, or re-entry.
8. Use the office door and confirm return to MAP-003 `(31,16)`, facing south.

## Afternoon path

1. In a test save/debug setup, enter the MAP-003 office door at exact stage `1010` with switch 110 OFF.
2. Confirm entry does not alter stage 1010 and the report begins once after transfer.
3. Confirm Marek stages at `(12,12)`; Joren and Edrin are visible; Latch remains absent.
4. Read all thirteen messages. Check speaker labels, exact order, em dash display, and horizontal wrapping.
5. Confirm completion sets switch 110 ON and stage `1011`, then releases player control.
6. Confirm the report never replays on movement, save/load, or re-entry.
7. Confirm the office door returns to MAP-003 `(31,16)`, facing south.

## Regression

- Walk the accepted office paths and verify furniture/wall collision is unchanged.
- Confirm MAP-003 tiles and every event other than office door ID 2 behave as before.
- Confirm there is no three-note cue, shake, tint, supernatural graphic, combat, reward, extra quest or ominous music in the office.

Record observed failures with reproduction steps and assign them to Eventwright unless the defect is demonstrably spatial.
