# Terminal Territories — Game Design

The canonical, implementation-independent rules of the game. For how the game is
built, see [02-development-phases.md](02-development-phases.md).

---

## 1. Quick reference

| Setting | Value |
| --- | --- |
| Players | 2–4, one capital each |
| Board | 12 × 8 (96 tiles), 4-neighbour adjacency |
| Game length | 20 rounds |
| Starting resources | 10; no income in round 1 |
| Action points | 3 per turn; unspent AP is lost |
| Expand | 1 AP + 2 / 3 / 3 / 4 resources (plains / forest / hills / ruins) |
| Fortify | 1 AP + 2 resources; +1 strength |
| Attack | 1 AP + `S` resources; commit `S` strength |
| End turn | free |
| Victory | last player standing, or highest territory % after round 20 |

A tile's **strength** is its garrison: the number used to defend, attack, and fortify.

---

## 2. Board and terrain

- A rectangular grid, **12 × 8 = 96 tiles** by default.
- Coordinates are `(x, y)`: `x` is the column, `y` is the row, and the origin
  `(0, 0)` is the **top-left**. Row 0 is the top row.
- Adjacency is **4-directional** (up, down, left, right). Diagonals do not count.
- Unowned land is **neutral** and can be claimed by anyone adjacent.
- Water is never owned and cannot be entered or attacked across.
- Map generation uses a stored seed, so a game can be regenerated exactly.

| Terrain | Passable | Expand | Income | Defense | Vision | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Plains | yes | 2 | 1 | +0 | 2 | Default terrain |
| Forest | yes | 3 | 1 | +1 | 2 | Cheap cover, poor economy |
| Hills | yes | 3 | 2 | +2 | 3 | Best income and defense |
| Ruins | yes | 4 | 1 (v8) | +1 | 2 | 15 resources once on claim, v8 only |
| Water | no | — | 0 | — | 0 | Blocks adjacency |

A **capital is not a terrain**. A capital tile yields **3** income (it replaces
the terrain yield) and adds **+2 defense**. Its vision is 3 and its strength cap
is 8. Capital status belongs to the player, not the ground.

Suggested mix: ~12% water, ~20% forest, ~12% hills, rest plains. Capitals and
their four neighbours are always land, and all capitals lie in one connected
passable-land component.

---

## 3. Players and setup

| Setting | Value |
| --- | --- |
| Capital | exactly one per player, starting strength 3, on plains |
| Starting resources | 10 |
| Action points | 3 per turn |
| Resources | carry over between turns; no cap |
| Turn order | fixed join order, never rotated |
| Randomness | none in combat; only seeded map generation |

Capital placement: one per quadrant. Two players use opposite quadrants, three
use three of the four, four use all four. Capitals are at least **5 tiles apart
by Manhattan distance**, have all four neighbours on land, and share one
connected passable-land component.

Play proceeds in join order starting with the first living seat; eliminated
players are skipped. There is no dice roll and no random seating. A round ends
after every living player has taken one turn.

---

## 4. Turn structure

**Start of turn.** Collect income from your owned tiles in round 2 and later.
Reset AP to 3. Unspent AP from your previous turn is gone.

**Act.** Spend AP and resources in any order. Every action validates fully before
anything is deducted, so a rejected action changes nothing. You may act until AP
runs out or you choose to stop.

**End turn.** Free and always legal on your turn, even with AP remaining.

If you capture a tile this turn, that tile is **newly captured** and cannot act
until your next turn: it cannot be fortified and cannot be an attack source.
Expand has its own eligible-neighbour rule (§5.1).

Victory is checked after every action and at the end of every turn.

---

## 5. Economy

```
income = sum of tile income for every tile you own
```

- A capital yields **3**, replacing the terrain yield rather than adding to it.
- Other owned tiles yield their terrain income: plains 1, forest 1, hills 2,
  ruins 1 after claim (v8).
- A **0-strength owned tile still earns income** and still counts as territory.
- Water yields nothing and is never owned.
- There is **no upkeep in v1**.

Example: capital + 2 plains + 1 forest + 1 hills yields
`3 + 1 + 1 + 1 + 2 = 8` resources per turn.

There is **no income in round 1**. The starting 10 resources are the opening
budget.

---

## 6. Actions

### 6.1 Expand

Claim one adjacent neutral **land** tile.

