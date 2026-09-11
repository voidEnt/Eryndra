# Eryndra Prologue Implementation Decomposition

**Source:** Locked `PrologueStoryv0.3`  
**Scope:** CORE story spine only  
**Status:** First implementation decomposition  
**Goal:** Convert the narrative Prologue into implementation-sized RPG Maker MZ scenes without adding side content or changing canon.

---

## Design Principle

The eight narrative sections in the locked Prologue are not treated as one-to-one RPG Maker event blocks. A new implementation scene is created when one or more of the following changes:

- player control begins or ends
- map ownership changes
- a new event controller becomes responsible for the sequence
- story state must be committed before the player may continue
- the scene requires a separate cinematic staging context

The Prologue contains **no required combat**. Combat should not be invented simply to satisfy RPG expectations. The vertical slice is intended to validate narrative events, exploration, state tracking, map transfers, dialogue, cinematics, audio cues, and asset handling.

---

# Prologue Spine Summary

| Scene ID | Implementation Scene | Narrative Source | Mode | Primary Location | Core Outcome |
|---|---|---|---|---|---|
| `PRO-SC-001` | The Forgotten Place | P-01 | Cinematic | Forgotten Watcher Station | Ancient station wakes; title reveal |
| `PRO-SC-002` | Morning at the Venn House | P-02 | Cutscene -> Player | Venn Home | Marek and family established |
| `PRO-SC-003` | Brackenford Morning | P-02/P-03 | Player | Brackenford | Ordinary life and optional local observation |
| `PRO-SC-004` | The Survey Assignment | P-03 | Dialogue/Cutscene | Survey Office | Joren assigns northern marker inspection |
| `PRO-SC-005` | Leaving Brackenford | P-03/P-04 | Player + Dialogue | Brackenford / Northern Road | Edrin interaction; departure confirmed |
| `PRO-SC-006` | Beyond the Familiar | P-04 | Player Exploration | Northern Road / Low Country | Environmental anomalies accumulate |
| `PRO-SC-007` | The Exposed Structure | P-04/P-05 | Player + Triggered Event | Old Place Exterior | Forgotten masonry discovered; entrance opened |
| `PRO-SC-008` | Contact | P-05 | Player -> Cinematic | Old Place Interior | Marek touches ring; intermediary imprint occurs |
| `PRO-SC-009` | The Echo | P-06 | Cinematic Montage | Distant unknown locations | Network response propagates; Cael observes |
| `PRO-SC-010` | The Report | P-07 | Player + Dialogue | Survey Office / Brackenford | Marek reports site; normality reasserted |
| `PRO-SC-011` | Home, But Changed | P-07 | Player -> Cutscene | Venn Home | Evening normality; Latch unease; distant tones |
| `PRO-SC-012` | The Omen | P-08 | Cinematic | Watcher Station / Old Place / Unknown Chamber | Propagation confirmed; Prologue completes |

---

# Scene Specifications

## PRO-SC-001 - The Forgotten Place

**Priority:** CORE  
**Narrative source:** P-01  
**Player control:** None  
**Required presentation:** Map-based cinematic or equivalent in-engine cinematic  
**Primary map:** `MAP-001 Forgotten Watcher Station` (provisional Bible assignment)

### Required beats

1. Begin in darkness.
2. Reveal dust, fitted stone, unfamiliar metal, roots, and the fractured-ring form.
3. Low pressure/vibration cue.
4. Dust tremor.
5. Ring pulses once.
6. Three restrained notes, equally spaced.
7. Light dies.
8. One narrow line returns and remains faintly visible.
9. Cut to black.
10. Display `ERYNDRA` title.

### Required state output

- Prologue has begun.
- Watcher station has awakened.

### Candidate persistent state names

- `PRO_Started`
- `PRO_WatcherStation_Awakened`

### Asset dependencies

- fractured-ring visual motif
- watcher-station tiles/environment
- three-note resonance SE or short audio asset
- vibration/low-frequency ambience
- title graphic or title text presentation

### Test target

The player must receive no explanatory terminology. Nothing identifies the location, date, civilization, Convergence, node, or network.

---

## PRO-SC-002 - Morning at the Venn House

**Priority:** CORE  
**Narrative source:** P-02  
**Player control:** Begins after introductory family beat  
**Primary map:** `MAP-002 Brackenford - Venn Home`

### Required characters

