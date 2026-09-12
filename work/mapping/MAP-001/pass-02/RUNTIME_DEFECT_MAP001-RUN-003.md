# MAP001-RUN-003 — Transparent pictures never became visible

**Observed in live RPG Maker MZ playtest:** 2026-09-12

## Symptom

The three-note cue and shake ran, but the full ring pulse never appeared and the title never appeared. Only the residual arc was visible because it was shown directly at nonzero opacity.

## Cause

Generated event command 232 (Move Picture) contained 12 parameters instead of MZ's required 13. The missing y-coordinate field shifted scale, opacity, blend, duration and wait one slot left. MZ therefore read target opacity as zero, leaving the full pulse and title transparent.

The schema was verified against the supplied MZ runtime's `Game_Interpreter.command232`: picture ID, reserved field, origin, coordinate-designation mode, x, y, scale X, scale Y, opacity, blend mode, duration, wait and easing.

## Correction

All six Move Picture commands now use the 13-field MZ layout. Eventwright and independent validators compare the complete parameter arrays rather than merely checking that command 232 exists.

## Required regression evidence

A fresh New Game must show a nearly complete cyan ring throughout the three-note cue, then a brief dark beat, the small residual arc, a fade to black, and the `ERYNDRA` title.
