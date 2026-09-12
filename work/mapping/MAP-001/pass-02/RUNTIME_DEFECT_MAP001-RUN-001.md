# MAP001-RUN-001 — Retracted parallax diagnosis

**Status:** RETRACTED on 2026-09-12; retained so the diagnostic history is not silently rewritten.

The first black-screen diagnosis incorrectly attributed the failure to the parallax name's `!` prefix. Live testing after removing the prefix showed the chamber beginning at its upper-left corner and the blue ring overlay only partially entering view. That evidence demonstrates that removal broke the approved map/camera alignment.

For this map-sized, non-looping RPG Maker MZ parallax, the `!` prefix selects zero-parallax handling whose origin follows the map display coordinates one-for-one. MAP-001 therefore requires both:

- map data name `!MAP001_WatcherStation_Base`
- installed file `img/parallaxes/!MAP001_WatcherStation_Base.png`

The confirmed black-screen cause is `MAP001-RUN-002`: the added reveal tint was too dark for the already-dark artwork. The final candidate restores the prefix and keeps the lighter readable-dark tone.
