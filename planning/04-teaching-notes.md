# Teaching Notes

How to run the project as a course, not just as a codebase.

---

## 1. The teaching loop

Every phase follows the same rhythm. It matters more than the slides.

1. **Play the current build (10 min).** Students hit the limitation as players
   before they meet it as engineers.
2. **Name the problem (5 min).** Write it on the board as a question, not a
   technology: "Why does the map not update until I press a key?"
3. **Predict (10 min).** Ask what a solution must do. Collect constraints
   before naming the tool.
4. **Introduce the concept (15 min).** Short, with one minimal example and one
   counter-example. No framework tour.
5. **Build in pairs (60–90 min).** Pair programming; rotate driver every
   milestone.
6. **Integrate (15 min).** Merge into `main` behind a working demo. Red CI is
   not "done".
7. **Retro (10 min).** What broke? What would you change? One sentence each.

The instructor writes code live for the risky parts, especially Phase 6 and 7.
Framing and lossy networks do not read well from slides.

---

## 2. Problem → concept map

Use this when a student asks "why are we learning this?"

| Player-visible problem | Engineering concept | Phase |
| --- | --- | --- |
| "The game only exists in my terminal." | Client/server, REST, JSON | 1 |
| "Two of us cannot play at once." | Shared state, turn enforcement, locking | 1, 3 |
| "Restarting loses the game." | Persistence, SQL, transactions | 2 |
| "I can edit the client and see everything." | Server authority, threat modelling | 3 |
| "I can claim to be someone else." | Authentication, hashing, tokens | 3 |
| "My move overwrote my friend's move." | Optimistic concurrency, versioning, idempotency | 3 |
| "I have to press refresh to see anything." | Push, WebSockets, events, deltas | 4 |
| "The map jumps backwards / flickers." | Snapshots vs deltas, ordering, reconciliation | 4, 7 |
| "My ally attacked me." | Relationship state, permissions, state machines | 5 |
| "HTTP is heavy for this." | Streams, framing, TCP, partial reads | 6 |
| "My commands vanish on bad Wi-Fi." | UDP, loss, retries, sequence numbers, acks | 7 |
| "Expanding is always right." | Simulation, balancing, design under constraints | 8 |
| "I need an opponent at 3 a.m." | Agents, evaluation, benchmarking | 9 |
| "Chat crashing took down the game." | Service boundaries, events, eventual consistency | 10 |

---

## 3. Suggested schedules

### Six weeks (the common case)

| Week | Content | Deliverable |
| --- | --- | --- |
| 1 | Phase 0 | Tested rules engine + hot-seat play |
| 2 | Phase 1 | REST server + ANSI terminal client |
| 3 | Phase 2 | SQLite persistence + migrations |
| 4 | Phase 3 | Auth, fog of war, conflict handling |
| 5 | Phase 4 | WebSocket updates + reconnect |
| 6 | Phase 5 (lite) | Alliances + course retro, demo day |

### Twelve weeks

Phases 0–4 in weeks 1–6 as above, then one phase per week for 5–10, with the
last week reserved for presentations and the incident drill.

If you must compress further, cut Phase 2 rather than Phase 0. A rules engine
plus REST plus fog plus sockets is a better course than persistence with
untested combat.

---

## 4. Session-level exercises

**Phase 0**

- Write a failing test for a rule that is not implemented, then implement it.
- Break the renderer by swapping `x` and `y`. Show why non-square maps catch it.
- Build one ANSI frame as a list of lines, then write it with home + erase-to-end.
  Compare against a full clear and explain the flicker.
- Ask: why is `apply_action` returning a new state instead of changing one?

**Phase 1**

- Add one endpoint without touching existing code (e.g. `GET /games`).
- Deliberately send malformed JSON and map every status code.
- Write a client in `curl` only, with no Python, to prove the API is the
  contract.
- Parse `\x1b[A` without swallowing the next keystroke. Test a lone `ESC`, a
  partial sequence, and an arrow key pressed twice quickly.
- Time one render and one poll at a 20 FPS cap. What is the frame budget, and
  what must never run inside it?

**Phase 2**

- Time a full-game load before and after adding indexes.
- Add `players.reputation` as a migration with existing rows.
- Show two processes writing SQLite concurrently and discuss the result.

**Phase 3**

- Attack the game: replay an old request, tamper with a token, read another
  player's tile. Each gets a test.
- Ask which of the five "CIA" properties each fix supports.

**Phase 4**

- Instrument request counts before/after push.
- Add an artificial 3-second server delay: what should the UI show?
- Move the network call onto a worker thread and drain a bounded queue. Prove
  that input and rendering stay responsive during the delay.
- Disconnect the client mid-turn and compare local and server state.

**Phase 5**

- Design a 3-player kingmaking scenario. Is it a rule problem or a social one?
- Implement "shared vision reveals only current sight, not memory" as a variant.

**Phase 6**

- Hand-write a framed client in another language (or in `nc`) to prove the
  protocol is understandable.
- Fuzz the decoder with random bytes; it must never crash the server.

**Phase 7**

- Turn on 30% loss and narrate what the debug overlay does.
- Ask: which commands can be duplicated safely, and which cannot? Relate it to
  HTTP methods and idempotency.
- Compare game feel at 10 Hz vs 30 Hz snapshots.
- Run the Pygame client with `SDL_VIDEODRIVER=dummy`; assert interpolation and
  overlay counters without opening a window.

