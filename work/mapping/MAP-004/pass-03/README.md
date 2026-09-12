# MAP-004 Mapping Pass 03 — chart correction candidate

Corrects the remaining Pass 02 D2 visual defect without changing the work order: replaces the back-wall note tile `(11,5)` with stock Inside_C tile `329`, a small tabular chart with illegible row and column marks. Pass 02's impassable wall and desk parchment are retained. Pass 01 and Pass 02 remain unchanged for audit.

`Map004.json` remains spatial-only with eight inert event anchors; the cumulative Eryndra review project is **not** modified. Independent static Validation and MZ runtime validation are separate gates. The original story and sample ZIPs are reference-only and unchanged.

From repository root with an available copy of the sample ZIP:

```sh
python work/mapping/MAP-004/pass-03/tools/build_map004_pass03.py --sample-zip /path/to/02-SampleGenerated.zip
python work/mapping/MAP-004/pass-03/tools/validate_map004_pass03.py /path/to/02-SampleGenerated.zip
```
