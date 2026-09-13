# MAP-004 Eventwright Work Order — Survey Assignment and Report

**Primary candidate:** `work/mapping/MAP-004/pass-03/Map004.json` (independent static Mapping PASS)  
**Integration patch:** MAP-003 accepted Mapping Pass 02, event ID 2 only  
**Scenes:** `PRO-SC-004` The Survey Assignment; `PRO-SC-010` The Report  
**Priority / pass:** CORE / Eventwright Functional Spine Pass 01  
**Locked sources:** `PrologueStoryv0.3` P-03/P-07; `Player1Backgroundv0.2` Marek, Joren and Edrin  

## Objective and authority

Implement two restrained office scenes on the accepted geometry: Joren's routine morning assignment and Marek's professional afternoon report. Connect the existing MAP-003 office door to MAP-004 and the MAP-004 door back to MAP-003. Preserve the ordinary tone, exact anchors and all accepted tile/collision data.

Eventwright owns event pages, state gates, placeholder character presentation, dialogue wrapping, player staging and the two specified transfer hooks. Do not change either map's tile data/dimensions, move or rename approved anchors, add combat/items/quests/plugins/custom JavaScript, allocate state, reveal ancient-system terminology, place Latch in the office, invent survey findings, or change another MAP-003 event. Placeholder sprites establish no final appearance canon.

## State and transfer contract

| Situation | Required behavior |
|---|---|
| MAP-003 office door ID 2, `VR-0001=1003` | On action, set `VR-0001=1004`; transfer to MAP-004 `(12,15)`, facing north, normal black fade. |
| MAP-003 office door at allowed later town stages | Transfer to the same MAP-004 arrival without changing state. The morning cannot replay after `SW-0103`; afternoon report triggers only at stage 1010. |
| Finish assignment | Set `SW-0103 PRO_Survey_Assignment_Received=ON`, then `VR-0001=1005`; release control in office. |
| MAP-004 door ID 5 | On action, transfer to MAP-003 `(31,16)`, facing south, normal black fade. |
| Enter MAP-004 at `VR-0001=1010` | Run report once. |
| Finish report | Set `SW-0110 PRO_Report_Complete=ON`, then `VR-0001=1011`; release control in office. |

No other global state. Controller pages may use their matching completion switch as a higher-priority blank page so autorun cannot replay. Normal entry path guarantees the exact controller stage; retain an internal equality guard because MZ's page variable condition is `>=`, not equality. Do not set stage merely by entering at unrelated values.

## Placeholder presentation

- Marek remains Actor 1/player; no duplicate Marek event. Move him from arrival `(12,15)` to dialogue staging `(12,12)` with a short forced route before each scene. Followers off during controlled dialogue; restore the previously intended exploration condition afterward.
- Joren uses a restrained stock adult/older placeholder at event ID 3 `(16,8)`, facing toward the work floor.
- Edrin uses a stock adult placeholder distinct from Joren at ID 4 `(9,11)`, facing toward Marek. He is visible for the assignment and report, absent during stage 1005 travel/revisit. Use stage-conditioned pages; no new switch.
- Speaker names required. No face portrait is required for this functional pass; if used, record exact stock sheets/indexes.
- Every Show Text content line must be **40 visible characters or fewer** (control codes excluded), preferably two lines per box and never more than four. Verify mechanically and visually in MZ.
- No three-note sound, shake, tint, supernatural graphic or ominous BGM. Ordinary silence is acceptable until an ambient-audio assignment exists.

## Exact morning dialogue — PRO-SC-004

Run at exact stage 1004 with `SW-0103=OFF`, after staging Marek. Preserve this order and wording; line breaks shown are required content lines.

