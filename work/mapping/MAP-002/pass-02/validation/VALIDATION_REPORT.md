# MAP-002 Independent Eventwright Validation Report

**Production unit:** `MAP-002 Brackenford - Venn Home`  
**Pass:** Eventwright Functional Spine Pass 01  
**Scenes:** `PRO-SC-002 Morning at the Venn House`; `PRO-SC-011 Home, But Changed`  
**Validation role:** Independent Validator  
**Static Eventwright outcome:** **PASS**  
**Overall handoff outcome:** **CONDITIONAL PASS — user-side RPG Maker MZ runtime evidence required**

## Scope and authority

Validation compared the candidate implementation against:

- locked `PrologueStoryv0.3` P-02 and P-07
- locked `Player1Backgroundv0.2` Venn household and voice guidance
- the Implementation Bible and Production Roles & Handoff Contract
- approved `MAP-002 Eventwright Work Order`
- accepted MAP-002 Mapping Pass 01 baseline
- accepted and runtime-tested MAP-001 Eventwright baseline
- stock RPG Maker MZ command and passage semantics inspected read-only from `SampleGenerated.zip`

No Eventwright-owned file was changed during Validation. Validator artifacts are isolated in this directory.

## Validated artifacts

| Artifact | SHA-256 |
|---|---|
| Accepted MAP-001 baseline | `f6b6a5f5e90d4f48b3b886ee5b23a09a86fba802e4d28c3cacfbf5468d4a39f6` |
| Accepted MAP-002 Mapping baseline | `429310b40f87053f669aca5377cd0544604d929b0e828a754d6ef966f78cdcd7` |
| MAP-001 transfer-patched candidate | `98fec8f89e190531e5de74b525574769b59c79c2030a9fd2ac9a906c47d623cd` |
| MAP-002 Eventwright candidate | `23b0c50b6323ca8eb1fd189b20caed7c6732cde54932ea2f1526f1cd4f6ac9ad` |

The deterministic builder reproduced both candidate files byte-for-byte.

## Independent results

The independent validator completed **62/62 checks with no static defects**.

Validated requirements include:

- MAP-002 tile data, dimensions, tileset, map properties, and all 17 anchor identities/coordinates remain preserved.
- MAP-001 differs from its accepted baseline only at the authorized `PRO-SC-002` transfer tail.
- The MAP-001 opening still writes `SW101 ON`, then `VR1=1002`, before transferring to MAP-002 `(14,14)`, facing north, with no transfer fade.
- Morning and Evening use page-level eligibility plus exact internal equality checks and OFF-switch checks.
- Higher completion pages prevent both autoruns from replaying at later story stages.
- Morning and Evening each contain all 22 approved dialogue lines in exact speaker and beat order.
- Faces, sprites, speaker names, ambient family lines, and Latch restrictions match the work order.
- All used event-command and movement-route arrays match the stock MZ schemas relevant to this pass.
- Morning's 28 movement steps satisfy directional tile passage and avoid the staged NPC collision cells.
- Morning writes only `SW102 ON` and `VR1=1003`, then leaves Marek visible and followers hidden at `(14,14)`.
- Evening stages four distinct supper positions and the exact bedroom composition.
- Latch is silent during the final beat and the faint three-note cue occurs exactly once.
- The 3.4-second cue timing provides approximately 120 silent frames after the cue before the final fade.
- Evening writes only `SW111 ON` and `VR1=1012`, then transfers under black to MAP-001 `(14,10)`, facing south, with no transfer fade.
- No guessed MAP-003 transfer, new global IDs, inventory, combat, shop, script, plugin, quest, or reward behavior was introduced.
- Deterministic rebuild and guarded installer behavior passed independently.
- Installer archive/reference refusals, missing-dependency refusal, wrong-baseline refusal, dry-run immutability, recoverable backups, exact replacement, and two-file rollback all passed.

Machine-readable detail is recorded in `independent_results.json`; the concise transcript is `independent_results.txt`.

## Immutable source verification

