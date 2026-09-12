# MAP-003 Brackenford — Mapping Pass 01 Candidate

**Status:** Mapper self-check PASS (`14/14`); **independent Mapping Validation pending**. No Eventwright work or live transfer is included in this package.

**Source:** approved [`MAP-003_Brackenford_Blueprint.md`](../../../../docs/design/maps/MAP-003_Brackenford_Blueprint.md), Prologue P-02/P-03/P-07. The map serves `PRO-SC-003`, `PRO-SC-005` and `PRO-SC-010` without separate morning/afternoon copies.

## Package

- `Map003.json` — original 45×35 map using stock Outside tileset slot 2; no changes to MAP-001 or MAP-002.
- `MAP-003_full-map.png` and three 816×624 camera views (`home`, `office`, `north-road`).
- `tools/build_map003.py` — deterministic source; reads only the immutable sample ZIP for stock tileset preview sheets.
- `tools/validate_map003.py`, `validation_self_results.txt` — Mapper self-check, not independent acceptance.
- `MAPPING_HANDOFF.md` — known limits, staged routes and next-stage dependencies.
- `TILE_DEPENDENCY_MANIFEST.md` — exact stock asset and preview dependency.

The screenshots are review composites of stock MZ tiles, not a claim of final commissioned artwork. Large facades and minimal set dressing are deliberate Pass 01 blocking geometry; later refinement should add ordinary town texture without changing anchor/route requirements. No ambient dialogue, rumor text, dog logic, quest, shop, map transfer or state change has been authored.

Do **not** overwrite a live review project's files with this unvalidated skeleton. Installing another map requires an explicitly reviewed addition to that project's `MapInfos.json`, asset inventory and the later Eventwright transfer hooks; there is no need to create a new game for each map.

## Reproduce

From the repository root, with Python 3 and Pillow available:

```text
python3 work/mapping/MAP-003/pass-01/tools/build_map003.py --sample-zip /path/to/immutable/SampleGenerated.zip
python3 work/mapping/MAP-003/pass-01/tools/validate_map003.py --mapfile work/mapping/MAP-003/pass-01/Map003.json --sample-zip /path/to/immutable/SampleGenerated.zip --story-zip /path/to/immutable/EryndraStory.zip --output work/mapping/MAP-003/pass-01/validation_self_results.txt
```

Exact input archives remain reference-only and unchanged. Validation should compare the map directly against the locked story, Bible, blueprint and stock MZ passage behavior, not just rerun Mapper-owned checks.
