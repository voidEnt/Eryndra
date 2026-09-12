# MAP-003 Mapping Pass 02 — Return for Independent Regression

## Defect addressed

Pass 01 Validator finding `MAP003-M01`: event ID 7 Latch departure at `(12,26)` conflicted with the work order's `(21,8)`. Pass 02 builder and `Map003.json` place it at `(21,8)` by the north road. The event remains invisible, below characters, through and inert. Its future stage-specific appearance/movement is Eventwright's responsibility, not a Mapper change.

MAP-003 candidate SHA-256: `f96b341538c0bf33b19844a6b276b879ebbed6ebdf296c58b7424ccad568f128`.

## Regression evidence

- The revised self-check passes 15/15, including explicit comparison to the canonical anchor table parsed from the approved work order.
- All other nine event ID/name/coordinate tuples remain unchanged from Pass 01.
- The builder re-rendered overall, home, office and north-road review PNGs. Since the moved event is blank, map tile data and visible preview composition should remain unchanged; independent Validator must verify.
- The exact three outside spawn cells remain free of event anchors and the Venn-home, office and north-road corridor network remains open.
- Both uploaded ZIPs, MAP-001 and MAP-002 were not edited. No new MZ runtime project was created.

## Gate

Independent Validation should rerun all static/schema/passage and canon checks, compare Pass 02 against Pass 01 allowing only the event 7 coordinate and map note changes, verify builder determinism and source hashes, and assess the northern road arrival and departure sightline. Runtime and cross-map integration stay conditional. Do not begin Eventwright until an independent Mapping PASS or a specifically documented nonblocking conditional outcome.