- Marek Venn - playable actor
- Davren Venn
- Elira Venn
- Nessa Venn
- Latch

### Required beats

- Establish family routine without sentimental exposition.
- Demonstrate Marek's habits through action: correct small problem, verify something twice, remember overlooked obligation.
- Establish Latch naturally as part of the household.
- Marek prepares ordinary field kit.
- Player gains control and leaves for work.

### State output

- Family introduction complete.
- Marek released into Brackenford.

### Candidate persistent state

- `PRO_VennHome_Intro_Complete`

### Local state preference

Minor household interactions should use self switches/local event pages rather than global switches unless later scenes need to know about them.

---

## PRO-SC-003 - Brackenford Morning

**Priority:** CORE  
**Narrative source:** P-02/P-03  
**Player control:** Yes  
**Primary map:** `MAP-003 Brackenford`

### Purpose

This is the Prologue's first meaningful free-exploration segment. It establishes scale, tone, and ordinary community life before the mystery accelerates.

### Required content

- Route from Venn Home to Survey Office.
- Ambient townspeople and ordinary work activity.
- Background hints of wider political/economic unease may appear in NPC dialogue, notices, or environmental details.
- No NPC should identify or discuss the ancient disturbance as a recognized phenomenon.

### Required gate

The story advances only when Marek enters the Survey Office.

### Deferred content

- side quests
- lore books
- optional interiors not needed for the Prologue spine
- expanded merchant systems

These may later be layered onto Brackenford without changing the CORE map's story function.

---

## PRO-SC-004 - The Survey Assignment

**Priority:** CORE  
**Narrative source:** P-03  
**Player control:** Dialogue/cutscene with controlled release  
**Primary map:** `MAP-004 Brackenford - Survey Office`

### Required characters

- Marek
- Joren Pell
- Edrin Holt

### Required beats

- Joren assigns verification of old road/boundary marks north of town.
- Explain that a minor ground shift has caused disagreement between marker and recorded line.
- Establish expectation that Marek returns before supper.
- Establish Marek/Edrin friendship through ordinary banter.
- Preserve wider-world rumors as background texture only.
- Latch follows despite no invitation.

### State output

- Survey assignment received.
- Northern route becomes the active story destination.

### Candidate persistent state

- `PRO_Survey_Assignment_Received`

---

## PRO-SC-005 - Leaving Brackenford

**Priority:** CORE  
**Narrative source:** P-03/P-04  
**Player control:** Yes with short scripted dialogue  
**Primary maps:** `MAP-003 Brackenford`, `MAP-005 Northern Road`

### Required beats

- Marek exits town toward the north.
- Edrin accompanies him along the maintained route.
- Dialogue continues their established friendship.
- At the appropriate junction, Edrin separates to conduct his own inspection.
- Marek continues with Latch.

### State output

- Departure from Brackenford committed.
- Edrin removed from active route sequence.

### Candidate persistent state

- `PRO_Left_Brackenford`

---

## PRO-SC-006 - Beyond the Familiar

**Priority:** CORE  
**Narrative source:** P-04  
**Player control:** Yes  
**Primary map:** `MAP-005 Northern Road`

### Required environmental beats

The anomalies should occur in escalating order while remaining individually dismissible:

1. familiar country transitions into map-known rather than personally-known country
2. birds abruptly absent
3. runoff channel appears wrong
4. expected marker displacement contradicts slope/ground logic
5. surrounding soil is not freshly disturbed
6. Latch refuses to cross shallow curve near dark stone
7. three faint tones heard and dismissed as wind
8. slope opening reveals undocumented worked masonry

### Implementation principle

These should be primarily environmental triggers and short observations, not long forced cutscenes. The player should feel that they are discovering irregularities while doing ordinary work.

### State output

- Exposed structure discovered.

### Candidate persistent state

- `PRO_OldPlace_Discovered`

---

## PRO-SC-007 - The Exposed Structure

**Priority:** CORE  
**Narrative source:** P-04/P-05  
**Player control:** Yes  
**Primary map:** `MAP-006 Old Place - Exterior`

### Required beats

- Establish road-risk/survey reason for Marek to investigate.
- Latch becomes increasingly unwilling to approach.
- Entrance to old masonry becomes interactable.
- Marek chooses to enter only far enough to assess structural risk.

### State output

- Interior access enabled.

### Local state preference

