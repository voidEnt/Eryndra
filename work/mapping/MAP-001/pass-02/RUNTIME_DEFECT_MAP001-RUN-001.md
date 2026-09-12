# MAP001-RUN-001 — Full-map parallax pinned to screen

**Observed in live RPG Maker MZ playtest:** 2026-09-12

## Symptom

The opening showed an almost entirely black screen with only a sliver of chamber wall, while the MZ editor displayed the full map correctly. No JavaScript console error occurred.

## Cause

The map parallax name began with `!`. In RPG Maker MZ, that prefix means a zero/screen-fixed parallax. MAP-001's base image is a 29×21-tile, map-sized image with a black outer buffer, so pinning its upper-left corner to the screen bypassed the intended player-camera crop.

## Correction

The MAP-001 event source now uses `MAP001_WatcherStation_Base` without the prefix, and the installer writes the asset to `img/parallaxes/MAP001_WatcherStation_Base.png`. The normal map camera therefore selects the chamber crop during the opening and ring crop after the northward scroll.

## Required regression evidence

Reinstall into a new blank MZ review project, then verify that the chamber appears during the first 0.5–3.5 seconds of a New Game. Continue the existing opening and closing-omen checks in `validation/RUNTIME_PLAYTEST.md`.
