# MAP-001 Pass 02 — Independent Validation Report

**Scope:** Asset + Eventwright proof build for `PRO-SC-001`, with the MAP-001 portion of `PRO-SC-012`  
**Static verdict:** PASS  
**Opening runtime verdict:** PASS — `PRO-SC-001` Tested and approved for integration  
**MAP-001 overall acceptance:** CONDITIONAL — MAP-002 transfer and `PRO-SC-012` integration remain

## Controlling inputs

- Locked `PrologueStoryv0.3`, P-01 and P-08
- Eryndra Implementation Bible and Production Roles & Handoff Contract
- MAP-001 Mapper, Asset, and Eventwright work orders
- Accepted MAP-001 Mapping Pass 01 handoff
- RPG Maker MZ 1.10.0 runtime files inspected read-only from `SampleGenerated.zip`

## Independent results

| Check set | Result |
|---|---:|
| Asset producer validation | 81/81 PASS |
| Eventwright producer validation | 40/40 PASS |
| Installer producer tests | 4/4 PASS |
| Independent Validator checks | 50/50 PASS |

The independent checks cover source/archive immutability, manifest hashes, full runtime and review-image decoding, map dimensions and collision substrate, six stable anchors, page gates, state writes, forbidden command classes, title sequencing, the pause before residual light, parallax naming, both camera frames, measured audio timing and headroom, successful blank-project installation, refusal without target-tree mutation, and the 700 KiB Git-facing file ceiling.

## Corrections required during Validation

Validation returned four defects upstream. All four were corrected and rechecked:

1. The original ring fracture looked like accidental structural damage and continued into the wall. The Asset worker replaced it with one clean engineered division confined to the ring's twelve-o'clock band.
2. The initial chamber frame cut off the upper part of the ring. The Asset worker moved and resized the ring so its visual bounds `(617,214)..(765,346)` remain within both approved 816×624 camera frames.
3. The title sequence would have revealed the chamber behind `ERYNDRA`. The Eventwright inserted a full-black base tint before the title Fade In.
4. The residual light appeared immediately after the pulse died. The Eventwright inserted a 24-frame dark pause to preserve P-01's “a moment later” timing.

The installer was also corrected so all occupied-ID checks occur before backups or writes. Rejected installs now leave the complete target tree unchanged. Asset generation uses atomic replacement, and every runtime PNG, review JPEG, and manifest hash is fully verified. The final packaging pass retains cyan overlay color while keeping every Git-facing file below 700 KiB; the largest file is 521,623 bytes.

## Canon and presentation review

The final camera composites show one sealed abandoned chamber, fitted stone, dull ring material, undisturbed dust, dead roots at fine seams, and no character, exit, furniture, treasure, inscription, rune, religious symbol, or explanatory label. The ring has solid masonry behind it and does not read as a doorway. Dormant, pulse, residual, and propagated states are distinct; the sole top division remains black in the illuminated states.

The OGG decodes as mono Vorbis at 48 kHz and 3.4 seconds. Independent waveform analysis found exactly three 0.55-second active tone regions beginning at 0.20, 1.40, and 2.60 seconds. Both onset intervals are 1.20 seconds. Peak level is approximately −11.72 dBFS before the event's 80% SE volume, leaving ample headroom.

## RPG Maker MZ semantic review

The command arrays match the MZ 1.10.0 interpreter schema. Autorun is trigger `3`; switch, variable, self-switch, transparency, follower, tint, scroll, picture, shake, fade, wait, and SE commands use the expected parameters. MZ selects the last valid event page, so the opening's SW101 page and the omen's Self Switch A / SW112 pages stop replay as intended.

**Runtime correction (2026-09-12):** `MAP001-RUN-001` was a retracted diagnosis. Live testing proved that removing the `!` prefix makes the map-sized parallax remain at its upper-left while the screen-space overlay moves independently. MAP-001 therefore restores `!MAP001_WatcherStation_Base`, which gives one-for-one map/display alignment for this zero-parallax resource. The confirmed black-screen cause was `MAP001-RUN-002`: `[-96, -96, -112, 48]` crushed the already-dark art. Both controllers now reveal to `[-24, -24, -28, 8]`. At the installed player reference `(14,10)`, the 816×624 chamber frame begins at map pixel `(288,192)`; scrolling north two tiles produces the ring frame at `(288,96)`. Prior acceptance remains superseded until this combined correction receives a fresh live MZ retest.

The opening writes SW100 ON and V1=1001, then finishes with SW101 ON and V1=1002. The closing proof controller requires V1≥1012, sets local Self Switch A, and deliberately leaves SW112 OFF and V1 at 1012 until the future multi-map P-08 montage exists.

## Runtime defect MAP001-RUN-003

Live MZ testing proved that the full pulse and title stayed transparent while the directly shown residual arc appeared. The generated command 232 arrays had 12 fields rather than the 13 consumed by MZ's `Game_Interpreter.command232`; the missing y field shifted opacity to zero. All six Move Picture commands now use the verified MZ schema, and both static validators require their exact arrays. This correction supersedes prior picture-transition acceptance until live retesting.

## Runtime acceptance

The Foreman-observed live RPG Maker MZ test confirmed the chamber reveal and framing, northward camera reframe, three-note cue, restrained shake, full cyan pulse with its dark division, pulse extinction and residual arc, black transition, and `ERYNDRA` title. The final console state was `[true, true, 1002]`, confirming SW100 ON, SW101 ON, and VR1=1002.

The independent Validator therefore assigns **PASS** to the `PRO-SC-001` opening. It is **Tested** and approved for integration. All three recorded opening runtime defects are closed.

MAP-001 overall remains **CONDITIONAL**. The transfer to MAP-002 is intentionally absent until the destination is approved, and `PRO-SC-012` still requires runtime and multi-map integration acceptance. SW112 and advancement to Act I remain deferred by design. MAP-001 is not Locked.

## Frozen artifact hashes

- Base parallax: `4fb64a66a9beabf1994f71abe526c1b3b2c3a59fb11435a57ee8a3f4ae9693f1`
- Asset manifest: `fbb2b92eb170a128c3460617c2a7326ca9ece87387a56a5409ddbd1b14bb954a`
- Ring-state contact sheet: `df5d6e710db6583a4335e667136c14a45d836ad56eb9586e7f26b71a5501e0f3`
- Eventwright Map001: `9eb52bb228437fa47c13746abb74074f9bd8c6ef2b0bfebfdd02c155e3616e47`
- Installer: `a1ae5c3e9e9cd25e6dfbcbf6a539f5a65c77b75eb92d53665485c6ca97aaa9ce`
- `EryndraStory.zip`: `56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611`
- `SampleGenerated.zip`: `b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768`
