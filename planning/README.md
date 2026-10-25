# Terminal Territories — Design & Teaching Pack

This folder is the working blueprint for the game: the rules, the build order,
and the architecture that lets each version grow out of the previous one.

| Document | What it answers |
| --- | --- |
| [01-game-mechanics.md](01-game-mechanics.md) | What exactly happens in a game? Costs, formulas, edge cases, scoring. |
| [02-development-phases.md](02-development-phases.md) | What do we build next, what do students learn, and when is a phase "done"? |
| [03-architecture.md](03-architecture.md) | How is the code organised so networking can be swapped without rewriting rules? |
| [04-teaching-notes.md](04-teaching-notes.md) | Session plans, discussion prompts, common student bugs, assessment. |
| [05-client-plan.md](05-client-plan.md) | What draws the game, how the client loop works, and when Pygame replaces the terminal. |

## The one-paragraph version

Players take turns expanding across a seeded hex-free grid, spending two
currencies (action points and resources) to expand, fortify and attack. The
server owns all state. Version 1 speaks REST/JSON; later versions add
persistence, fog of war, push updates, alliances, a raw TCP protocol, a
real-time UDP mode, an economy simulation, bots, and finally a distributed
service topology — without changing the core rules.

## Five design commitments

These are the constraints that make the project teach what it claims to teach.
Break them only on purpose.

1. **Rules engine first, network second.** `terminal_territories/core/` is pure
   Python: no FastAPI, no UI toolkit, no sockets, no database. Every rule can be
   tested with a unit test. The network layer is a thin shell around it.
2. **The server is authoritative, always.** The client renders state and sends
   intentions. It never computes the result of an action it can avoid
   computing, and it never sends something the server blindly trusts.
3. **Every feature earns its concept.** No "now we learn WebSockets" chapter.
   A gameplay problem appears, and the technology is the fix. Phase 4 exists
   because polling makes the map feel dead, not because sockets are on a
   syllabus.
4. **Deterministic by default.** Map generation is seeded; combat is
   arithmetic, not dice. Students can write exact assertions and replay any
   game from its event log. Randomness is a later, deliberate feature flag.
5. **One protocol, many transports.** The same command and event types travel
   over REST, WebSockets, TCP frames and UDP datagrams. Transport changes
   should never change game semantics.

## Reading order for whoever is running the course

1. Read the mechanics doc end-to-end once, without worrying about code.
2. Read the phase doc and mark the cut line for the length of your course
   (there is a suggested 6-week and 12-week path in the teaching notes).
3. Skim the architecture doc before Phase 0 so the folder layout is in place.
4. Keep the teaching notes open during sessions.

## Status

- [x] Design pass: mechanics, phases, architecture, client plan
- [x] Client shell prototype: ANSI welcome, menu and grid (no server or rules engine)
- [ ] Phase 0: rules engine, pure renderer, tests — **next**
- [ ] Phase 1: REST server and custom ANSI terminal client

There is no rules engine or working server yet; `terminal_territories/server/`
is still empty scaffolding.

Numbers in the mechanics doc are a **starting point**, not a sacred text. Phase
0 includes a balance simulation so they can be tuned before anyone plays a real
game.
