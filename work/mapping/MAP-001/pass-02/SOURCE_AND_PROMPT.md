# MAP-001 Pass 02 - Source and Process Record

## Original approved visual master

- Git-facing source preview: `source/MAP001_Approved_Concept.jpg`
- Status: Foreman-approved generated concept
- Original dimensions: 1474x1067 RGB
- Canon basis: `PrologueStoryv0.3`, P-01 and P-08
- Geometry basis: accepted MAP-001 Mapping Pass 01

The approved concept was generated with the built-in image-generation tool from the accepted Map001 tile-composite geometry reference. Its Git-facing JPEG is a high-quality visual provenance preview; the untouched lossless source remains in the local production archive.

## Recorded generation prompt

> Use case: stylized-concept  
> Asset type: RPG Maker MZ parallax environment art for MAP-001, Forgotten Watcher Station  
> Transform the supplied exact 29x21 tile map composite into a polished late-16-bit / 32-bit top-down JRPG cinematic chamber while preserving its rectangular one-room geometry, wall boundaries, floor footprint, camera orientation, and black outer buffer. Impossibly ancient and abandoned for centuries: precise fitted dark stone, sparse dull unfamiliar metal, fine dead roots through hairline seams mainly on east/right wall, undisturbed dusty floor with no footprints. Center one dominant solid circular ring on the north wall with a single narrow intentional black fracture at the top; wall remains behind its opening, so it is clearly not a doorway or portal. Ring dormant and almost dark, no runes. Crisp hand-painted pixel-art environment, tile-readable, restrained detail, cold slate and charcoal, ominous near-dark ambient visibility. Preserve source aspect and coordinate alignment, north wall above, open floor below, sealed south foreground. No added rooms, exits, characters, creatures, corpses, furniture, treasure, doors, stairs, altar, throne, books, readable text, religious symbols, runes, sigils, torches, braziers, daylight, active machinery, glowing magic, footprints, UI, labels, or watermark.

## Canon-corrected intermediate

- Intermediate lossless source: retained in the local production archive outside the Git-facing pass directory
- Method: two built-in image-editing passes
- Reason: the original concept's jagged vertical crack read as accidental damage and extended into the wall, contrary to P-01 and the MAP-001 work orders

First correction prompt:

> Repair only the jagged vertical crack that runs through and above the large circular ring. Replace the damaged wall above the ring and the wall visible inside/behind the ring with continuous fitted dark masonry matching the existing surrounding bricks. Replace the irregular broken ring gap with one clean, narrow, symmetric engineered division confined strictly to the ring's metal/stone band at the 12 o'clock position. The division should look deliberately manufactured: straight, precise, and narrow, with clean aligned edges. Preserve the exact room layout, camera, scale, ring center and radius, columns, floor rectangle, black perimeter, object positions, darkness, colors, textures, roots, dust, dull metal, and sealed-room appearance. The division must stop at the inner and outer edges of the ring band. Add no symbols, runes, text, doors, lights, characters, or geometry.

Second correction prompt:

> Remove only the unintended vertical seam/gap at the six-o'clock bottom of the circular ring. Reconstruct that tiny bottom segment as continuous uninterrupted ring material matching the adjacent ring blocks and shading. Keep the single clean narrow engineered division at 12 o'clock exactly as it is. Keep the repaired continuous masonry above and behind the ring and preserve all other content, geometry, lighting, crop, and textures.

These edits repaired the natural crack, but the resulting ring remained too high for the approved default camera frame. The intermediate is preserved for provenance and is not the runtime source.

## Canon-corrected camera-fit master

- Runtime source: `source/MAP001_CanonCorrected_CameraFit.jpg`
- Source dimensions: 1474x1067 RGB, high-quality JPEG provenance copy
- Final map-space ring center after resize: approximately `(691,280)`
- Final map-space visual bounds after resize: approximately `x=617..765`, `y=214..346`

Camera-fit correction prompt:

> Move the complete circular ring lower on the same north wall and reduce it modestly so the entire ring fits inside the map rectangle x=576..815 and y=192..383. Target ring center approximately x=697, y=280 in the 1392x1008 input, with outer radius approximately 80 pixels. Remove the old larger/higher ring cleanly and restore matching fitted masonry where it was. Keep the ring solid-backed by continuous masonry. Preserve one and only one clean, narrow, engineered black division confined to the ring band at 12 o'clock. Preserve the left and right ring mounting supports if possible, scaled and moved consistently with the ring. Keep the exact scene, room geometry, floor, roots, black perimeter, lighting, textures, and all non-ring positions unchanged. No crack or seam may extend into the wall. The bottom of the ring must be continuous.

The camera-fit result keeps the complete ring within both approved 816x624 camera frames. It contains one top division, continuous backing masonry, preserved side supports, and no bottom gap.

## Build process

Run from this directory:

```bash
python3 build_assets.py
```

The script uses Pillow to resize the camera-fit master to the exact 29x21-tile parallax size, derive aligned elliptical ring and dust overlays, render the title card, and create the transparent collision sheet. It synthesizes the three-note source waveform in Python and invokes `ffmpeg` only for OGG/Vorbis encoding. The base parallax uses an adaptive indexed palette, while review composites use high-quality RGB JPEG so the cyan illumination remains faithful within the connector's 700 KiB per-file transport ceiling. Images and manifest/database JSON are published through temporary files and atomic renames.

The ring center, horizontal/vertical radii, and fracture gap were measured from the camera-fit master after scaling. Every illuminated ring state omits the deliberate top fracture. Dust placement uses a fixed random seed. Review images are rebuilt from the same runtime files.

## Source and license notes

The concept and corrections were generated specifically for Eryndra. No stock image from either immutable reference ZIP is copied into these outputs. Lossless PNG source masters remain preserved in the local production archive outside the Git-facing directory; compact high-quality JPEG provenance copies are versioned with the pass. Final project distribution metadata remains subject to the Foreman's normal release review.
