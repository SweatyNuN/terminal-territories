# Future Package Options

Nothing here is installed. This is a menu, not a dependency manifest. Add a package only when the phase that needs it begins. The runtime is standard-library-only today.

## Installed now

Runtime: none. Development: pytest, pytest-asyncio, ruff, mypy, pre-commit, and textual (retained experiment only).

## Standard library first

- `dataclasses` / `enum`: models, actions, and game states without a framework.
- `json` / `struct`: JSON payloads and binary framing.
- `sqlite3`: persistence and transactions before any ORM.
- `asyncio` / `socket` / `selectors`: servers, streams, and connection handling.
- `termios` / `tty` / `select`: raw terminal input for the client.
- `tomllib`: reading configuration without an extra parser.

## Phase 1 — REST

| Package | What it would be for | When/notes |
| --- | --- | --- |
| fastapi | HTTP routing and validation | When one terminal cannot share a game |
| uvicorn[standard] | ASGI server | Pairs with FastAPI |
| httpx | Client-side HTTP calls | Also the basis for later tests |
| pydantic | Request and response models | Validation at the boundary |
| pydantic-settings | Configuration from environment | Keep secrets out of code |
| typer (or click) | Command-line entry point | Typer if you want type hints |
| rich | Readable terminal output | Optional; plain text is fine first |

## Phase 2 — Persistence

| Package | What it would be for | When/notes |
| --- | --- | --- |
| sqlalchemy | Models and query layer over SQL | When raw SQL becomes repetitive |
| aiosqlite | Async SQLite driver | Only if the server is async |
| alembic | Schema migrations | When a migration must be reversible |
| psycopg[binary] or asyncpg | PostgreSQL drivers | Later, when SQLite stops fitting |

## Phase 3 — Identity and security

| Package | What it would be for | When/notes |
| --- | --- | --- |
| argon2-cffi | Password hashing | Prefer over hand-rolled schemes |
| passlib[bcrypt] | Alternative password hashing | Choose one hashing library |
| pyjwt | Signed session tokens | When sessions cross process boundaries |
| itsdangerous | Signed values and cookies | Simpler than JWT for one server |
| python-multipart | Form and file parsing | Needed for login forms |

## Phase 4 — Push

| Package | What it would be for | When/notes |
| --- | --- | --- |
| websockets | Client side of WebSocket transport | uvicorn[standard] includes the server side |
| sse-starlette | Server-sent events | A simpler alternative to WebSockets |
| httpx-sse | Client for server-sent events | Pairs with sse-starlette |

## Phase 5 — Diplomacy

| Package | What it would be for | When/notes |
| --- | --- | --- |
| transitions or python-statemachine | State machines for alliances | Optional; plain enums may be enough |

## Phase 6 — TCP

No package is required for the transport itself; `asyncio`, `socket`, and `struct` cover it.

| Package | What it would be for | When/notes |
| --- | --- | --- |
| orjson | Faster JSON encoding | Optional; measure before adding |
| msgpack | Compact binary frames | Optional; compare against JSON |
| cbor2 | Alternative binary encoding | Optional; choose one format |

## Phase 7 — UDP and Pygame

| Package | What it would be for | When/notes |
| --- | --- | --- |
| pygame or pygame-ce | Visual client for real-time play | Choose one; pygame-ce is a maintained fork |
| numpy | Math and interpolation | Optional; pure Python may suffice |
| msgpack / cbor2 | Compact snapshots | Optional; reuse the Phase 6 format |

## Phase 8 — Economy

No runtime package is required; the economy layer is rules and configuration.

| Package | What it would be for | When/notes |
| --- | --- | --- |
| hypothesis | Property-based balance tests | Optional but useful for invariants |
| pytest-benchmark | Timing comparisons | Optional; supports balance experiments |

## Phase 9 — Bots

| Package | What it would be for | When/notes |
| --- | --- | --- |
| numpy | Evaluation math | Bots use the public protocol |
| scipy | Optimisation and statistics | Optional |
| networkx | Graph work over the board | Optional |
| scikit-learn / torch | Machine learning experiments | Heavy; not needed for v1 |

## Phase 10 — Distributed

| Package | What it would be for | When/notes |
| --- | --- | --- |
| redis | Shared state and simple queues | When services share data |
| nats-py or aio-pika | Message broker client | Pick one broker |
| asyncpg or psycopg | Shared PostgreSQL access | When SQLite is no longer enough |
| opentelemetry-sdk | Traces across services | Add instrumentation packages alongside |
| prometheus-client | Metrics | Pair with a scrape endpoint |
| tenacity | Retries and backoff | For calls between services |

Docker Compose is tooling, not a Python package.

## Dev and testing later

| Package | What it would be for | When/notes |
| --- | --- | --- |
| pytest-cov | Coverage reporting | When coverage becomes a question |
| hypothesis | Property-based tests | Rules invariants and protocols |
| pytest-xdist / pytest-benchmark | Parallel runs and timing | Only if the suite needs speed or comparisons |
| respx | Mocking HTTPX clients | For REST client tests |
| time-machine or freezegun | Frozen clocks | Turn timers and cooldowns |
| locust | Load testing | Before and after Phase 10 |
| import-linter | Layer boundary checks | Enforce architecture rules |
| mutmut | Mutation testing | A quality experiment, not a default |
| mkdocs-material or sphinx | Documentation site | Only if docs outgrow Markdown |

## UI alternatives

| Package | What it would be for | When/notes |
| --- | --- | --- |
| textual | Prototype TUI framework | Retained experiment, not the plan |
| prompt-toolkit | Input handling and completions | Alternative to raw termios |
| blessed / rich | Terminal capabilities, colour, tables | Optional rendering aids |

## Rules

- Add a package when the phase that needs it starts, not before.
- Prefer the standard library when it covers the problem.
- Use lower bounds, not exact pins, in `pyproject.toml`.
- A lockfile is optional; if added, keep it out of the design docs.
- `pyproject.toml` lists only current-phase dependencies; this file stays a menu.
