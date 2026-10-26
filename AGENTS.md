# Agent Notes — Terminal Territories

Memory file for future agent sessions on this repository.

## Goal

The design documents support the owner's own implementation and learning. The owner writes the code. Do not implement code unless explicitly asked.

## What success looks like

The owner can implement and explain each phase without the docs dictating the code. The docs are a thinking tool, not a build manual.

## Hard rules for doc edits

- Never update the docs to match the current code. Do not add code-status tables, gap lists, or "implemented / not implemented" markers.
- No code, code file paths, function signatures, test matrices, acceptance criteria, step-by-step build instructions, or exact endpoints unless the owner explicitly asks for code-specific docs.
- Keep documents concise. One canonical source per topic. Delete duplication instead of adding another document.
- Use personal, project-focused language. Write for the owner, not for a room.
- If a rule decision changes, update `planning/01-game-mechanics.md` and its resolved-decisions table, then check 02 and 05 for references.
- Do not create a new document without a unique purpose.
- Prefer editing the canonical document over appending a section that repeats it.
- `pyproject.toml` lists only dependencies the current phase imports. Future options stay in `PACKAGES.md`; do not move them into `pyproject.toml` until the phase begins.

## Voice

- First person or neutral project voice.
- State problems as questions a player or builder would ask.
- Short sentences, concrete examples, no marketing tone.
- One good example beats three abstractions.
- No progress reports; docs describe design, not history.

## Canonical map and target lengths

| Document | Purpose | Target |
| --- | --- | --- |
| `planning/01-game-mechanics.md` | Canonical rules | ~320 lines |
| `planning/02-development-phases.md` | Technology progression | ~230 |
| `planning/03-architecture.md` | Boundaries and invariants | ~130 |
| `planning/04-learning-notes.md` | Personal learning loop | ~120 |
| `planning/05-client-plan.md` | Terminal-first client plan | ~110 |
| `PACKAGES.md` | Future package options (not dependencies) | ~140 |
| `README.md` | Pitch and project map | ~80 |
| `planning/README.md` | Design-pack map | ~55 |

Targets are upper bounds in spirit. Shorter is fine; longer needs a reason.

## Audit checklist

Before finishing a doc edit, verify:

- Numbers agree across documents: players, board size, rounds, action points, costs, caps, victory conditions.
- Every relative link resolves. Do not link to deleted documents.
- Dependencies in `pyproject.toml` match current imports; future packages are only suggestions in `PACKAGES.md`.
- No rule is stated twice unless one version is a deliberate summary that links to 01.
- No code, code file paths, endpoints, status tables, or acceptance criteria crept in.
- No framing that treats the reader as a group being led.
- Markdown tables have matching header and delimiter columns.
- Code fences are paired and language-tagged where useful.
- The result reads as a design spec, not a build log.

## Editing workflow

1. Read `planning/01-game-mechanics.md` first.
2. Edit the canonical document for the topic.
3. Sweep links and numbers across 02 and 05.
4. Run the audit checklist.
5. Delete anything that only restates another section.

## Boundaries

- Do not modify Python code or tests during a documentation pass.
- Do not create a parallel version of a document; edit the canonical one.
- Do not add changelog or status sections.
- When unsure, delete rather than add.

## Later, code-specific docs

Code-specific documentation is a separate, later request. Wait until the owner has implemented something and asked for docs that describe it. Do not pre-write build guides, API references, or test plans.
