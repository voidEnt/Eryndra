# MAP-002 Mapping Pass 01

**Map:** `MAP-002 Brackenford - Venn Home`  
**Stage:** Mapping skeleton  
**Ownership:** Eryndra project  
**Status:** Mapper self-validation PASS; pending independent Validation

Independent Validation observation `OBS-01` has been corrected: the misleading
stock animal-portrait tile was removed from Marek's room and the neutral work
surface retained. The package is ready for Validator re-check.

This package implements the approved one-floor spatial skeleton for the Venn
home. It contains no dialogue, autorun, transfer, movement route, audio,
character graphic or global-state logic. The 17 required events are blank
registration stubs for the Eventwright.

## Deliverables

- `Map002.json` - RPG Maker MZ map data
- `MAP-002_full-map.png` - 1392x1104 full-map composite
- `MAP-002_common-room_816x624.png` - approved common-room camera crop
- `MAP-002_marek-bedroom_816x624.png` - approved bedroom camera crop
- `TILE_DEPENDENCY_MANIFEST.md` - tileset and passage dependencies
- `MAPPING_HANDOFF.md` - compliance and deviation report
- `tools/build_map002.py` - deterministic map/composite builder
- `tools/validate_map002.py` - Mapper-stage validator
- `validation/validation_results.txt` - latest validator output

## Rebuild

The builder reads the supplied `SampleGenerated.zip` only to preview the stock
MZ Inside sheets. It never extracts into or writes to the reference project.

```powershell
py tools\build_map002.py --sample-zip "C:\path\to\SampleGenerated.zip" --output-dir "."
py tools\validate_map002.py --map ".\Map002.json" --sample-zip "C:\path\to\SampleGenerated.zip" --results ".\validation\validation_results.txt"
```

Python 3 and Pillow are required for composite generation. `Map002.json` itself
uses only stock MZ data structures and stock Inside tileset slot 3.