The newly exposed entrance can be handled with local map/event state unless another map needs the exact physical entrance condition.

---

## PRO-SC-008 - Contact

**Priority:** CORE  
**Narrative source:** P-05  
**Player control:** Exploration until ring interaction; then cinematic  
**Primary map:** `MAP-007 Old Place - Interior`

### Required beats

1. precise geometry feels wrong to Marek's trained eye
2. smaller/incomplete divided-ring form discovered
3. Latch remains outside and growls continuously
4. Marek inspects ring
5. player/event triggers contact across fracture
6. first note
7. second note
8. third note felt as much as heard
9. brief spatial disorientation suggesting distant linked places
10. narrow light travels around ring and stops beneath Marek's hand
11. reaction ends
12. Marek verifies he is uninjured
13. Marek leaves while rationalizing the event

### Critical canon rule

Do not show a vision, prophecy, textual message, special mark, power gain, bloodline reveal, or divine selection. The intermediary imprint is invisible to Marek and accidental in circumstance.

### State output

- Marek contact complete.
- Local node awakened.
- Marek intermediary imprint recorded by implementation state.

### Candidate persistent states

- `PRO_Contact_Complete`
- `PRO_LocalNode_Awakened`
- `PRO_Marek_Imprinted`

The player does not see the technical meaning of these flags.

---

## PRO-SC-009 - The Echo

**Priority:** CORE  
**Narrative source:** P-06  
**Player control:** None  
**Presentation:** Cinematic montage

### Required beats

- distant fractured ring produces faint light
- second sealed instrument gives same three-note resonance
- third old location reacts physically without lighting
- unnamed observer hears response from obsolete device
- observer marks the date without celebration

### Canon identity

The unnamed observer is Cael Veyran, but his name must not be revealed to the audience in this sequence.

### Implementation recommendation

Do not create a large explorable map for every anonymous distant location. Use compact cinematic staging maps, reusable cinematic spaces, picture layers, or tightly scoped map fragments. These locations exist to communicate network scale, not to become playable Prologue destinations.

### State output

- Network echo shown to audience.
- Cael has detected renewed activity.

### Candidate persistent state

- `PRO_Network_Echo_Observed`

---

## PRO-SC-010 - The Report

**Priority:** CORE  
**Narrative source:** P-07  
**Player control:** Yes + dialogue  
**Primary maps:** `MAP-003 Brackenford`, `MAP-004 Brackenford - Survey Office`

### Required beats

- Brackenford appears normal.
- Marek reports undocumented masonry and uncertain road risk.
- Marek mentions sound but avoids saying stone answered him.
- Joren treats report seriously but sees no reason for panic.
- Edrin returns with only mundane road problems.
- Ordinary conversation makes Marek's experience briefly feel foolish.

### State output

- Survey report complete.
- Workday story objective complete.
- Home becomes next required destination.

### Candidate persistent state

- `PRO_Report_Complete`

---

## PRO-SC-011 - Home, But Changed

**Priority:** CORE  
**Narrative source:** P-07  
**Player control:** Begins under player control; ends in cutscene  
**Primary map:** `MAP-002 Brackenford - Venn Home`

### Required beats

- Nessa asks why Latch is muddy.
- Davren/Elira discuss ordinary household concerns.
- Supper reinforces normality.
- Latch refuses to sleep in Marek's room and watches north from threshold.
- Later Marek wakes believing he hears three distant notes.
- Notes do not repeat.

### State output

- Evening home sequence complete.
- Marek asleep before closing omen.

### Candidate persistent state

- `PRO_HomeEvening_Complete`

---

## PRO-SC-012 - The Omen

**Priority:** CORE  
**Narrative source:** P-08  
**Player control:** None  
**Presentation:** Closing cinematic

### Required beats

1. Night over Brackenford; lamps extinguish.
2. Marek sleeps.
3. Return to watcher station from `PRO-SC-001`.
4. Light has spread farther around ring; fracture remains black.
5. Three notes sound.
6. Distant three-note answer.
7. Cut to Old Place ring; contact point responds briefly.
8. Cut to another unknown chamber beginning to wake.
9. Cut to black.

### State output

- Prologue complete.
- Game is ready to transition into Act I while Brackenford remains intact and public understanding remains unchanged.

### Candidate persistent state

- `PRO_Complete`

### Test target