| Immutable input | Expected and observed SHA-256 | Result |
|---|---|---|
| `EryndraStory.zip` | `56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611` | PASS |
| `SampleGenerated.zip` | `b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768` | PASS |

Neither archive was modified. `SampleGenerated` remains a read-only technical reference.

## Defects

No static blocking or nonblocking defect was found in the submitted Eventwright scope.

## Open runtime acceptance conditions

These are not static defects. They are required evidence that cannot be established by JSON inspection alone.

| ID | Runtime condition | Owner | Blocking for final Eventwright acceptance? |
|---|---|---|---:|
| `MAP002-VAL-C01` | MAP-001 opening presentation remains unchanged and transfers cleanly under black into Morning | Validation/user playtest | Yes |
| `MAP002-VAL-C02` | Morning staging, dialogue, movement, interaction, control release, state, passability, save/load, and no-replay behavior work in MZ | Validation/user playtest | Yes |
| `MAP002-VAL-C03` | Evening staging, dialogue, supper, bedroom framing, silent Latch, one faint cue, wake, final silence, and black handoff work in MZ | Validation/user playtest | Yes |
| `MAP002-VAL-C04` | Evening final state and MAP-001 Omen entry are correct; completed Evening does not replay after save/load | Validation/user playtest | Yes |

## Required user-side RPG Maker MZ tests

### Test A — MAP-001 into Morning

1. Install into a newly created Eryndra review project using the guarded installer. Do not use either source ZIP or any `SampleGenerated` tree.
2. Start a New Game on MAP-001 `(14,10)`.
3. Confirm the previously accepted MAP-001 chamber, pan, three notes, pulse/residual ring, fade, and `ERYNDRA` title are unchanged.
4. Confirm the title clears under black and MAP-002 fades in with the household staged correctly.
5. Confirm the exact Morning dialogue, one restrained dog sound, crooked-latch action, field-kit route, and two inspection motions.
6. Confirm control releases with Marek visible at `(14,14)` and followers hidden.
7. Check all required household routes and family action lines. The south door must not transfer to MAP-003.
8. In F8 Console, run:

```javascript
[$gameMap.mapId(), $gameSwitches.value(101), $gameSwitches.value(102), $gameVariables.value(1), $gamePlayer.isTransparent(), $gamePlayer.followers().isVisible()]
```

Expected:

```text
[2, true, true, 1003, false, false]
```

9. Save, load, and confirm Morning does not replay.

### Test B — Evening direct setup

From an active map playtest, use this one-line F8 setup:

```javascript
$gameSwitches.setValue(110,true);$gameSwitches.setValue(111,false);$gameVariables.setValue(1,1011);$gamePlayer.reserveTransfer(2,14,19,8,2);SceneManager.goto(Scene_Map);
```

Confirm:

1. Marek and muddy Latch appear at the entry; Latch does not bark.
2. The exact entry, shutter, and supper exchanges play in order.
3. Four distinct supper positions read clearly.
4. The bedroom composition shows Marek asleep and Latch at `(19,9)`, facing north.
5. The three-note cue plays once at faint volume; Marek changes pose without leaving the bed; no explanatory dialogue appears.
6. Silence follows and the screen fades fully black before the MAP-001 transfer.
7. MAP-001's existing Omen controller begins.
8. During the MAP-001 arrival, run:

```javascript
[$gameMap.mapId(), $gameSwitches.value(110), $gameSwitches.value(111), $gameSwitches.value(112), $gameVariables.value(1)]
```

Expected at handoff:

```text
[1, true, true, false, 1012]
```

9. Repeat from a fresh setup and test a save/load after `SW111=true`; Evening must not replay.

## Verdict

The Functional Spine Pass 01 is structurally, narratively, and technically suitable for user-side MZ playtesting. It receives **STATIC PASS / OVERALL CONDITIONAL PASS**. Final Eventwright acceptance requires closing `MAP002-VAL-C01` through `MAP002-VAL-C04` with observed runtime evidence.
