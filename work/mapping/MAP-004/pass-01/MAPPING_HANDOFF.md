# MAP-004 Mapping Pass 01 — Mapper handoff

**Status:** Candidate for separate Validator, not accepted.  
**Work order:** `docs/design/maps/MAP-004_Brackenford_Survey_Office_Blueprint.md`.  
**Product:** `Map004.json`, 25×19 Inside-ID-3 office, single front door at `(12,16)`, clear interior arrival `(12,15)`.

Eight inert anchors have exact IDs, names and positions from the blueprint. Intended two-scene occupancy: Joren `(16,8)` behind the record desk `(16,9)`, Edrin `(9,11)`, Marek's staging `(12,12)`. All underlying anchor pages contain only the stock terminal command. Player can walk from arrival to desk front `(16,11)`, around west of counter to `(15,8)` adjacent to Joren, and to Edrin. Same geography is available for the afternoon report. No MAP-003 or MAP-002 file was changed.

**Self-check:** `tools/validate_map004.py` reports 10/10 checks passed and 195 reachable walkable tiles from arrival. This uses event records parsed from the work order, not just the generator table; full-map and camera-sized views were reviewed. A separate Validator still needs to test tile rendering/passability in RPG Maker MZ, scene framing, office atmosphere, exact work-order compliance and any defects the mapper missed. Runtime dialogue/transfer correctness belongs to Eventwright and later Validation.

**Known limitation:** The stock desk/cabinets are generic. They do not visibly identify the corrected boundary measurements or a written ledger; those details must come from canon-faithful Eventwright dialogue, or a separately authorized small prop asset. Do not invent text or diagram labels to compensate.

**Next gate:** Validator reports PASS/FAIL with defects assigned to Mapping or requirements. Only after a Mapping PASS may Eventwright implement morning/evening pages and the bidirectional MAP-003 office transfer in the cumulative review project. Outside office arrival is MAP-003 `(31,16)` facing south; inside arrival is `(12,15)` facing north. No transfer has yet been installed.
