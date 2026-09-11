# MAP-001 Asset Work Order - Forgotten Watcher Station

**Scope:** MAP-001, PRO-SC-001, and reusable support for PRO-SC-012  
**Priority:** CORE  
**Input geometry:** accepted MAP-001 Mapping Pass 01  
**Canon source:** PrologueStoryv0.3, P-01 and P-08  
**Authority:** Production Roles and Handoff Contract

## Objective

Create a self-contained visual and audio presentation package for the sealed watcher-station chamber. The tile map remains the spatial and event-anchor substrate. A map-sized parallax supplies the chamber art, while transparent picture overlays supply ring and dust states.

The work must preserve the accepted 29x21 geometry and the two approved 816x624 camera frames.

## Registered dependencies

| Bible ID | Runtime name | Purpose |
|---|---|---|
| TIL-007 | Cinematic Parallax Collision | Invisible passable/blocked A5 tiles for parallax cinematic maps |
| PIC-001 | MAP001_WatcherStation_Base | Map-sized dormant chamber parallax |
| PIC-002 | MAP001_Ring_Pulse | Full ring pulse overlay |
| PIC-003 | MAP001_Ring_Residual | Narrow residual line after opening pulse |
| PIC-004 | MAP001_Ring_Propagated | Wider closing-omen illumination |
| PIC-005 | MAP001_Dust_Tremor | Restrained dust disturbance overlay |
| PIC-006 | SYS_Eryndra_Title | Opening title card |
| SE-001 | Ancient_ThreeNote_Resonance | Three low signal tones with equal silence |

## Required outputs

- Map-sized PNG MAP001_WatcherStation_Base.png, exactly 1392x1008.
- Transparent 816x624 PNG overlays for pulse, residual, propagated and dust states, aligned to the approved ring-camera frame.
- Transparent 816x624 SYS_Eryndra_Title.png containing only ERYNDRA.
- OGG three-note cue at practical MZ volume, with three restrained low tones separated by equal silence.
- Transparent 768x768 A5 sheet Eryndra_CinematicCollision_A5.png.
- Tileset-7 database fragment with tile 1536 fully blocked, tile 1537 passable, and unused tiles set to star/skip.
- Asset manifest with dimensions, alpha status, hashes, origin, prompt/process, intended folder and license/source notes.

## Visual requirements

- One sealed chamber; no added rooms or exits.
- Exact ancient fitted stone, sparse dull metal, dead roots through fine seams, dust without footprints.
- The fractured ring is embedded on the north wall and remains visibly solid-backed.
- One narrow deliberate black fracture at the top of the ring.
- Dormant state is nearly dark.
- Pulse is restrained cold white/cyan.
- Residual state lights only a short narrow arc.
- Propagated state lights substantially more circumference while the fracture stays black.
- Ring overlays may glow but must not contain letters, runes or symbols.

## Forbidden content

No characters, corpses, furniture, treasure, doors, stairs, altars, thrones, readable text other than the title asset, religious symbols, runes, torches, daylight, active machinery, portals or footprints.

## Technical rules

- Generated art may not change MAP-001 collision geometry or anchor coordinates.
- Keep supplied ZIP files immutable and reference-only.
- Do not copy stock reference sheets into the Eryndra repository.
- The base art may use the approved generated concept derived from the accepted map composite.
- Ring/dust overlays must be deterministic and reproducible where practical.
- The black fracture remains unlit in every ring state.
- All project-bound assets live under work/mapping/MAP-001/pass-02/ until final validation.

## Acceptance

The Asset pass advances when all dimensions and alpha channels validate, both camera compositions remain readable, the four ring states are visually distinct, the three-note timing is measurable, no forbidden content appears, and a manifest records every output.