The closing feeling must be omen, not explanation. The audience should understand that the event is distributed and continuing, but not what the system is or what it ultimately means.

---

# Initial Core Character Registry for the Prologue

| Bible ID | Name | Implementation Role | First Scene | Notes |
|---|---|---|---|---|
| `ACT-001` | Marek Venn | Playable actor | `PRO-SC-002` | Age 24; human; Aurelian; junior surveyor |
| `NPC-001` | Davren Venn | Family NPC | `PRO-SC-002` | Marek's father |
| `NPC-002` | Elira Venn | Family NPC | `PRO-SC-002` | Marek's mother |
| `NPC-003` | Nessa Venn | Family NPC | `PRO-SC-002` | Marek's younger sister |
| `NPC-004` | Latch | Companion/event NPC | `PRO-SC-002` | One-eared road dog; ordinary animal |
| `NPC-005` | Joren Pell | Survey mentor | `PRO-SC-004` | Gives assignment and receives report |
| `NPC-006` | Edrin Holt | Road Warden / friend | `PRO-SC-004` | Age 26; Marek's oldest friend |
| `NPC-007` | Cael Veyran | Hidden-identity story NPC | `PRO-SC-009` | Audience must not be given his name here |

Unnamed townspeople, travelers, workers, and background figures are SUPPORT assets and may be represented by reusable generic NPC definitions rather than individually registered story characters.

---

# Initial Core Map Registry for the Prologue

These Bible map IDs are provisional assignments for the vertical slice. MZ numeric map IDs remain unassigned until ID ranges are reserved.

| Bible ID | Map Name | Purpose | Required By |
|---|---|---|---|
| `MAP-001` | Forgotten Watcher Station | Opening/closing ancient cinematic | `PRO-SC-001`, `PRO-SC-012` |
| `MAP-002` | Brackenford - Venn Home | Family introduction and evening return | `PRO-SC-002`, `PRO-SC-011` |
| `MAP-003` | Brackenford | Free exploration and town traversal | `PRO-SC-003`, `PRO-SC-005`, `PRO-SC-010` |
| `MAP-004` | Brackenford - Survey Office | Assignment and report scenes | `PRO-SC-004`, `PRO-SC-010` |
| `MAP-005` | Northern Road | Departure and anomaly exploration | `PRO-SC-005`, `PRO-SC-006` |
| `MAP-006` | Old Place - Exterior | Discovery and approach | `PRO-SC-007` |
| `MAP-007` | Old Place - Interior | Contact sequence | `PRO-SC-008` |
| `MAP-008` | Network Echo Staging | Reusable cinematic staging for distant responses | `PRO-SC-009`, `PRO-SC-012` |

`MAP-008` is intentionally a production/staging abstraction. If later art direction makes separate cinematic maps preferable, it may be split before implementation without altering story canon.

---

# Initial Story-State Model

The Prologue should not use one global switch for every small action. The minimum CORE persistent state currently appears to be:

- `PRO_Started`
- `PRO_WatcherStation_Awakened`
- `PRO_VennHome_Intro_Complete`
- `PRO_Survey_Assignment_Received`
- `PRO_Left_Brackenford`
- `PRO_OldPlace_Discovered`
- `PRO_Contact_Complete`
- `PRO_LocalNode_Awakened`
- `PRO_Marek_Imprinted`
- `PRO_Network_Echo_Observed`
- `PRO_Report_Complete`
- `PRO_HomeEvening_Complete`
- `PRO_Complete`

A separate sequential story-stage variable is also recommended, probably system-wide rather than Prologue-specific. This can gate linear progression while switches preserve facts that later acts may need to query.

**Proposed variable concept:** `SYS_StoryStage`

Exact numeric switch/variable IDs are intentionally deferred until the reserved range strategy is finalized.

---

# Vertical-Slice Success Criteria

The Prologue vertical slice is successful when a fresh game can be played from opening cinematic through `PRO_Complete` with:

- correct scene order
- no sequence breaks
- correct map access/gating
- working transfers
- correct character presence
- functioning dialogue and cutscene control
- three-note/ring motif presented consistently
- no premature explanation of ancient-system terminology
- no accidental chosen-one implication
- no required combat added to the Prologue
- save/load does not break story state
- Act I can begin from the resulting state

Only after this spine works should DEFERRED Prologue content such as extra Brackenford interiors, optional conversations, historical books, secrets, or side quests be layered in.
