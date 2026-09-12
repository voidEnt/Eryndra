# MAP-002 Eventwright Dependency and Deviation Report

## Dependencies

- Accepted Mapping Pass 01 `Map002.json`, SHA-256 `429310b40f87053f669aca5377cd0544604d929b0e828a754d6ef966f78cdcd7`.
- Accepted MAP-001 Eventwright candidate, SHA-256 `f6b6a5f5e90d4f48b3b886ee5b23a09a86fba802e4d28c3cacfbf5468d4a39f6`.
- MAP-001 runtime assets already installed, especially `audio/se/Ancient_ThreeNote_Resonance.ogg` or `.m4a`.
- Stock MZ placeholders: character sheets `Actor1`, `People1`, `People2`, `Nature`, `Damage1`; face sheets `Actor1`, `People1`, `People2`; stock SE `Dog` and `Equip1`.
- Registered `MapInfos.json` entries for map IDs 1 and 2.
- Actor 1 displays the canonical default name Marek.

## Exact preserved ownership

- The Eventwright rechecked locked `PrologueStoryv0.3` P-02/P-07 and `Player1Backgroundv0.2` household/voice sections directly from the immutable story archive. The implemented domestic routine, restrained report, ordinary Latch behavior and unease without explanation remain consistent with those sources.
- MAP-002 tile data, dimensions, tileset, furniture, collision-dependent geometry, anchor IDs/names/coordinates and all non-event map properties are unchanged except the map note.
- MAP-001 is preserved except for the explicitly authorized transfer-tail replacement after its existing `PRO-SC-002` hook.
- No source/reference archive was written or extracted as an editable fixture.

## Eventwright implementation choices within authority

- Normal conversational pauses use 12 frames; establishing holds use 36 frames.
- `Dog` uses volume 55; `Equip1` uses volume 45 and pitch 95; `SE-001` uses volume 35 at night.
- The supper relocation and bedroom relocation occur under Fade Out.
- The bedroom uses temporary `Damage1` player presentation and restores `Actor1` before transfer.
- The bedroom camera is normalized to the map's top-right limit using stock Scroll Map commands, which matches the accepted `(20,6)` camera composition without custom JavaScript.
- No optional Marek `...` line was used; the wake is visual and silent.

## Deviations

No approved dialogue, beat, state, coordinate, global ID, geometry or transfer deviation was taken.

## Intentionally unresolved

- MAP-003 has no approved destination coordinate. Event 15 remains an inactive documented hook.
- The actual later return into MAP-002 is not patched because its upstream map/event does not yet exist. Test B supplies the approved direct state setup.
- MAP-001's Omen continuation into MAP-007/MAP-008 remains outside this pass.
- Final character art, dog art, face art, animation, ambient sound and final audio mix remain provisional.
- The MAP-001 transfer patch reopens MAP-001 integration regression even though its prior opening content was preserved.

## Immutable source verification

| Input | SHA-256 after build/test |
|---|---|
| `EryndraStory.zip` | `56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611` |
| `SampleGenerated.zip` | `b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768` |
