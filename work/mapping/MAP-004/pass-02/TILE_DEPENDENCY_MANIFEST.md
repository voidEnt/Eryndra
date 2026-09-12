# MAP-004 Pass 02 stock tile delta

Baseline dependencies in `../pass-01/TILE_DEPENDENCY_MANIFEST.md` continue. The correction uses stock `Inside_A4.png` tile `7048` for a fully blocked lower boundary (`0xE0F` in tileset ID 3), and stock `Inside_B.png` tile `91` for a small generic parchment at `(11,5)` and `(16,9)`. Desk stock tile `116` now occupies layer 2 beneath the parchment at `(16,9)`; it remains visually contiguous and impassable. No new file references, images, custom art, database slots or plugins were introduced. The reference ZIPs remain read-only.
