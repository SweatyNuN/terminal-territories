# Learning Notes

This file is about how I learn through this project, not about what the software
does. The game is the excuse; the understanding is the point.

---

## 1. The learning loop

1. **Play the current build.** Hit the limitation as a player before meeting it
   as an engineer.
2. **Name the problem.** State it as a question about behaviour, not as the name
   of a technology.
3. **Predict the constraints.** Decide what any solution must do before choosing
   a tool.
4. **Learn the concept.** Read a primary source and write the idea in my own
   words.
5. **Build the smallest version** that tests the idea.
6. **Reflect.** What broke, what surprised me, and what would I change?

---

## 2. Problem → concept map

| Player-visible problem | Concept | Phase |
| --- | --- | --- |
| "The game only exists in my terminal." | Client/server, request/response, JSON | 1 |
| "Two of us cannot play at once." | Shared state, turn enforcement, serialisation | 1, 3 |
| "Restarting loses the game." | Persistence, transactions | 2 |
| "I can edit the client and see everything." | Trust boundaries, server authority | 3 |
| "I can claim to be someone else." | Identity, tokens, hashing | 3 |
| "My move overwrote my friend's move." | Optimistic concurrency, versioning, idempotency | 3 |
| "I have to press refresh to see anything." | Push, events, deltas | 4 |
| "The map jumps backwards or flickers." | Snapshots, ordering, reconciliation | 4, 7 |
| "My ally attacked me." | Relationships, permissions, shared vision | 5 |
| "HTTP feels heavy for this." | Streams, framing, partial reads | 6 |
| "My commands vanish on bad Wi-Fi." | Loss, retries, sequence numbers, acknowledgements | 7 |
| "Expanding is always right." | Simulation, balance, design under constraints | 8 |
| "I need an opponent at 3 a.m." | Agents, evaluation, benchmarking | 9 |
| "Chat crashing took down the game." | Service boundaries, eventual consistency | 10 |

---

## 3. Pace

| If I have | I can reach | What to protect |
| --- | --- | --- |
| 2 evenings a week for 6 weeks | Phases 0–2 | Rules correctness before speed |
| 3 evenings a week for 6 weeks | Phases 0–4 | Finishing the rules engine early; push can wait until the loop is solid |
| 1 evening a week for 12 weeks | Phases 0–2, slowly | A steady rhythm over a rushed start |
| 2 evenings a week for 12 weeks | Phases 0–6 | One transport change at a time |
| 3–4 evenings a week for 12 weeks | Phases 0–8 | Room for reflection, not just output |
| Unknown weeks, limited energy | Phase 0 only | Depth over coverage: finish the game before networking it |

---

## 4. Reflection prompts

**Phases 0–1**

- What did I have to explain twice before it became a precise rule?
- Where did the client and the server disagree, and which side was wrong?
- What did I assume a player would never do?

**Phases 2–3**

- What did persistence reveal that memory hid?
- Which conflict was a design problem rather than a coding problem?
- What information did I accidentally expose?

**Phases 4–7**

- What actually changed when delivery changed?
- Which failure was new, and which had been there all along?
- Can I separate latency, ordering, and reliability in my own words?

**Phases 8–10**

- What did simulation change about my instincts?
- Where is eventual consistency invisible, and where is it not?
- What would I design differently if I started again?

---

## 5. Getting unstuck

1. Reproduce the smallest case that still fails.
2. Isolate one layer and prove the others are innocent.
3. Read the primary documentation, not a summary of it.
4. Run one experiment that changes a single variable.
5. Write the model down in plain language. If I cannot, I do not understand it
   yet.

---

## 6. My definition of done

- I can demo it without notes.
- The rules are tested before I build on them.
- I can explain the concept without pointing at the code.
- The design docs and decision records still agree with each other.
- I know the next constraint and why it matters.

---

## 7. Traps I expect

- **Coordinate systems.** Mixing row/column with x/y, and testing only on square
  maps.
- **Shared mutable state.** Something changes underneath a reader that assumed
  it was alone.
- **Blocking I/O.** One slow call freezes input and rendering together.
- **Message framing.** Assuming one read equals one message.
- **Trusting the client.** Taking identity or legality from whatever the sender
  claims.

---

A phase is finished when it changes what I can explain, not when it merely
runs.
