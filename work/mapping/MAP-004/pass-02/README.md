# MAP-004 Mapping Pass 02 — correction candidate

Corrects independent Pass 01 defects D1 (lateral travel onto false south wall) and D2 (missing ordinary chart/records). No approved anchors, room dimensions, global state, event commands or prior map files changed. `pass-01/` remains preserved for auditing.

Use `Map004.json` only for spatial review; it is not Eventwright-authored or playtest-ready. The same cumulative Eryndra MZ review project will receive an integration candidate only after separate Validator acceptance and Eventwright transfer/dialogue implementation.

Rebuild and Mapper regression from repository root:

```sh
python work/mapping/MAP-004/pass-02/tools/build_map004_pass02.py --sample-zip /path/to/02-SampleGenerated.zip
python work/mapping/MAP-004/pass-02/tools/validate_map004_pass02.py /path/to/02-SampleGenerated.zip
```

The existing `work/mapping/MAP-004/pass-01/tools/build_map004.py` supplies the original geometry and the repository MAP-002 stock renderer supplies stock preview sheets. The ZIP is opened read-only; no sample map data is copied. Separate independent Validation is still required.
