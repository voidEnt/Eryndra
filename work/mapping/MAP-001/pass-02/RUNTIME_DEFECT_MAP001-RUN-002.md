# MAP001-RUN-002 — Reveal tint rendered the chamber unreadably black

**Observed in live RPG Maker MZ playtest:** 2026-09-12

## Symptom

MAP-001 contained the chamber image and camera crop, but the opening appeared black. Entering `$gameScreen.startTint([0, 0, 0, 0], 1)` in the live MZ developer console immediately revealed the chamber.

## Cause

The source parallax is deliberately dark. The controller then applied the additional tone `[-96, -96, -112, 48]`, which removed nearly all visible detail from that source at runtime.

## Correction

Both opening and omen controllers now reveal to `[-24, -24, -28, 8]`: still dark and cold, but readable. Static validators now require that exact readable-dark tone.

## Required regression evidence

Start a fresh New Game after applying this revision. The chamber must become visible during the first 0.5–3.5 seconds, before the northward ring reframe.