- Cost: 1 AP + the terrain expand cost (plains 2, forest 3, hills 3, ruins 4).
- The new tile becomes yours with **strength 1** and is newly captured.
- The target must be 4-adjacent to a tile you own that was **not captured this
  turn**. A tile captured earlier this turn does not qualify, so expansion
  cannot chain through fresh conquests.
- Expand has no source tile and moves no strength, so any eligible owned
  neighbour works, including a 0-strength one.
- The target must be neutral land; expanding into water or an owned tile is
  invalid.

### 6.2 Fortify

Increase the garrison of an owned tile.

- Cost: 1 AP + 2 resources.
- Effect: **+1 strength**, up to the cap: **5** for a normal tile, **8** for a
  capital.
- The target must be yours and **not newly captured**. A 0-strength owned tile
  may be fortified.
- Fortifying at the cap is rejected and costs nothing.

### 6.3 Attack

Attack an adjacent enemy tile by committing strength from one of your tiles. You
choose the **source**, the **target**, and **`S`**, the strength committed.

- Cost: 1 AP + `S` resources.
- `1 ≤ S ≤ source strength`. The source must be owned, not newly captured, and
  have at least 1 strength.
- Remove `S` from the source **immediately**, whether the attack succeeds or
  fails. A source reduced to 0 stays yours, still earns income, and cannot
  attack again until fortified.
- You may attack the same target more than once in a turn if you can pay for it.

Resolution:

```
attacker power = S
defender power = target strength + terrain defense + 2 if the target is a capital
```

| Condition | Result |
| --- | --- |
| `S > defender power` | **Capture.** The target becomes yours with garrison `max(1, S - defender power)` and is newly captured. |
| `S <= defender power` | **Repelled.** The owner is unchanged. If target strength is above 0, it loses `max(1, floor(S / 2))` but never drops below 1. If it is 0, it stays 0. |

A tie is a repel, and a repel never increases strength. Attacking a neutral tile
is invalid; use Expand. Attacking an ally is invalid while the alliance is active.

**Worked attacks.** Assume plains unless stated.

| Source | `S` | Target | Result |
| --- | --- | --- | --- |
| 4 | 3 | strength 2, forest (defense 3) | Tie: repelled. Target 2 → 1. Source 4 → 1. Cost 3. |
| 5 | 4 | strength 2, forest (defense 3) | `4 > 3`: captured with garrison 1. Source 5 → 1. Cost 4. |
| 1 | 1 | strength 0, forest (defense 1) | Tie: repelled. Target **stays 0**. Source 1 → 0. Cost 1. |

**Chipping a capital.** A full-strength capital on plains has defense
`5 + 2 = 7`, while a normal tile caps at 5 strength, so it must be chipped first.

| Step | Attack | Math | Result |
| --- | --- | --- | --- |
| 1 | strength-4 tile commits `S=3` | `3 <= 7` | Repelled. Capital 5 → 4. Source 4 → 1. |
| 2 | strength-5 tile commits `S=4` | `4 <= 6` | Repelled. Capital 4 → 2. Source 5 → 1. |
| 3 | strength-5 tile commits `S=5` | `5 > 4` | Captured with garrison 1. Source 5 → 0. |

### 6.4 End turn

Free. Advance to the next living player in join order. After the last living
player acts, the round counter increments and the next round starts with the
first living player in join order. The starting seat is **never rotated**.

### 6.5 Surrender

On your turn you may leave the game. All your tiles, including your capital,
become neutral with strength 0. You are eliminated and removed from turn order.
Your resources are discarded, not transferred. Any alliances involving you
dissolve.

---

## 7. Capture, elimination, and victory

### 7.1 Capturing a capital

1. The captured capital becomes a **normal owned tile for the attacker**. The
   attacker does not gain a second capital; their original capital remains
   their only one.
2. The defeated player is **eliminated** and removed from the turn order.
3. All the defeated player's other tiles become **neutral with strength 0**.
4. Resources are **not transferred**; they are discarded. Any alliance
   involving the defeated player dissolves.

### 7.2 Victory and scoring

1. **Domination:** only one non-eliminated player remains; that player wins.
2. **Round limit:** after the last turn of round 20, the highest territory
   percentage wins.

```
territory percentage = owned land tiles / total land tiles × 100
```

A 0-strength owned tile still counts. Water is not land. Eliminated players own
no tiles and score 0.

Tie-breakers, in order: total garrison strength, then resources, then the
earliest position in the initial join order.

