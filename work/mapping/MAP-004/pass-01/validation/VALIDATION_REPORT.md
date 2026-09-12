# MAP-004 Mapping Pass 01 — independent Validator report

**Outcome: FAIL** (static Mapping gate). Reviewed independently against the approved MAP-004 work order, locked `PrologueStoryv0.3` P-03/P-07, stock Inside tileset ID 3 flag data, `Map004.json` and camera/full-map previews. No MZ runtime playtest was performed. Owner for both blockers: **Mapping**.

| ID | Severity | Evidence | Required correction and regression |
|---|---|---|---|
| D1 | Blocking | The supposed south wall `(x=4..11,13..20,y=16)` uses tile `6785` with stock flag `0xE08`, which permits lateral walking. From clear arrival `(12,15)` step down onto the intended doorway `(12,16)`, then left to `(11,16)`, `(10,16)` (or right to `(13,16)`): Marek walks along the visually solid wall. | Make all south boundary tiles except the single door `(12,16)` impassable in **all four directions** per actual MZ flags; test movement from the door, not only direct approach from the north. Recheck screenshot and camera composition. |
| D2 | Blocking | Work order's Working back wall requires a generic nonlegible wall chart and recognizable ordinary records. Pass 01 views show bare timber backdrop, plain cabinets and empty worktops without a chart/record visual. | Place a canon-neutral wall chart/record visual in the approved zone, without legible invented geography, measurement or lore. Review it in arrival and desk camera views; escalate if stock assets cannot satisfy. |

Dimensions `25×19`, tileset ID 3, eight exact inert anchors, clear interior arrival `(12,15)`, desk front `(16,11)`, Joren-side `(15,8)`, Edrin `(9,11)`, stage neutrality and absence of new gameplay passed static review. Mapper's 10/10 self-check was insufficient: its wall test only sampled the canvas edge and treated `6785` as if it blocked all directions. Pass 01 is preserved unchanged. Revalidate a separate Pass 02 correction before Eventwright work.
