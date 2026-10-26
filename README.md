# Terminal Territories

A multiplayer, turn-based territory game built as a personal learning project for networking, APIs, concurrency, and distributed systems.

## What it is

Two to four players share a 12 × 8 board, each starting with one capital and a small budget. Every turn gives you 3 action points and a resource budget to spend on Expand, Fortify, or Attack. You win by being the last player standing, or by holding the highest territory percentage after 20 rounds.

The canonical rules are in [01 — Game design](planning/01-game-mechanics.md).

```text
A A . . . . B B B B . .
A A . . . . B B B B . .
A . . C C C B B B . . .
. . C C C C C . . . . .
```

Each letter is a player's territory; a dot is neutral land. Terrain changes what expansion costs and how well a tile defends, and a capital is the one tile that can grow past the normal strength cap.

## Why this project

Every technology in the stack arrives as the answer to a gameplay problem:

- Polling makes the map feel dead, so state moves to push updates.
- Two players overwrite each other's moves, so the server becomes authoritative and actions are serialised.
- A command vanishes on a lossy link, so the protocol gains acknowledgement, sequencing, and retry.
- A restart wipes the match, so persistence and a storage boundary appear.
- One server cannot carry chat, auth, and rankings, so the system splits into services.

That ordering is the point. The rules stay fixed while the transport, storage, and process topology change around them.

## Design rules

- The rules engine is pure and knows nothing about the network.
- The server is authoritative; clients send intentions, not outcomes.
- Every feature earns its technology; no topic is added just to tick a box.
- Determinism first: seeded maps and arithmetic combat make replays and exact tests possible.

## The path

| Phase | Focus |
| --- | --- |
| 0 | Rules engine and hot-seat play |
| 1 | REST API and the first terminal client |
| 2 | Persistence across restarts |
| 3 | Authentication, server authority, fog of war |
| 4 | Push updates over WebSockets |
| 5 | Alliances and diplomacy |
| 6 | A custom TCP protocol |
| 7 | Real-time UDP battlefield |
| 8 | Economy layer |
| 9 | Bot players |
| 10 | Distributed services |

Each phase ends with something playable. The full breakdown, dependencies, and outcomes are in [02 — Development phases](planning/02-development-phases.md).

## Stack

The intended stack, added phase by phase:

- Python 3.12+ and the standard library
- FastAPI and SQLite, once a shared game needs them
- WebSockets, TCP, and UDP
- A custom ANSI terminal client
- Pygame, only for the final real-time mode

The runtime is standard-library-only today. [PACKAGES.md](PACKAGES.md) lists optional future packages and what they are for; nothing there is installed.

## Docs

[planning/README.md](planning/README.md) maps the design pack.

- [01 — Game design](planning/01-game-mechanics.md): canonical rules, costs, formulas, edge cases, and scoring.
- [02 — Development phases](planning/02-development-phases.md): how the technology progresses, one gameplay problem at a time.
- [03 — Architecture](planning/03-architecture.md): layer boundaries and the invariants they protect.
- [04 — Learning notes](planning/04-learning-notes.md): the personal learning loop behind each phase.
- [05 — Client plan](planning/05-client-plan.md): terminal-first rendering and the switch to Pygame for real-time play.

The docs are design specs. They describe problems, constraints, and decisions, not the current code.
