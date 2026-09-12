# MAP-001 Pass 02 — Integrated Proof Build

This package is the first complete Eryndra room candidate produced through the approved pipeline:

**Work Order → Mapping → Asset Pass → Eventwright → Independent Validation**

It implements the MAP-001 portions of `PRO-SC-001 The Forgotten Place` and `PRO-SC-012 The Omen` as a self-contained proof build for a newly created blank RPG Maker MZ project.

## Current verdict

- Asset checks: **81/81 PASS**
- Eventwright checks: **40/40 PASS**
- Safe-installer checks: **4/4 PASS**
- Independent integrated checks: **50/50 PASS**
- Static verdict: **PASS**
- Final room acceptance: **CONDITIONAL — live RPG Maker MZ playtest required**

No file from `EryndraStory.zip` or `SampleGenerated.zip` is modified or installed. Both supplied ZIPs are immutable reference inputs.

## Package layout

- `assets/` — runtime parallax, overlays, collision tileset, title and audio
- `eventwright/Map001.json` — executable MAP-001 candidate
- `eventwright/install_into_blank_mz_project.py` — guarded blank-project installer
- `review/` — camera and state composites for visual review
- `source/` — generated visual provenance and corrected runtime master
- `validation/VALIDATION_REPORT.md` — independent static verdict
- `validation/RUNTIME_PLAYTEST.md` — exact final acceptance procedure
- `ASSET_MANIFEST.json` — asset identities and hashes

## Runtime hotfix

Live MZ testing retracted the initial `MAP001-RUN-001` diagnosis and confirmed `MAP001-RUN-002`: MAP-001 needs the `!` map-aligned parallax plus the readable-dark reveal tint. See both defect records. Reinstall this revision into a new blank review project before final acceptance.

## Final acceptance step

Follow `validation/RUNTIME_PLAYTEST.md` in a newly created blank RPG Maker MZ project. Return the two requested screenshots and the short PASS/FAIL note. Do not install into either reference archive or an extracted reference-project directory.

The candidate remains in this work folder until runtime acceptance. It is not yet promoted to `game/data/`.