**Phase 8**

- Two balance hypotheses, one simulation each. Report which survived.
- Make upkeep configurable and run a tournament with three values.

**Phase 9**

- Write a bot that only expands. Then one that only attacks. Explain the
  results with the map.
- Add a "cheater" bot that sends illegal actions and assert the rejection rate.

**Phase 10**

- Incident drill: kill one service while a game is running. Write the timeline.
- Ask where consistency can be eventual without a player noticing.

---

## 5. Bugs students will write (and what each teaches)

| Bug | Lesson |
| --- | --- |
| `(row, col)` vs `(x, y)` | Naming and coordinates; test with non-square boards |
| Mutating `GameState` in place | Value semantics; replayability |
| Trusting `player_id` from the request body | Identity comes from the token |
| Client-side fog filtering | Hiding is not the same as not sending |
| Read-modify-write without a version check | Lost updates, optimistic concurrency |
| Retrying a POST without an idempotency key | Double-spend, at-least-once delivery |
| `time.sleep` in an async handler | Blocking the event loop |
| Clearing the screen after drawing | ANSI ordering, flicker, frame diffing |
| Blocking HTTP/socket call in the render loop | Worker threads, queues, frame budgets |
| Missing terminal restore on crash | `finally`, signals, terminal lifecycle |
| Unbounded event queue | Backpressure, memory, coalescing |
| Busy-wait redraw loop | Dirty flags, frame caps, idle waits |
| Sharing mutable state across threads | Immutable events, single-owner state |
| `recv(4096)` assumed to be one message | Stream framing, partial reads |
| Full state broadcast on every event | Deltas, bandwidth, backpressure |
| Global mutable game dict without a lock | Races across awaits, per-game locks |
| Wall-clock time for cooldowns | Server time, monotonic clocks, tick numbers |
| Floats for resources | Integer arithmetic, rounding |
| One giant JSON blob in SQL | Data modelling, queryability |
| Silent `except Exception: pass` | Observability, error taxonomies |
| Bots with special endpoints | Dogfooding your own API |

When a student hits one, do not fix it immediately. Ask them to write the
failing test first, then let the test explain the bug.

---

## 6. Assessment

Suggested weighting for a project-based course:

| Criterion | Weight | What "excellent" looks like |
| --- | --- | --- |
| Rules correctness | 25% | Edge cases tested; deterministic; invalid actions rejected with precise codes |
| Architecture | 20% | `core` is I/O-free; a transport can be swapped without touching rules |
| Testing | 20% | Unit + integration + one end-to-end game; tests document behaviour |
| Security and robustness | 15% | Auth, fog, versioning, idempotency, malformed input handled |
| Code quality | 10% | Readable names, small functions, typed DTOs, no magic numbers |
| Documentation and demo | 10% | Protocol docs, ADRs, a 5-minute demo that survives questions |

A strong signal: the student can explain *why* a rule lives in `core` and not
in a route handler.

---

## 7. Classroom operations

- **Ports:** server on `8000`; give each student pair `TT_PORT=8000 + n` to
  avoid collisions on shared machines.
- **Demo day:** run one server on the projector, four clients in separate
  terminals, one player using `curl` to prove the API is honest.
- **Determinism:** always pass `TT_SEED` in class so bugs reproduce. Store the
  seed in the game record and show it in the UI.
- **Timeboxing:** use the round limit (20) for demos. A 3-second turn timer in
  real-time mode keeps demos moving.
- **Git:** one branch per phase, merged into `main` only when the definition of
  done is met. Tag each merge `vN` so students can check out any phase.
- **Pairing:** pairs keep one shared repo; reviewers are a different pair. The
  review is graded as part of the reviewer's participation.

### Demo script for the end of the course

1. Create a game with a fixed seed; show the seed.
2. Two players join: one uses the ANSI terminal client, one uses `curl`.
3. Capture a capital; show elimination and neutralisation of the loser's tiles.
4. Restart the server; rejoin and continue.
5. Toggle fog: show two clients seeing different maps.
6. Turn on 10% packet loss in real-time mode; show the overlay correcting.
7. Show a finished game on the leaderboard, written by a separate service.
8. Show the ADR list and one failing test that was written before its fix.

---

## 8. Differentiation

**Students who finish early**

- Write the property-based invariant suite.
- Implement a protocol fuzzer and a chaos proxy with more failure modes.
- Add an ADR arguing against a decision made in class, with evidence.
- Build a second client (web or TUI in another language) against the OpenAPI
  schema.

**Students who struggle**

- Pair them on renderer and UI work first; the feedback loop is immediate.
- Give them the combat table as test cases and let them implement to the tests.
- Reduce scope to Phases 0–1 and make the demo excellent.
- Encourage a `curl`-only client early: it demystifies the whole stack.

**No prior Python experience**

Spend a session on dataclasses, type hints, `pytest`, and f-strings before
Phase 0. The game is a bad place to learn both Python and networking at once.

---

## 9. Instructor checklist per phase

- [ ] Demo of the previous phase still works
- [ ] The problem is stated as a question and felt by playing
- [ ] The seam for this phase already exists in the architecture
- [ ] Tests and CI updated in the same merge
- [ ] Protocol/README updated with the change
- [ ] One ADR or design note written
- [ ] Retro completed and captured
- [ ] Next phase's broken build is *not* pre-emptively fixed
