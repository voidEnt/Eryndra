# MAP-004 — Mapping Pass 01 candidate

Original `Map004.json` is the spatial-only Brackenford Survey Office for morning assignment and evening report. Approved requirements: `docs/design/maps/MAP-004_Brackenford_Survey_Office_Blueprint.md`. The map is **not independently validated, not Eventwright-authored, not runtime-tested**.

Contents: JSON, reproducible builder and self-check under `tools/`, full-map/arrival/desk PNG previews, stock-tile dependency manifest and Mapper handoff. Only read-only stock tileset sheets and schema were taken from `SampleGenerated.zip`; neither attached ZIP is modified, and no sample map geometry was used.

From repository root:

```sh
python work/mapping/MAP-004/pass-01/tools/build_map004.py --sample-zip /path/to/02-SampleGenerated.zip
python work/mapping/MAP-004/pass-01/tools/validate_map004.py /path/to/02-SampleGenerated.zip
```

The builder reuses the repository's existing stock Inside renderer and blank event-page helper from `work/mapping/MAP-002/pass-01/tools/build_map002.py`. It does not import that map's structure. The preview is a tilesheet composite and does **not** substitute for in-editor/player validation. Use the same cumulative Eryndra review project when a later approved Eventwright integration pass supplies the transfer, not a new MZ game per map.
