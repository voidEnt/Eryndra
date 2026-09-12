# MAP-002 Tile and Dependency Manifest

## Runtime fixture

- RPG Maker MZ stock tileset database slot: `3`
- Tileset name: `Inside`
- Required stock sheets: `Inside_A4`, `Inside_A5`, `Inside_B`, `Inside_C`
- Parallax: none
- Custom graphics: none
- Plugins: none
- Regions: all zero

The fixture remains a placeholder. No stock sheet or other runtime asset is
copied into this package. A user opening the map must use an MZ project whose
tileset slot 3 is the stock `Inside` definition with its original flags.

## Used tile groups

| Tile IDs | Purpose | Passage assumption |
|---|---|---|
| `1536` | Dark outer buffer | Fully impassable |
| `1552` | Maintained wood floor | Passable |
| `6784`, `6785`, `6787`, `6789`, `7048` | Timber/plaster shell, partitions and corners | Structural boundary; treated as blocked |
| `169`, `170`, `177`, `178` | Parents' shared bed | Blocked furniture |
| `171`, `179` | Nessa's bed | Blocked furniture |
| `172`, `180` | Marek's bed | Blocked furniture |
| `137`, `184`, `204`, `212`, `232`, `248` | Ordinary storage and household clutter | Stock passage flags |
| `186`, `194`, `201`, `202`, `203` | Hearth, sink and kitchen surfaces | Blocked work fixtures |
| `112`, `113`, `120` | Supper table and four usable stools | Table blocked; stools passable |
| `116`, `220`, `402` | Marek's neutral preparation surface; Davren's repair surface, scrap wood and hand tools | Stock passage flags |

The field kit and borrowed calibration weight are represented by exact blank
event anchors at `(21,12)` and `(22,12)`. No treasure-like graphic is used in
Mapping Pass 01. The repair table at `(20,13)` provides the required nearby
preparation surface.

Validator observation `OBS-01` was corrected by removing tile `332`, whose
stock appearance read as an animal portrait rather than a survey map. Marek's
small neutral table at `(18,6)` remains the required bedroom preparation
surface without introducing a lore-significant wall graphic.

## Reference integrity

The builder opens `SampleGenerated.zip` read-only for stock sheet preview and
the validator opens it read-only for `Tilesets.json` flags. No reference map is
loaded by the builder, copied or adapted.

Reference hashes observed during this pass:

- `EryndraStory.zip`: `56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611`
- `SampleGenerated.zip`: `b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768`