**Joren**
```
Morning, Marek. The north road needs
a second pair of eyes.
```
**Joren**
```
A road crew says one old marker no
longer agrees with the recorded line.
```
**Joren**
```
Likely a minor ground shift. Verify
the road and boundary marks.
```
**Joren**
```
Correct the measurement, note it in
the ledger, and be back before supper.
```
**Edrin**
```
Before he turns a misplaced stone
into a diplomatic crisis, you mean.
```
**Marek**
```
Roads only stay boring because
someone notices the stones.
```
**Edrin**
```
There he is. I worried the morning
had made you agreeable.
```
**Joren**
```
Edrin has his own inspection along
the first stretch. Take the north road.
```
**Marek**
```
Understood. I'll report when we're back.
```

Then set assignment completion/state in the prescribed order. Latch following is staged later on MAP-003; do not mention or summon him here.

## Exact afternoon dialogue — PRO-SC-010

Run at exact stage 1010 with `SW-0110=OFF`, after staging Marek.

**Joren**
```
You're back. What did you find?
```
**Marek**
```
The marker shifted uphill. The soil
around it wasn't freshly disturbed.
```
**Marek**
```
Above it, the slope opened onto worked
masonry absent from our records.
```
**Marek**
```
It may be an old substructure. Road
risk uncertain. Inspect it properly.
```
**Joren**
```
I'll mark the site for examination.
Anything else?
```
**Marek**
```
I heard three tones inside. Evenly
spaced. I couldn't identify the source.
```
**Marek**
```
For a moment, I thought the stone—
```
**Marek**
```
No. Record that the sound came from
within the structure.
```
**Joren**
```
I will. You don't decorate reports,
so uncertainty belongs in this one.
```
**Edrin**
```
My route offered a washed shoulder
and a wagoner arguing with the rain.
```
**Edrin**
```
You win the stranger report.
```
**Marek**
```
I would rather not.
```
**Joren**
```
We'll examine it properly. For now,
go home. Supper has seniority.
```

Then set report completion/state in the prescribed order. Joren remains professional, Edrin familiar, and Marek stops short of claiming the stone answered him.

## Event architecture and permitted edits

- MAP-004 ID 1 `EV_Story_SurveyAssignment`: autorun page conditioned `VR-0001>=1004`; internal exact-stage and completion guard; a later page conditioned `SW-0103=ON` prevents replay.
- MAP-004 ID 2 `EV_Story_SurveyReport`: autorun page conditioned `VR-0001>=1010`; internal exact-stage and completion guard; later page conditioned `SW-0110=ON` prevents replay.
- ID 3 Joren: visible stock placeholder with stage-appropriate short action lines only if needed; it must never replace either controller.
- ID 4 Edrin: stage pages make him visible at 1004, hidden from 1005 through 1009, visible again from 1010. Avoid page-order mistakes from MZ's `>=` conditions.
- ID 5 office door: action-button bidirectional transfer specified above.
- IDs 6–8: retain inert; ledger/chart/camera anchors need no player interaction in this pass.
- MAP-003: modify **only event ID 2**. Preserve the entire accepted MAP-003 Pass 02 tile array and events 1 and 3–10 byte-equivalently where possible. No live north-road/home transfer is authorized by this work order.

## Deliverables and Eventwright gate

Deliver under `work/mapping/MAP-004/pass-03/eventwright/`: implemented `Map004.json`, a clearly named MAP-003 event-2 integration candidate (not a replacement hidden without notice), deterministic builder, event-command manifest, dependency/deviation report, installer for the existing cumulative Eryndra review project, and static test evidence. Installer must back up changed project data, install/update map ID 4 and its `MapInfos.json` entry, patch MAP-003 ID 2 without replacing its validated tile data, and verify required database switch/variable names without overwriting unrelated project data.

Static acceptance: exact state writes and order; no unauthorized commands; both controllers terminate without replay; exact transfers/directions; only MAP-003 event 2 differs; all dialogue text/order/speakers and ≤40-character content lines; correct Edrin visibility bands; all Mapping geometry/anchors/collision preserved; install dry-run/idempotence and JSON/schema checks. Separate Validator must review Eventwright output. User MZ playtest then checks: entry, assignment, office exit/re-entry without replay, report at stage 1010, message wrapping, character staging, collision, and return to MAP-003. No claim of runtime PASS before that test.
