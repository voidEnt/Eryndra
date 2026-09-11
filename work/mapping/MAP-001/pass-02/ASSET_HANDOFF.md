# MAP-001 Asset Pass 02 - Handoff

**Assigned:** Build the approved MAP-001 visual/audio package for Eventwright integration without changing map geometry or event logic.

**Produced:** The exact 1392x1008 base parallax, three 816x624 ring-state overlays, one 816x624 dust overlay, the 816x624 title card, transparent 768x768 collision sheet, Tileset 7 database fragment, three-note OGG cue, deterministic build/validation scripts, manifest, source record, and camera review composites.

**Repository packaging:** Every Git-facing Pass-02 file is at or below 700 KiB. The runtime base uses an adaptive indexed PNG palette without changing dimensions or alignment. Review composites use high-quality RGB JPEG so the cyan runtime illumination remains visible and accurate. High-quality JPEG provenance copies replace oversized lossless sources in the Git-facing package; the lossless originals remain preserved locally outside it.

**Requirements satisfied:** The approved generated concept remains the composition source. Its canon-defective natural crack was repaired through controlled image edits: masonry is continuous above and behind the ring, and the ring has one clean engineered division confined to its twelve-o'clock band. The ring was moved lower and reduced so its complete visual bounds fit both approved camera frames. The ring states are distinct and aligned to the approved ring-camera frame. The deliberate top division is fully transparent in every illumination overlay. The base retains fitted stone, dull unfamiliar ring material, dust without footprints, dead roots, a sealed room, and no forbidden content.

**Remaining integration checks:** Runtime picture placement, screen tint/brightness, cue volume, and MZ playback require Eventwright integration and playtest. `SOURCE_AND_PROMPT.md` records the original generation prompt and all three correction prompts.

**Next-role note:** The four picture effects are authored in 816x624 screen space for the ring camera whose map origin is `(288,96)`. Show them at screen origin `(0,0)` only while that camera frame is active. The base image is a map-sized parallax and the collision sheet/fragment control invisible walkability.
