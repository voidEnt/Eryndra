# MAP-002 Eventwright Self-Validation Report

**Stage:** Eventwright Functional Spine Pass 01  
**Outcome:** **PASS for Eventwright handoff**  
**Independent Validation:** Required  
**Runtime acceptance:** Required

## Static results

- Event/data checks: `40/40 PASS`, including face-window layout (36 characters / four lines maximum)
- Installer refusal/atomicity scenarios: `10/10 PASS`, including exact installed pre-wrap pair upgrade
- Deterministic rebuild: byte-identical PASS
- MAP-002 Mapping geometry/data: byte-identical to accepted baseline
- All 17 anchor IDs, names and coordinates: preserved
- Morning movement route: all 28 steps stock-passable and clear of staged NPCs
- Exact dialogue: Morning `22/22`; Evening `22/22`; ambient `3/3`
- Unauthorized inventory, battle, shop, plugin, script and route-script commands: none
- New global IDs: none
- MAP-003 transfers: none

## Candidate hashes

| Candidate | SHA-256 |
|---|---|
| `Map001_TRANSFER_PATCH_CANDIDATE.json` | `98fec8f89e190531e5de74b525574769b59c79c2030a9fd2ac9a906c47d623cd` |
| `Map002.json` | `fcf70f9e356c2b35ec72332129715f9ff6e856cb6a90003e5e3352dbf757c933` |

## Installer evidence

The installer tests verify:

1. both immutable archive-name targets are refused without a byte change;
2. a path named as an extracted `SampleGenerated` tree is refused without a byte change;
3. a missing required asset is refused without a byte change;
4. an incompatible MAP-002 baseline is refused without a byte change;
5. dry-run performs no write;
6. successful installation replaces only both documented map files and creates backups; and
7. an injected second-replacement failure rolls both map files back to their original bytes.

All refusal checks run before backup directory creation, temporary staging or replacement. The current installer accepts the exact pre-wrap installed map pair as a source for the wrapped replacement; it refuses a mixed or user-modified pair.

## Required independent/runtime checks

- Regression of the complete validated MAP-001 opening through its new transfer.
- MZ execution of Morning and Evening movement routes against real collision.
- Visible/controllable release and exact state `SW102=true`, `VR1=1003`.
- Bedroom composition, downed/wake presentation, one faint note cue and silent Latch.
- Black transfer and exact Evening state `SW111=true`, `VR1=1012`.
- Save/load and no-replay behavior.
- Placeholder sprite/face compatibility in the user's MZ runtime.

This report does not claim independent or user runtime acceptance.

User observed horizontal dialogue clipping in the previous candidate. The wrapped candidate passes static checks, but the presentation correction still needs MZ runtime confirmation.
