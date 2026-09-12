# MAP-004 Mapping Pass 02 — Mapper correction handoff

**Controlling work order:** `docs/design/maps/MAP-004_Brackenford_Survey_Office_Blueprint.md`.  
**Defect authority:** `work/mapping/MAP-004/pass-01/validation/VALIDATION_REPORT.md`.  
**Candidate:** `Map004.json` plus three stock-sheet previews; no live dialogue, transfer, visual effect or project install.

- **D1:** Changed south boundary 16 tile cells at `y=16`, all but door `(12,16)`, from stock ID `6785` (directional flag `0xE08`) to ID `7048` (`0xE0F`, four-way blocked). Result is a solid bottom sill with only one doorway. Mapper regression models actual MZ source/destination directional movement from arrival through doorway and checks both left and right wall travel are impossible.
- **D2:** Added stock B tile `91`, a small unlabelled parchment, at `(11,5)` as mundane pinned office chart/record; one more unlabelled parchment on the existing ledger worktop `(16,9)`, keeping its desk graphic underneath on layer 2. No invented legible map geography, ancient clue, quest or interactable item. Visual review confirms ordinary records at 816×624 framing.

No other map data changed: 19 tile-layer cell edits total (16 boundary tiles, one wall-paper tile, two desk-paper/layer tiles). All eight event IDs/names/coordinates and inert pages remain identical. Mapper regression: **7/7 PASS, 194 reachable cells**. This is the Mapper's self-check; independent Validator and runtime inspection are separate gates.

The sample and story ZIPs are unchanged. Eventwright may not treat this as accepted until Validator confirms both corrections and the full Mapping work order.
