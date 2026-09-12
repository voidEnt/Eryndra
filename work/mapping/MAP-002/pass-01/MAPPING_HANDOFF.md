# MAP-002 Mapping Pass 01 Handoff

## Result

The Venn home spatial skeleton is ready for independent Validation. It is a
single modest household organized around a central common room, with three
sleeping spaces, a narrow connecting hall, an open kitchen, Davren's compact
repair nook and one south-facing mud entry.

## Narrative/style review

The Mapper rechecked `PrologueStoryv0.3` sections P-02 and P-07 and
`Player1Backgroundv0.2` section "The Venn Household" before construction.
The result emphasizes ordinary repair-minded family life. It adds no shrine,
magic, fractured-ring imagery, library, weapon display, hidden room, treasure,
second exit or supernatural implication.

## Geometry compliance

- Canvas: `29x23`; authored footprint remains within `x=4..24`, `y=2..20`.
- Parents: west bedroom; shared bed and small cabinet.
- Nessa: compact center bedroom; single bed and dresser.
- Marek: east bedroom; simple bed and small neutral work surface.
- Hall: direct three-door connection to the common level.
- Kitchen: west side, open to the household center.
- Common room: centered table with four stock wooden stools and clear routes.
- Repair nook: east side with hand tools, small surface, wood and crate clutter.
- Entry: one south door, open latch position and clear Latch floor space.
- All 17 work-order anchors use exact IDs, names and coordinates.

## Camera verification

- Common frame `(14,13)` crops wholly within the 29x23 canvas. Its black lower
  corners are authored impassable buffer outside the narrower mud entry, not an
  exposed map edge.
- Bedroom frame `(20,6)` crops wholly within the canvas and includes Marek's bed
  `(21,5)`, doorway `(19,8)` and Latch threshold `(19,9)` together.

## Staging verification

The table uses two blocked table cells with four distinct, stock-passable stool
cells: `(13,12)`, `(16,12)`, `(14,11)` and `(15,13)`. All four connect to the
house route network and do not trap the arrival or bedroom paths.

## Deviations and Mapper decisions

No required event anchor moved and no canvas/zone/exit deviation was taken.

At skeleton fidelity, the stock Inside placeholder makes the timber trim more
decorative than final art may warrant. This is accepted as a documented fixture
limitation, not a canon statement. Final materials and restrained wear remain a
later Asset/Mapping refinement responsibility.

The field kit and calibration weight remain blank anchors without visible item
graphics. This avoids creating a misleading treasure/collectible affordance;
the adjacent repair surface supplies their spatial staging. Eventwright or an
approved Asset pass may later provide non-inventory prop presentation.

Independent Validation observation `OBS-01` was resolved within Mapping
authority: stock tile `332` was removed because its rendered appearance read as
an animal portrait rather than a survey map. The neutral table at `(18,6)` now
fulfills Marek's bedroom preparation-surface requirement without adding lore.

## Mapper gate

Self-validation: `PASS` (`53/53`).  
Map SHA-256: recorded in `validation/validation_results.txt`.

Independent Validator owns acceptance. Eventwright must not begin until that
stage returns PASS.
