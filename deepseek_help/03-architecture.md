# Architecture

The architecture exists to make one promise: **the rules never change when the
transport does**. Every phase after 1 is a change at the edge.

---

## 1. Layering

```mermaid
flowchart TB
    subgraph Edge
        UI[Textual client]
        BOT[Bots]
    end
    subgraph Protocols
        REST[REST / JSON]
        WS[WebSocket]
        TCP[TCP frames]
        UDP[UDP datagrams]
        P["protocol: DTOs + codecs"]
    end
    subgraph Application
        SVC["server: game service"]
        STORE[repository / persistence]
        AUTH[auth]
    end
    subgraph Domain
        CORE["core: rules, board, scoring, vision"]
    end
    UI --> P
    BOT --> P
    P --> REST
    P --> WS
    P --> TCP
    P --> UDP
    REST --> SVC
    WS --> SVC
    TCP --> SVC
    UDP --> SVC
    SVC --> CORE
    SVC --> STORE
    SVC --> AUTH
```

Dependency rule, enforced by review and (optionally) an import-linter check:

- `core` may import Python standard library only. Not Pydantic, not FastAPI,
  not Textual, not SQLAlchemy.
- `protocol` may import `core` types and Pydantic.
- `server` may import `core` and `protocol`.
- `client` may import `protocol` (and `core` for rendering helpers, never for
  deciding legality). The one exception is `client/hotseat.py`, which acts as
  the referee in Phase 0 and may call `apply_action`; it is deleted or kept as
  a dev tool once the server exists.
- Nothing imports `client`.

If a rule needs the database, it is not a rule.

---

## 2. Target layout

```text
terminal-territories/
├── pyproject.toml
├── README.md
├── human_notes.md
├── deepseek_help/
└── terminal_territories/
    ├── __init__.py
    ├── core/                 # pure domain
    │   ├── balance.py        # every tunable number, one place
    │   ├── board.py          # generation, adjacency, bounds
    │   ├── state.py          # GameState, Tile, Player
    │   ├── actions.py        # action types + parsed commands
    │   ├── rules.py          # apply_action, validation
    │   ├── combat.py         # attack resolution
    │   ├── vision.py         # fog of war projection (v3)
    │   ├── diplomacy.py      # alliances, proposals (v5)
    │   ├── scoring.py        # standings, victory
    │   ├── events.py         # domain events
    │   └── errors.py         # typed domain errors
    ├── protocol/
    │   ├── models.py         # wire DTOs
    │   ├── codec.py          # JSON encode/decode, TCP framing, UDP packets
    │   └── errors.py         # error codes shared with clients
    ├── server/
    │   ├── app.py            # FastAPI wiring
    │   ├── service.py        # orchestration, transactions, locks
    │   ├── store.py          # in-memory and SQL repositories
    │   ├── auth.py           # tokens, hashing (v3)
    │   ├── realtime.py       # WS hub (v4)
    │   ├── tcp.py            # TCP server (v6)
    │   ├── udp.py            # UDP snapshot loop (v7)
    │   └── routes/
    ├── client/
    │   ├── app.py            # Textual App
    │   ├── screens/          # lobby, game, standings
    │   ├── widgets/          # board, status, log
    │   ├── api.py            # REST/WS/TCP transport clients
    │   ├── store.py          # local view of authoritative state
    │   ├── render.py         # state -> text (shared with tests)
    │   └── hotseat.py        # Phase 0 local game
    └── bots/                 # v9
        ├── client.py
        ├── heuristic.py
        ├── personalities.py
        └── tournament.py
```

Create folders when the phase needs them, not before. Empty scaffolding is a
lie about progress.

---

## 3. The domain model

Immutable state, explicit transitions. This sketch is the shape Phase 0 should
produce:

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Tile:
    x: int
    y: int
    terrain: Terrain
    owner: str | None = None
    strength: int = 0
    captured_round: int | None = None


@dataclass(frozen=True)
class Player:
    id: str
    name: str
    resources: int
    ap: int
    capital: tuple[int, int]
    eliminated: bool = False
    reputation: int = 0          # v3+


@dataclass(frozen=True)
class GameState:
    game_id: str
    version: int                 # increments on every accepted action
    seed: int
    round: int
    turn_index: int
    players: tuple[Player, ...]
    tiles: tuple[Tile, ...]      # row-major, index = y * width + x
    phase: GamePhase             # LOBBY | ACTIVE | FINISHED
```

Commands and results:

```python
def apply_action(
    state: GameState,
    player_id: str,
    action: Action,
) -> tuple[GameState, list[Event]]:
    """Validate and apply one action.

    Raises a DomainError subclass on rejection. Never mutates `state`.
    """
```

Rules for the implementation:

- Validation is a sequence of small guards, each raising a specific error
  (`NOT_YOUR_TURN`, `INSUFFICIENT_RESOURCES`, `TARGET_NOT_ADJACENT`, ...).
- The only randomness is map generation from `seed`; combat is arithmetic.
- Events describe what happened in player-visible terms; they are the source
  for the UI log, replay tests and later the leaderboard.
- State transitions return a new state with `version + 1`. No `copy.deepcopy`
  of the world on every action — use `dataclasses.replace` on the changed
  tiles and players. This is a deliberate performance lesson once maps grow.

### 3.1 Errors

```python
class DomainError(Exception):
    code: str          # stable, shared with clients
    http_status: int   # 400/403/404/409/422
    message: str       # human readable, safe to display
