# Terminal Territories — Design Pack

The design pack for the game. It is implementation-independent: these documents describe the problems, constraints, and decisions that shape the build, not the state of any code.

Written for one reader: the person building the game.

## Document map

| Document | Purpose |
| --- | --- |
| [01 — Game design](01-game-mechanics.md) | Canonical rules: board, actions, combat, scoring, edge cases. |
| [02 — Development phases](02-development-phases.md) | The technology progression, each step driven by a gameplay problem. |
| [03 — Architecture](03-architecture.md) | Layer boundaries and the invariants that keep rules independent of transport. |
| [04 — Learning notes](04-learning-notes.md) | The personal learning loop: what to notice, try, and revisit. |
| [05 — Client plan](05-client-plan.md) | Terminal-first rendering, with Pygame only for the real-time mode. |

## Reading order

1. **01 once, end to end.** It is the canonical source for every rule.
2. **02 for the path.** Pick the next phase and the problem it solves.
3. **03 before building.** Know the boundaries before adding a layer.
4. **04 while learning.** Use it to reflect on what a phase actually showed you.
5. **05 before client work.** Decide what draws the game and how it talks to the server.

## Principles

- **One canonical source per topic.** Rules live in 01. Other documents link to them instead of restating them.
- **Problems, constraints, decisions.** Documents explain why a design looks the way it does, not how to type it.
- **Code state is irrelevant.** No progress checklists, no gap tables, no "currently implemented" notes.
- **Delete duplication.** If two documents say the same thing, keep the better one and remove the other.
- **Short enough to use.** A document that is not read is not a design document.

## Changing the design

- A rule change edits 01 and its resolved-decisions table, then checks 02 and 05 for stale references.
- A phase change edits 02, then checks the phase list in the root README and the pace table in 04.
- A client decision edits 05, then checks the stack section in the root README.
- Do not create a new document unless it has a unique purpose.
- When a decision is still open, keep it in 01's open questions rather than starting a new file.

## Keeping the pack honest

- Numbers must agree across documents: players, board size, rounds, action points, costs, caps, and victory conditions.
- Every relative link must resolve.
- A summary may repeat a rule only if it links back to 01 as the authority.
- Tables and code fences must stay balanced.
- Prefer deleting a stale paragraph over correcting it in place.

Implementation notes and build checklists belong with the code, not here. Code-specific documentation is a separate, later pass once there is something to describe.
