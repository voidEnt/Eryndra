# MAP-004 stock tile dependencies

- MZ map ID 4, tileset ID 3 (`Inside`); stock `Inside_A4.png`, `Inside_A5.png`, and `Inside_B.png` from `SampleGenerated.zip` are consulted read-only for rendering. These are stock MZ asset dependencies, **not** sample-project layout/canon. Review project must contain compatible stock Inside tileset at ID 3. If its database differs, resolve deliberately before installation.
- Tile size 48px, 25×19 map, six layers. A5 floor/buffer tile IDs: `1552` (walkable wood), `1536` (blocked dark). A4 timber/wall IDs: `6784`, `6785`, `7048`. B furniture IDs: `116` (ordinary desk), `120` (stool), `137` (cabinet). No custom image/audio required.
- The desks/cabinets stand in for mundane survey records, with no legible ledger or measured map drawn in the stock assets. Eventwright/Asset Worker may propose a dedicated ledger visual later, but Mapping does not create new canonical content, images or inventory items.
- `Map004.json` has no script, plugin, BGM/BGS autoplay, battle, external PNG/parallax reference or live event dependency. Its blank anchor schema comes from the existing repository MAP-002 builder.
- The reference ZIPs, their database/map IDs and attached canon PDFs remain unchanged. No assets or layouts were copied out to become new Eryndra canon.