```

Clients branch on `code`, never on `message`. Keep the codes in
`protocol/errors.py` and test that every raised code has an HTTP mapping.

---

## 4. Concurrency and consistency

| Phase | Strategy |
| --- | --- |
| 1 | One in-memory store; requests handled sequentially by the event loop, but read-modify-write is still unsafe across `await` points. |
| 2 | Transaction per action, load → apply → save. Add `version` to the row. |
| 3 | Optimistic concurrency: `UPDATE ... WHERE version = :expected`. Zero rows updated → `409 CONFLICT`. |
| 4 | Per-game `asyncio.Lock` around the read-apply-publish sequence; broadcast only after commit. |
| 6 | Same lock, shared by TCP and HTTP handlers. |
| 7 | Same domain lock; UDP snapshots read an immutable state reference, so they never block gameplay. |
| 10 | Game service is the only writer for a game; other services consume events. Leaderboard is eventually consistent. |

The invariant to state in the code: **only the game service mutates a game, and
it does so under a per-game lock with a version check.** Everything else is a
reader.

---

## 5. Transport abstraction

Define the seam once so Phase 6 and 7 are not rewrites:

```python
class GameSession(Protocol):
    async def join(self, game_id: str, token: str) -> Snapshot: ...
    async def send(self, command: Command) -> Ack: ...
    async def stream(self) -> AsyncIterator[Event]: ...
```

`RestSession`, `WebSocketSession`, `TcpSession` and `UdpSession` implement it.
The Textual app talks to a `GameSession`, so switching transport is a
constructor argument. If the UI knows which transport it is using, the seam is
in the wrong place.

---

## 6. Client architecture (Textual)

- **Screens:** `LobbyScreen` (games, join/create), `GameScreen` (board, status,
  log, input), `StandingsScreen`.
- **Store:** a single source of truth mirroring the server view. Widgets read
  from it and subscribe to changes; they never call the network directly.
- **Worker:** one async task owns the `GameSession` and writes into the store.
  UI events post commands to a queue; the worker sends them.
- **Commands:** a command palette (`e` expand, `a` attack, `f` fortify,
  `space` end turn) with a coordinate prompt. Keyboard-first, mouse optional.
- **Errors:** a persistent status line shows the last server error code and a
  friendly message; a rejected action must never crash the app.
- **Optimistic rendering (v7 only):** apply a predicted change, mark it
  pending, reconcile on the next snapshot, roll back visibly if corrected.
  Before v7, never guess: render only authoritative state.

A plain CLI fallback (`client/cli.py`, stdin + `rich`) is worth keeping for
headless demos and for testing the server without Textual. That is the place
for `prompt-toolkit` if you want line editing.

---

## 7. Configuration

Settings come from environment variables with a `.env` file for development:

```text
TT_HOST=127.0.0.1
TT_PORT=8000
TT_DB_URL=sqlite+aiosqlite:///./tt.db
TT_LOG_LEVEL=info
TT_SEED=1234
TT_ROUNDS=20
TT_REALTIME=false
```

Use `pydantic-settings`. Never read `os.environ` scattered through modules.
Game balance numbers live in `core/balance.py`, not in environment variables:
they are design, not deployment.

---

## 8. Testing strategy

| Layer | Tool | What it proves |
| --- | --- | --- |
| Domain unit | pytest | Every rule, formula and edge case. No I/O, fast. |
| Property | Hypothesis (optional) | Invariants across thousands of random action sequences. |
| Protocol | pytest + golden JSON | Wire format is stable and round-trips. |
| Integration | `httpx.ASGITransport` | Routes, status codes, transactions, auth. |
| Transport | real sockets on localhost | Framing, disconnects, partial reads, loss. |
| End-to-end | scripted games | A full game over the real protocol, deterministic seed. |
| Load/chaos | custom proxy, locust (stretch) | Slow consumers, 10% loss, reconnects. |

Rules for tests:

- Every bug fix gets a failing test first.
- Domain tests use a hand-built board fixture, not a generated one, unless the
  seed is pinned.
- Integration tests never depend on the wall clock; inject the tick source.
- `pytest -m "not slow"` must stay under a few seconds for the inner loop.

---

## 9. Packaging

`pyproject.toml` defines the base install (client + server for Phase 1) and
optional extras by phase:

| Extra | Installs | Used in |
| --- | --- | --- |
| `db` | SQLAlchemy, aiosqlite, Alembic | Phase 2+ |
| `realtime` | `websockets` (client side; uvicorn already ships a server impl) | Phase 4+ |
| `reliability` | Hypothesis (property tests) | Phase 0 stretch |
| `prompt` | prompt-toolkit | CLI fallback only |
| `dev` | pytest, pytest-asyncio, pytest-cov, ruff, mypy | every phase |

`requirements.txt` is redundant once `pyproject.toml` exists. Keep it as a
one-line shim (`-e .`) or delete it, but do not maintain two dependency lists.

---

## 10. Architectural decisions worth writing down (ADRs)

Create `docs/adr/000N-title.md` as you decide:

1. Sequential turns, not simultaneous resolution.
2. Deterministic combat.
3. Server-authoritative state from Phase 1, even before auth exists.
4. Immutable domain state + event log.
5. JSON on the wire until Phase 6, then measure binary.
6. SQLite for the classroom, PostgreSQL for the distributed phase.
7. Neutral tiles on capital capture (anti-snowball).
8. One transport seam, four implementations.

Each ADR: context, decision, consequences, what would change your mind. This is
the highest-value writing exercise in the whole project.
