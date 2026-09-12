# MAP-003 Pass 01 Tile and Reference Dependencies

| Resource | Use | Status |
|---|---|---|
| MZ Outside tileset, `tilesetId: 2` | Runtime ground, roads, roofs, facades and window overlays | Stock MZ placeholder only; project must have the standard `Tilesets.json` entry and sheet filenames. |
| `Outside_A3.png` | Brown wood roofs/facades; ochre backdrop roof | Stock MZ tile sheet, no custom edits. |
| `Outside_A5.png` | Grass, earth, cobblestone, pale stone, boundary rock | Stock MZ tile sheet, no custom edits. |
| `Outside_B.png` | Simple facade windows | Stock MZ tile sheet, no custom edits. |
| `Outside_C.png` | Available in the stock preview loader; no drawn tiles selected | Not a required runtime usage in Pass 01. |
| Existing MAP-002 preview renderer (`tools/build_map002.py`) | Reused only for the MZ stock autotile-geometry table when rendering MAP-003 review PNGs | MAP-003 JSON output does not depend on MAP-002 map data. |
| `SampleGenerated.zip` | Read-only reference for stock sheets/flags only | Never a target for writes or source of canon/layout. SHA-256 `b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768`. |
| `EryndraStory.zip` | Read-only canon for Mapper style gate/self-check | SHA-256 `56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611`. |

No new asset filenames, tileset IDs, music, sounds, plugins or battle graphics are assigned. Runtime custom art and its licensing remain future asset work.