There is **no shared victory**. At the round limit, allies are ranked against
each other like anyone else.

---

## 8. Later layers

These add to the core; the rules above still apply, with the additions below.

### Fog of war (v3)

- Tiles are *visible* (full data), *remembered* (terrain plus stale owner and
  strength), or *unknown* (a blank cell).
- Vision is 2 for owned tiles and 3 for hills and capitals. Shared vision arrives with alliances (v5).
- Terrain is remembered permanently; owner and strength are not.

### Alliances (v5)

- A player proposes; the target accepts or declines. Proposals expire after 2
  rounds.
- Allies cannot attack each other, share vision, and may transfer up to 10
  resources once per round for 1 AP.
- Breaking is unilateral and instant, with a 3-round re-ally cooldown.
- There is no shared victory.

### Real-time mode (v7)

- AP regenerates 1 every 2 seconds, cap 3; income arrives every 10 seconds.
- There is no turn order; every player may act at once.
- A match ends after 10 minutes or when someone reaches 60% territory.

### Economy layer (v8)

- Upkeep is `floor(owned tiles / 6)` resources per turn.
- Ruins pay 15 once on claim, then yield 1 per turn.
- A trade bonus gives +1 income per allied capital after 3 rounds.
- Net income never falls below 0.

### Bots (v9)

- Bots use the same actions and protocol as players.
- Personalities are preference weights, not separate rules.

---

## 9. Resolved decisions

| # | Question | Decision |
| --- | --- | --- |
| A | Does a captured capital become a second capital? | No. It becomes a normal owned tile for the attacker; each player has exactly one capital. |
| B | What strength does a neutral tile have? | Always 0, including tiles abandoned by surrender or elimination. |
| C | Can an owned tile reach 0 strength? | Yes. It still counts for territory and income, can be fortified, cannot attack, and can still be Expand's eligible neighbour. |
| D | Is there income in round 1? | No. Income starts in round 2; the opening budget is 10. |
| E | Can Expand chain through newly captured tiles? | No. The neighbour must have been owned before this turn. |
| F | Is there a shared victory for allies? | No. At the round limit, allies are ranked against each other. |
| G | What does fog "unknown" show? | A blank cell: no terrain, owner, or strength. Terrain is known permanently once seen; owner and strength are not. |
| H | Do ruins produce income? | 15 resources once on claim, then 1 per turn (v8). v1 maps contain no ruins. |
| I | How are capitals constrained? | One per quadrant, at least 5 Manhattan apart, on plains, four land neighbours, all in one connected land component. |
| J | Why is capital defense +2 when sources cap at 5? | Intentional. A full-strength capital must be chipped before it can fall. |
| K | Who goes first? | Fixed join order. No dice, no random seats, no start-seat rotation. |
| L | What does an attack choose? | Source, target, and committed strength `S`, all explicit. |
| M | What does "newly captured" mean? | Captured during your current turn. Such a tile cannot fortify or attack this turn. |
| N | What happens when a repel hits a 0-strength tile? | It stays 0. A repel never increases strength. |

---

## 10. Tuning knobs

| Knob | Default | Range to try | Effect |
| --- | --- | --- | --- |
| Map size | 12 × 8 | 10 × 8 – 16 × 10 | Bigger maps favour expansion and longer games. |
| AP per turn | 3 | 2–4 | Lower is slower and more tactical. |
| Starting resources | 10 | 5–15 | Higher gives a more explosive opening. |
| Fortify cost | 2 | 1–3 | Cheaper fortify favours turtling. |
| Strength caps | 5 / 8 | 4–6 / 6–10 | Lower caps make capitals easier to take. |
| Round limit | 20 | 12–30 | Shorter games end in more territory races. |
| Income per tile | 1 | 1–2 | With 20+ tiles, 1 per turn is already strong. |
| Capital defense | +2 | +1–3 | Lower values make early capital rushes viable. |
| First-player advantage | none | Last seat +1 resource, or randomize seats once | Never rotate the start seat; it gives A, B, B, A in a 2-player game. |

---

## 11. Open playtest questions

- Is committing the whole garrison too punishing, or is it the right tension?
- Does the 3-round alliance cooldown create enough doubt, or should betrayal
  also cost resources?
- Does the round limit produce too many ties? A sudden-death round with doubled
  income is the fallback.
- Should eliminated players spectate with full vision?
